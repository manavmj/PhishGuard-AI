import React, { useState, useRef, useEffect } from 'react';
import { 
  Shield, 
  Send, 
  HelpCircle, 
  Info, 
  History, 
  MessageSquare, 
  AlertTriangle, 
  CheckCircle2, 
  AlertCircle,
  FileText,
  Image as ImageIcon,
  Mic,
  Link as LinkIcon,
  X,
  Plus,
  ArrowRight,
  ShieldCheck,
  ShieldAlert,
  Loader2
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { useDropzone } from 'react-dropzone';
import ReactMarkdown from 'react-markdown';
import { cn } from './lib/utils';
import { analyzeContent, AnalysisResult } from './services/gemini';

type Message = {
  id: string;
  type: 'user' | 'bot';
  content: string;
  timestamp: string;
  isAnalysis?: boolean;
  fileType?: 'text' | 'image' | 'pdf' | 'audio' | 'url';
  filePreview?: string;
};

export default function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      type: 'bot',
      content: `👋 Welcome to PhishGuard AI — Your Real-Time Phishing & Spam Detector!

I can analyze:
📩 Text messages / emails (English & Hindi)
📸 Screenshots (send as image)
📄 PDFs (forward suspicious documents)
🔗 URLs / links (paste the link)
🎙️ Voice messages (send audio)
📲 Forwarded notifications (forward directly here)

**Multilingual Support:** I now support analysis of content in Hindi and Hinglish!

Just send me anything suspicious and I'll tell you if it's SAFE ✅ or DANGEROUS ⚠️.

Commands:
/start — Show this welcome message
/help — Detailed usage guide
/about — How PhishGuard AI works
/feedback — Report a wrong verdict
/stats — Your scan history (this session)`,
      timestamp: new Date().toLocaleTimeString(),
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  const [showClearConfirm, setShowClearConfirm] = useState(false);

  const clearChat = () => {
    setMessages([messages[0]]);
    setShowClearConfirm(false);
  };

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const onDrop = async (acceptedFiles: File[]) => {
    for (const file of acceptedFiles) {
      const reader = new FileReader();
      reader.onload = async () => {
        const base64Data = (reader.result as string).split(',')[1];
        const mimeType = file.type;
        
        let fileType: Message['fileType'] = 'text';
        if (mimeType.startsWith('image/')) fileType = 'image';
        else if (mimeType === 'application/pdf') fileType = 'pdf';
        else if (mimeType.startsWith('audio/')) fileType = 'audio';

        const userMessage: Message = {
          id: Date.now().toString(),
          type: 'user',
          content: `Sent a ${fileType}: ${file.name}`,
          timestamp: new Date().toLocaleTimeString(),
          fileType,
          filePreview: mimeType.startsWith('image/') ? (reader.result as string) : undefined,
        };

        setMessages(prev => [...prev, userMessage]);
        setIsAnalyzing(true);

        try {
          const result = await analyzeContent([{ data: base64Data, mimeType }]);
          const botMessage: Message = {
            id: (Date.now() + 1).toString(),
            type: 'bot',
            content: result.text,
            timestamp: result.timestamp,
            isAnalysis: true,
          };
          setMessages(prev => [...prev, botMessage]);
        } catch (error) {
          console.error('Analysis failed:', error);
          setMessages(prev => [...prev, {
            id: (Date.now() + 1).toString(),
            type: 'bot',
            content: '⚠️ Sorry, I encountered an error while analyzing that file. Please try again.',
            timestamp: new Date().toLocaleTimeString(),
          }]);
        } finally {
          setIsAnalyzing(false);
        }
      };
      reader.readAsDataURL(file);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ 
    onDrop,
    accept: {
      'image/*': [],
      'application/pdf': [],
      'audio/*': []
    }
  });

  const handleSend = async () => {
    if (!inputValue.trim()) return;

    const text = inputValue.trim();
    setInputValue('');

    // Handle commands
    if (text.startsWith('/')) {
      handleCommand(text);
      return;
    }

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: text,
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsAnalyzing(true);

    try {
      const result = await analyzeContent(text);
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: result.text,
        timestamp: result.timestamp,
        isAnalysis: true,
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Analysis failed:', error);
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: '⚠️ Sorry, I encountered an error while analyzing that message. Please try again.',
        timestamp: new Date().toLocaleTimeString(),
      }]);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleCommand = (command: string) => {
    let response = '';
    switch (command.toLowerCase()) {
      case '/start':
        response = messages[0].content;
        break;
      case '/help':
        response = `📖 **PhishGuard AI Usage Guide**

**1. Text Analysis**
Paste any suspicious email, SMS, or WhatsApp message. I'll look for urgency, impersonation, and data requests.

**2. Screenshot Analysis**
Send a screenshot of a bank alert, login page, or OTP screen. I'll analyze the visual design and text.

**3. PDF Analysis**
Forward suspicious invoices, job offers, or notices. I'll scan for malicious links and fraud patterns.

**4. URL Analysis**
Paste a link. I'll analyze the domain structure and reputation without visiting it.

**5. Audio Analysis**
Send a voice message. I'll transcribe and analyze it for vishing (voice phishing) tactics.`;
        break;
      case '/about':
        response = `🛡️ **About PhishGuard AI**

PhishGuard AI is an advanced cybersecurity tool developed to combat the rising tide of digital fraud. 

**Model:** Gemini 2.0 Multimodal AI
**Approach:** Real-time signal extraction and threat scoring.
**Disclaimer:** This tool provides advisory verdicts. Always verify through official channels.

Developed for Medicaps University, 2026.`;
        break;
      case '/feedback':
        response = `📝 **Feedback Received**
Thank you for helping us improve! Our team will review the last verdict to refine our AI models.`;
        break;
      case '/stats':
        const scans = messages.filter(m => m.isAnalysis).length;
        response = `📊 **Your Session Stats**
Total Scans: ${scans}
Last Scan: ${messages.filter(m => m.isAnalysis).pop()?.timestamp || 'None'}`;
        break;
      default:
        response = `❌ Unknown command: ${command}. Type /help for a list of commands.`;
    }

    setMessages(prev => [...prev, {
      id: Date.now().toString(),
      type: 'user',
      content: command,
      timestamp: new Date().toLocaleTimeString(),
    }, {
      id: (Date.now() + 1).toString(),
      type: 'bot',
      content: response,
      timestamp: new Date().toLocaleTimeString(),
    }]);
  };

  const getVerdictColor = (content: string) => {
    if (content.includes('SAFE ✅')) return 'text-emerald-500';
    if (content.includes('LOW RISK ⚠️')) return 'text-yellow-500';
    if (content.includes('MEDIUM RISK 🟠')) return 'text-orange-500';
    if (content.includes('HIGH RISK 🔴')) return 'text-red-500';
    if (content.includes('PHISHING 🚨')) return 'text-red-600 font-bold';
    return 'text-blue-400';
  };

  return (
    <div className="flex h-screen bg-[#0a0a0a] text-zinc-100 font-sans selection:bg-emerald-500/30">
      {/* Sidebar - History */}
      <AnimatePresence>
        {showHistory && (
          <motion.div
            initial={{ x: -300, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: -300, opacity: 0 }}
            className="w-72 border-r border-white/10 bg-[#0f0f0f] flex flex-col"
          >
            <div className="p-4 border-bottom border-white/10 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <History className="w-4 h-4 text-emerald-500" />
                <span className="font-medium text-sm uppercase tracking-wider">Scan History</span>
              </div>
              <button onClick={() => setShowHistory(false)} className="p-1 hover:bg-white/5 rounded">
                <X className="w-4 h-4" />
              </button>
            </div>
            <div className="flex-1 overflow-y-auto p-2 space-y-2">
              {messages.filter(m => m.isAnalysis).length === 0 ? (
                <div className="text-center py-10 text-zinc-500 text-xs">No scans yet</div>
              ) : (
                messages.filter(m => m.isAnalysis).map(m => (
                  <div key={m.id} className="p-3 rounded-lg bg-white/5 border border-white/5 hover:border-emerald-500/30 transition-colors cursor-pointer group">
                    <div className="text-[10px] text-zinc-500 mb-1">{m.timestamp}</div>
                    <div className="text-xs line-clamp-2 text-zinc-300 group-hover:text-emerald-400 transition-colors">
                      {m.content.split('\n')[5] || 'Analysis Report'}
                    </div>
                  </div>
                ))
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col relative overflow-hidden">
        {/* Header */}
        <header className="h-16 border-b border-white/10 bg-[#0a0a0a]/80 backdrop-blur-md flex items-center justify-between px-6 z-10">
          <div className="flex items-center gap-3">
            {!showHistory && (
              <button onClick={() => setShowHistory(true)} className="p-2 hover:bg-white/5 rounded-full transition-colors">
                <History className="w-5 h-5 text-zinc-400" />
              </button>
            )}
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center shadow-[0_0_15px_rgba(16,185,129,0.3)]">
                <Shield className="w-5 h-5 text-black" />
              </div>
              <div>
                <h1 className="text-sm font-bold tracking-tight">PHISHGUARD AI</h1>
                <div className="flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse" />
                  <span className="text-[10px] text-emerald-500/80 font-mono uppercase tracking-widest">System Active</span>
                </div>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-4 relative">
            {showClearConfirm ? (
              <div className="absolute right-0 top-full mt-2 bg-[#1a1b1e] border border-white/10 rounded-xl p-3 shadow-2xl z-20 flex items-center gap-3 min-w-[200px]">
                <span className="text-xs text-zinc-400">Clear chat?</span>
                <button onClick={clearChat} className="px-3 py-1 bg-red-500 text-white text-[10px] font-bold rounded-lg hover:bg-red-600 transition-colors">YES</button>
                <button onClick={() => setShowClearConfirm(false)} className="px-3 py-1 bg-white/5 text-zinc-400 text-[10px] font-bold rounded-lg hover:bg-white/10 transition-colors">NO</button>
              </div>
            ) : null}
            <button onClick={() => setShowClearConfirm(true)} className="p-2 hover:bg-white/5 rounded-full transition-colors group">
              <X className="w-5 h-5 text-zinc-400 group-hover:text-red-400" />
            </button>
            <button onClick={() => handleCommand('/help')} className="p-2 hover:bg-white/5 rounded-full transition-colors group">
              <HelpCircle className="w-5 h-5 text-zinc-400 group-hover:text-emerald-400" />
            </button>
            <button onClick={() => handleCommand('/about')} className="p-2 hover:bg-white/5 rounded-full transition-colors group">
              <Info className="w-5 h-5 text-zinc-400 group-hover:text-emerald-400" />
            </button>
          </div>
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-hide">
          <div className="max-w-3xl mx-auto space-y-6">
            {messages.map((message) => (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                key={message.id}
                className={cn(
                  "flex flex-col",
                  message.type === 'user' ? "items-end" : "items-start"
                )}
              >
                <div className={cn(
                  "max-w-[85%] rounded-2xl p-4 text-sm leading-relaxed",
                  message.type === 'user' 
                    ? "bg-emerald-500 text-black font-medium rounded-tr-none" 
                    : message.isAnalysis 
                      ? "bg-[#151619] border border-white/10 w-full font-mono text-zinc-300 rounded-tl-none shadow-xl"
                      : "bg-[#1a1b1e] text-zinc-300 rounded-tl-none"
                )}>
                  {message.filePreview && (
                    <img 
                      src={message.filePreview} 
                      alt="Preview" 
                      className="w-full max-h-64 object-contain rounded-lg mb-3 border border-white/10"
                      referrerPolicy="no-referrer"
                    />
                  )}
                  {message.fileType && !message.filePreview && (
                    <div className="flex items-center gap-3 p-3 bg-black/20 rounded-lg mb-3 border border-white/5">
                      {message.fileType === 'pdf' && <FileText className="w-8 h-8 text-red-400" />}
                      {message.fileType === 'audio' && <Mic className="w-8 h-8 text-blue-400" />}
                      <span className="text-xs opacity-70 truncate">{message.content}</span>
                    </div>
                  )}
                  <div className={cn(
                    "whitespace-pre-wrap",
                    message.isAnalysis && "markdown-body"
                  )}>
                    {message.isAnalysis ? (
                      <ReactMarkdown>{message.content}</ReactMarkdown>
                    ) : (
                      message.content
                    )}
                  </div>
                </div>
                <span className="text-[10px] text-zinc-500 mt-1.5 px-1 font-mono">
                  {message.timestamp}
                </span>
              </motion.div>
            ))}
            {isAnalyzing && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex flex-col items-start"
              >
                <div className="bg-[#151619] border border-white/10 rounded-2xl p-4 rounded-tl-none flex items-center gap-3">
                  <Loader2 className="w-4 h-4 text-emerald-500 animate-spin" />
                  <span className="text-xs text-emerald-500/80 font-mono uppercase tracking-widest">Analyzing Content...</span>
                </div>
              </motion.div>
            )}
            <div ref={chatEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="p-6 bg-gradient-to-t from-[#0a0a0a] to-transparent">
          <div className="max-w-3xl mx-auto">
            <div className="relative group">
              <div {...getRootProps()} className={cn(
                "absolute -top-12 left-0 right-0 h-10 border border-dashed rounded-lg flex items-center justify-center transition-all duration-300",
                isDragActive 
                  ? "bg-emerald-500/10 border-emerald-500 opacity-100 translate-y-0" 
                  : "border-white/10 opacity-0 translate-y-2 pointer-events-none"
              )}>
                <input {...getInputProps()} />
                <p className="text-[10px] uppercase tracking-widest text-emerald-500 font-bold">Drop files to scan</p>
              </div>

              <div className="bg-[#1a1b1e] border border-white/10 rounded-2xl shadow-2xl focus-within:border-emerald-500/50 transition-all duration-300 overflow-hidden">
                <div className="flex items-end p-2 gap-2">
                  <div className="flex items-center gap-1 pb-1.5 pl-2">
                    <button {...getRootProps()} className="p-2 hover:bg-white/5 rounded-full transition-colors text-zinc-400 hover:text-emerald-400">
                      <Plus className="w-5 h-5" />
                    </button>
                    <button className="p-2 hover:bg-white/5 rounded-full transition-colors text-zinc-400 hover:text-emerald-400">
                      <Mic className="w-5 h-5" />
                    </button>
                  </div>
                  <textarea
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        handleSend();
                      }
                    }}
                    placeholder="Paste message, URL, or drag files here..."
                    className="flex-1 bg-transparent border-none focus:ring-0 text-sm py-3 resize-none max-h-32 min-h-[44px] scrollbar-hide"
                    rows={1}
                  />
                  <div className="pb-1.5 pr-2">
                    <button
                      onClick={handleSend}
                      disabled={!inputValue.trim() || isAnalyzing}
                      className={cn(
                        "p-2.5 rounded-xl transition-all duration-300 flex items-center justify-center",
                        inputValue.trim() && !isAnalyzing
                          ? "bg-emerald-500 text-black shadow-[0_0_15px_rgba(16,185,129,0.4)] hover:scale-105 active:scale-95"
                          : "bg-white/5 text-zinc-600 cursor-not-allowed"
                      )}
                    >
                      <Send className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              </div>
              <div className="mt-3 flex items-center justify-center gap-6">
                <div className="flex items-center gap-1.5 text-[10px] text-zinc-500 uppercase tracking-widest">
                  <ShieldCheck className="w-3 h-3 text-emerald-500" />
                  <span>Secure Analysis</span>
                </div>
                <div className="flex items-center gap-1.5 text-[10px] text-zinc-500 uppercase tracking-widest">
                  <ShieldAlert className="w-3 h-3 text-red-500" />
                  <span>Real-time Detection</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
