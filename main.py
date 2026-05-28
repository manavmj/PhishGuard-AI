# ============================================================
#  PhishGuard AI — main.py
#  Entry point — run this file to start the bot
#
#  HOW TO RUN:
#  In PyCharm: click the green ▶ play button on this file
#  In terminal: python main.py
#
#  BEFORE RUNNING:
#  1. Make sure .env file exists with your tokens
#  2. Make sure system_prompt.txt exists
#  3. Run train_model.py first (if not already done)
#  4. Install dependencies: pip install -r requirements.txt
# ============================================================

import sys
import os

def check_requirements():
    """
    Check that all required files exist before starting the bot.
    Gives clear error messages if anything is missing.
    """
    errors = []

    # Check .env file
    if not os.path.exists(".env"):
        errors.append(
            "❌ .env file not found!\n"
            "   Create a .env file with:\n"
            "   TELEGRAM_BOT_TOKEN=your_token_here\n"
            "   GEMINI_API_KEY=your_key_here"
        )

    # Check system prompt
    if not os.path.exists("system_prompt.txt"):
        errors.append(
            "❌ system_prompt.txt not found!\n"
            "   Create system_prompt.txt in the project root folder."
        )

    # Check model files (warning only, not fatal)
    if not os.path.exists(os.path.join("model", "phishing_model.pkl")):
        print(
            "⚠️  Warning: phishing_model.pkl not found.\n"
            "   Run train_model.py first for ML model support.\n"
            "   The bot will still work using Gemini AI only.\n"
        )

    if errors:
        print("\n" + "=" * 55)
        print("  PHISHGUARD AI — STARTUP ERRORS")
        print("=" * 55)
        for err in errors:
            print(f"\n{err}")
        print("\n" + "=" * 55)
        sys.exit(1)


def main():
    """Main entry point — starts the PhishGuard AI bot."""

    print()
    print("=" * 55)
    print("  🛡️  PHISHGUARD AI — STARTING UP")
    print("=" * 55)

    # ── Pre-flight checks ──────────────────────────────────────
    check_requirements()

    # ── Import and create bot ──────────────────────────────────
    from bot import create_bot

    app = create_bot()

    print()
    print("=" * 55)
    print("  ✅ PhishGuard AI Bot is RUNNING!")
    print("  Open Telegram and message your bot.")
    print("  Press Ctrl+C to stop the bot.")
    print("=" * 55)
    print()

    # ── Start polling (long-polling mode) ──────────────────────
    # The bot will keep running until Ctrl+C is pressed
    app.run_polling(
        allowed_updates=["message"],  # Only process message updates
        drop_pending_updates=True,    # Ignore messages sent while bot was offline
    )


if __name__ == "__main__":
    main()