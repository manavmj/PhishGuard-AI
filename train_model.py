# ============================================================
#  PhishGuard AI — train_model.py
#  Trains the Logistic Regression phishing classifier
#  and saves model.pkl + vectorizer.pkl
#
#  HOW TO RUN:
#  In PyCharm terminal: python train_model.py
#  OR click the green play button on this file
# ============================================================

import os
import pandas as pd
import joblib
import nltk

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

# Local imports
from utils.preprocess import clean_text

# ─── Download NLTK data if needed ─────────────────────────────
nltk.download("punkt",     quiet=True)
nltk.download("stopwords", quiet=True)

# ─── Paths ────────────────────────────────────────────────────
DATASET_PATH = os.path.join("data", "phishing_dataset.csv")
MODEL_PATH   = os.path.join("model", "phishing_model.pkl")
VECTOR_PATH  = os.path.join("model", "vectorizer.pkl")


# ─── Step 1: Load Dataset ─────────────────────────────────────
def load_dataset(path: str) -> pd.DataFrame:
    """
    Load the phishing dataset from a CSV file.
    Expected columns: text (or email_text) + label (0=safe, 1=phishing)
    """
    print(f"[1/6] Loading dataset from: {path}")

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"\n❌ Dataset not found at: {path}\n"
            f"Please place your phishing_dataset.csv file inside the 'data/' folder.\n"
            f"You can download datasets from:\n"
            f"  - https://www.kaggle.com/datasets (search 'phishing email dataset')\n"
            f"  - https://archive.ics.uci.edu/ml/datasets/SMS+Spam+Collection"
        )

    df = pd.read_csv(path)
    print(f"    ✅ Loaded {len(df)} records")
    print(f"    Columns: {list(df.columns)}")
    return df


# ─── Step 2: Prepare Data ─────────────────────────────────────
def prepare_data(df: pd.DataFrame):
    """
    Detect text and label columns, combine if needed,
    and clean the text.
    """
    print("[2/6] Preparing data...")

    # ── Auto-detect text column ────────────────────────────────
    text_col = None
    for col in ["email_text", "text", "message", "body", "content", "sms"]:
        if col in df.columns:
            text_col = col
            break

    # If no standard name, try combining subject + body + url
    if text_col is None:
        possible_combos = ["subject", "body", "url"]
        found = [c for c in possible_combos if c in df.columns]
        if found:
            df["email_text"] = df[found].fillna("").agg(" ".join, axis=1)
            text_col = "email_text"
        else:
            # Use first string column
            text_col = df.select_dtypes(include="object").columns[0]

    # ── Auto-detect label column ───────────────────────────────
    label_col = None
    for col in ["label", "class", "spam", "phishing", "target", "Category"]:
        if col in df.columns:
            label_col = col
            break

    if label_col is None:
        label_col = df.select_dtypes(include=["int64", "float64"]).columns[0]

    print(f"    Text column  : {text_col}")
    print(f"    Label column : {label_col}")

    # ── Normalize labels to 0/1 ───────────────────────────────
    df[label_col] = df[label_col].astype(str).str.lower()
    label_map = {
        "1": 1, "phishing": 1, "spam": 1, "yes": 1, "ham": 0,
        "0": 0, "legitimate": 0, "safe": 0, "no": 0, "not spam": 0,
    }
    df["label"] = df[label_col].map(label_map)

    # Drop rows with unmapped labels
    df = df.dropna(subset=["label", text_col])
    df["label"] = df["label"].astype(int)

    print(f"    Label distribution:\n{df['label'].value_counts().to_string()}")
    print(f"    Total usable records: {len(df)}")

    return df[text_col].tolist(), df["label"].tolist()


# ─── Step 3: Preprocess Text ──────────────────────────────────
def preprocess_texts(texts: list) -> list:
    """Apply clean_text() to every sample in the dataset."""
    print("[3/6] Preprocessing text (this may take a minute)...")
    cleaned = [clean_text(t) for t in texts]
    print(f"    ✅ Preprocessing complete")
    return cleaned


# ─── Step 4: TF-IDF Vectorization ────────────────────────────
def vectorize(texts_train, texts_test):
    """
    Fit TF-IDF vectorizer on training data only.
    Transform both train and test sets.
    """
    print("[4/6] Vectorizing with TF-IDF...")

    vectorizer = TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),   # Unigrams and bigrams
        min_df=2,             # Ignore very rare terms
        sublinear_tf=True,    # Apply log normalization
    )

    X_train = vectorizer.fit_transform(texts_train)
    X_test  = vectorizer.transform(texts_test)

    print(f"    Feature matrix shape (train): {X_train.shape}")
    print(f"    Feature matrix shape (test) : {X_test.shape}")

    return vectorizer, X_train, X_test


# ─── Step 5: Train Model ──────────────────────────────────────
def train_model(X_train, y_train):
    """Train Logistic Regression classifier."""
    print("[5/6] Training Logistic Regression model...")

    clf = LogisticRegression(
        max_iter=1000,
        C=1.0,
        solver="lbfgs",
        random_state=42,
        class_weight="balanced",   # Handle class imbalance
    )
    clf.fit(X_train, y_train)
    print("    ✅ Model trained successfully")
    return clf


# ─── Step 6: Evaluate and Save ───────────────────────────────
def evaluate_and_save(clf, vectorizer, X_test, y_test):
    """Evaluate model on test set and save artifacts."""
    print("[6/6] Evaluating model...")

    y_pred = clf.predict(X_test)

    acc  = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec  = recall_score(y_test, y_pred, zero_division=0)
    f1   = f1_score(y_test, y_pred, zero_division=0)

    print()
    print("=" * 50)
    print("  MODEL EVALUATION RESULTS")
    print("=" * 50)
    print(f"  Accuracy  : {acc:.4f}  ({acc*100:.2f}%)")
    print(f"  Precision : {prec:.4f}")
    print(f"  Recall    : {rec:.4f}")
    print(f"  F1-Score  : {f1:.4f}")
    print()
    print("  Classification Report:")
    print(classification_report(y_test, y_pred,
                                 target_names=["Legitimate", "Phishing"]))
    print("  Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("=" * 50)

    # Check if accuracy meets minimum threshold
    if acc < 0.90:
        print(f"\n⚠️  Warning: Accuracy {acc:.2%} is below the 90% target.")
        print("   Consider: more data, better preprocessing, or hyperparameter tuning.")
    else:
        print(f"\n✅ Accuracy {acc:.2%} meets the 90% minimum requirement!")

    # ── Save model and vectorizer ──────────────────────────────
    os.makedirs("model", exist_ok=True)
    joblib.dump(clf,        MODEL_PATH)
    joblib.dump(vectorizer, VECTOR_PATH)
    print(f"\n✅ Model saved     → {MODEL_PATH}")
    print(f"✅ Vectorizer saved → {VECTOR_PATH}")


# ─── Main Pipeline ────────────────────────────────────────────
def main():
    print()
    print("=" * 50)
    print("  PHISHGUARD AI — MODEL TRAINING PIPELINE")
    print("=" * 50)
    print()

    # Load dataset
    df = load_dataset(DATASET_PATH)

    # Prepare data
    texts, labels = prepare_data(df)

    # Preprocess text
    cleaned_texts = preprocess_texts(texts)

    # Train/test split (80/20, fixed seed for reproducibility)
    print("    Splitting dataset: 80% train / 20% test")
    texts_train, texts_test, y_train, y_test = train_test_split(
        cleaned_texts, labels,
        test_size=0.2,
        random_state=42,
        stratify=labels,
    )
    print(f"    Train size: {len(texts_train)} | Test size: {len(texts_test)}")

    # Vectorize
    vectorizer, X_train, X_test = vectorize(texts_train, texts_test)

    # Train
    clf = train_model(X_train, y_train)

    # Evaluate and save
    evaluate_and_save(clf, vectorizer, X_test, y_test)

    print()
    print("🎉 Training complete! You can now run main.py to start the bot.")
    print()


if __name__ == "__main__":
    main()