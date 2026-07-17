import React, { useState, useEffect, useRef } from "react";
import { 
  MessageSquare, Send, Upload, FileText, Trash2, 
  Settings, Sliders, ChevronDown, ChevronUp, AlertCircle, 
  CheckCircle2, RefreshCw, X, Database, Info, Sparkles
} from "lucide-react";

const API_URL = "http://localhost:8000";

function App() {
  // State for Chat
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [activeCitation, setActiveCitation] = useState(null);

  // State for Configuration
  const [config, setConfig] = useState({
    model_name: "gemini-3.1-flash-lite",
    temperature: 0.2,
    retrieval_type: "hybrid",
    top_k: 4,
    vector_weight: 0.5,
    keyword_weight: 0.5,
    use_reranker: true,
    chunk_size: 1000,
    chunk_overlap: 200
  });

  // Backend Info
  const [backendConfig, setBackendConfig] = useState({
    available_models: ["gemini-3.1-flash-lite", "gemini-1.5-flash", "gemini-1.5-pro", "gpt-4o-mini", "gpt-4o"],
    gemini_key_configured: false,
    openai_key_configured: false
  });

  // State for Documents
  const [documents, setDocuments] = useState({});
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [uploadError, setUploadError] = useState("");
  const [uploadSuccess, setUploadSuccess] = useState("");

  const chatEndRef = useRef(null);
  const fileInputRef = useRef(null);

  // Load documents and configs on mount
  useEffect(() => {
    fetchDocuments();
    fetchBackendConfig();
  }, []);

  // Scroll to bottom of chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const fetchDocuments = async () => {
    try {
      const res = await fetch(`${API_URL}/documents`);
      if (res.ok) {
        const data = await res.json();
        setDocuments(data.documents || {});
      }
    } catch (err) {
      console.error("Error fetching documents:", err);
    }
  };

  const fetchBackendConfig = async () => {
    try {
      const res = await fetch(`${API_URL}/config`);
      if (res.ok) {
        const data = await res.json();
        setBackendConfig(data);
        if (data.default_model) {
          setConfig(prev => ({ ...prev, model_name: data.default_model }));
        }
      }
    } catch (err) {
      console.error("Error fetching backend config:", err);
    }
  };

  // Drag and Drop handlers
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFilesUpload(e.dataTransfer.files);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFilesUpload(e.target.files);
    }
  };

  const handleFilesUpload = async (files) => {
    setUploading(true);
    setUploadError("");
    setUploadSuccess("");

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      if (!file.name.endsWith(".pdf") && !file.name.endsWith(".txt")) {
        setUploadError(`File '${file.name}' is unsupported. Only PDF & TXT allowed.`);
        continue;
      }

      const formData = new FormData();
      formData.append("file", file);
      formData.append("chunk_size", config.chunk_size);
      formData.append("chunk_overlap", config.chunk_overlap);

      try {
        const res = await fetch(`${API_URL}/upload`, {
          method: "POST",
          body: formData
        });

        if (res.ok) {
          setUploadSuccess(`Successfully ingested '${file.name}'`);
          fetchDocuments();
        } else {
          const errData = await res.json();
          setUploadError(`Error ingesting '${file.name}': ${errData.detail || "Server error"}`);
        }
      } catch (err) {
        setUploadError(`Connection error: Failed to upload '${file.name}'`);
      }
    }
    setUploading(false);
  };

  const handleDeleteDoc = async (filename) => {
    try {
      const res = await fetch(`${API_URL}/documents/${encodeURIComponent(filename)}`, {
        method: "DELETE"
      });
      if (res.ok) {
        fetchDocuments();
      } else {
        alert("Failed to delete document");
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleClearAll = async () => {
    if (window.confirm("Are you sure you want to clear the vector database and delete all files?")) {
      try {
        const res = await fetch(`${API_URL}/clear?delete_files=true`, { method: "POST" });
        if (res.ok) {
          setDocuments({});
          setMessages([]);
          alert("Database and folder cleared successfully!");
        }
      } catch (err) {
        console.error(err);
      }
    }
  };

  // Send query to RAG
  const handleQuery = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = { role: "user", text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setLoading(true);
    setActiveCitation(null);

    try {
      const res = await fetch(`${API_URL}/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: input,
          retrieval_type: config.retrieval_type,
          top_k: config.top_k,
          temperature: config.temperature,
          model_name: config.model_name,
          vector_weight: config.vector_weight,
          keyword_weight: config.keyword_weight,
          use_reranker: config.use_reranker
        })
      });

      if (res.ok) {
        const data = await res.json();
        setMessages(prev => [...prev, {
          role: "assistant",
          text: data.answer,
          model: data.model_used,
          sources: data.sources || []
        }]);
      } else {
        const errData = await res.json();
        setMessages(prev => [...prev, {
          role: "assistant",
          text: `Error from server: ${errData.detail || "Unable to retrieve answer."}`,
          sources: []
        }]);
      }
    } catch (err) {
      setMessages(prev => [...prev, {
        role: "assistant",
        text: "Error: Connection lost. Is the FastAPI backend running?",
        sources: []
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen bg-brandDarker text-slate-100 flex flex-col overflow-hidden">
      
      {/* Background Decorative Orbs */}
      <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] rounded-full bg-accentBlue glowing-orb" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] rounded-full bg-accentPurple glowing-orb" />

      {/* Header */}
      <header className="relative z-10 w-full px-6 py-4 glass-panel border-b flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-gradient-to-r from-accentBlue to-accentCyan p-2.5 rounded-xl shadow-lg shadow-accentBlue/20">
            <Sparkles className="w-6 h-6 text-white animate-pulse" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-100 to-slate-400">
              InsightRAG
            </h1>
            <p className="text-xs text-slate-400">Document Question Answering Pipeline</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          {/* API Config Badges */}
          <div className="hidden md:flex gap-2 text-xs">
            <span className={`px-2.5 py-1 rounded-full flex items-center gap-1.5 ${
              backendConfig.gemini_key_configured 
                ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20" 
                : "bg-amber-500/10 text-amber-400 border border-amber-500/20"
            }`}>
              <span className={`w-1.5 h-1.5 rounded-full ${backendConfig.gemini_key_configured ? "bg-emerald-400" : "bg-amber-400"}`} />
              Gemini API
            </span>
            <span className={`px-2.5 py-1 rounded-full flex items-center gap-1.5 ${
              backendConfig.openai_key_configured 
                ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20" 
                : "bg-slate-500/10 text-slate-400 border border-slate-500/10"
            }`}>
              <span className={`w-1.5 h-1.5 rounded-full ${backendConfig.openai_key_configured ? "bg-emerald-400" : "bg-slate-400"}`} />
              OpenAI API
            </span>
          </div>

          <button 
            onClick={handleClearAll}
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold bg-red-500/10 text-red-400 border border-red-500/20 hover:bg-red-500 hover:text-white transition-all duration-200"
          >
            <Database className="w-3.5 h-3.5" />
            Clear DB
          </button>
        </div>
      </header>

      {/* Main Workspace */}
      <main className="relative z-10 flex-1 flex flex-col lg:flex-row p-6 gap-6 h-[calc(100vh-80px)] overflow-hidden">
        
        {/* Left Panel: Configuration & Documents */}
        <section className="w-full lg:w-[420px] flex flex-col gap-6 overflow-y-auto pr-1">
          
          {/* Section 1: Ingestion Area */}
          <div className="glass-panel rounded-2xl p-5 flex flex-col gap-4">
            <h2 className="text-sm font-semibold text-slate-300 flex items-center gap-2 border-b border-white/5 pb-2">
              <Upload className="w-4 h-4 text-accentCyan" /> Document Ingestion
            </h2>
            
            {/* Drag Zone */}
            <div 
              onDragEnter={handleDrag}
              onDragOver={handleDrag}
              onDragLeave={handleDrag}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current.click()}
              className={`border-2 border-dashed rounded-xl p-6 text-center cursor-pointer flex flex-col items-center justify-center gap-3 transition-all duration-200 ${
                dragActive 
                  ? "border-accentBlue bg-accentBlue/5" 
                  : "border-white/10 hover:border-white/20 bg-brandDark/40"
              }`}
            >
              <input 
                ref={fileInputRef}
                type="file" 
                multiple 
                onChange={handleFileChange}
                className="hidden" 
                accept=".pdf,.txt"
              />
              <div className="p-3 bg-white/5 rounded-full">
                <Upload className="w-6 h-6 text-slate-400" />
              </div>
              <div>
                <p className="text-sm font-medium">Drag & Drop files or <span className="text-accentBlue hover:underline">browse</span></p>
                <p className="text-xs text-slate-500 mt-1">Supports PDF & TXT up to 20MB</p>
              </div>
            </div>

            {/* Notification messages */}
            {uploading && (
              <div className="flex items-center justify-center gap-2 text-xs text-accentCyan bg-accentCyan/5 border border-accentCyan/10 p-2.5 rounded-lg animate-pulse">
                <RefreshCw className="w-3.5 h-3.5 animate-spin" /> Ingesting file... building vectors...
              </div>
            )}
            {uploadError && (
              <div className="flex items-start gap-2 text-xs text-red-400 bg-red-500/5 border border-red-500/10 p-2.5 rounded-lg">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{uploadError}</span>
              </div>
            )}
            {uploadSuccess && (
              <div className="flex items-start gap-2 text-xs text-emerald-400 bg-emerald-500/5 border border-emerald-500/10 p-2.5 rounded-lg">
                <CheckCircle2 className="w-4 h-4 shrink-0" />
                <span>{uploadSuccess}</span>
              </div>
            )}

            {/* Ingested List */}
            <div className="flex flex-col gap-2 mt-2">
              <h3 className="text-xs font-semibold text-slate-400">Ingested Documents ({Object.keys(documents).length})</h3>
              <div className="max-h-[140px] overflow-y-auto flex flex-col gap-1.5 pr-1">
                {Object.keys(documents).length === 0 ? (
                  <p className="text-xs text-slate-500 italic text-center py-4 bg-brandDark/20 rounded-lg">
                    No documents uploaded yet.
                  </p>
                ) : (
                  Object.keys(documents).map((docName) => (
                    <div key={docName} className="flex items-center justify-between p-2 bg-brandDark/40 border border-white/5 rounded-lg group hover:border-white/10 transition-all duration-150">
                      <div className="flex items-center gap-2 min-w-0">
                        <FileText className="w-4 h-4 text-accentBlue shrink-0" />
                        <div className="min-w-0">
                          <p className="text-xs font-medium text-slate-300 truncate" title={docName}>{docName}</p>
                          <p className="text-[10px] text-slate-500">{documents[docName].chunk_count} chunks created</p>
                        </div>
                      </div>
                      <button 
                        onClick={() => handleDeleteDoc(docName)}
                        className="p-1 text-slate-500 hover:text-red-400 rounded hover:bg-red-500/10 transition-all duration-150"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          {/* Section 2: Pipeline Configurations */}
          <div className="glass-panel rounded-2xl p-5 flex flex-col gap-4">
            <h2 className="text-sm font-semibold text-slate-300 flex items-center gap-2 border-b border-white/5 pb-2">
              <Settings className="w-4 h-4 text-accentPurple" /> Pipeline Settings
            </h2>

            {/* Model Select */}
            <div className="flex flex-col gap-1.5">
              <label className="text-xs font-semibold text-slate-400 flex items-center justify-between">
                <span>LLM Generation Model</span>
                {!backendConfig.gemini_key_configured && (
                  <span className="text-[10px] text-amber-500 italic">No API Key: Simulated Answer</span>
                )}
              </label>
              <select 
                value={config.model_name}
                onChange={(e) => setConfig({ ...config, model_name: e.target.value })}
                className="w-full text-xs px-3 py-2 bg-brandDark border border-white/10 rounded-lg focus:border-accentBlue outline-none"
              >
                {backendConfig.available_models.map(m => (
                  <option key={m} value={m}>{m}</option>
                ))}
              </select>
            </div>

            {/* Retrieval Type Selection */}
            <div className="flex flex-col gap-1.5">
              <label className="text-xs font-semibold text-slate-400">Search Strategy</label>
              <div className="grid grid-cols-3 gap-1 bg-brandDark p-1 rounded-lg border border-white/5">
                {["vector", "keyword", "hybrid"].map((strategy) => (
                  <button
                    key={strategy}
                    onClick={() => setConfig({ ...config, retrieval_type: strategy })}
                    className={`py-1.5 text-[11px] font-medium rounded-md capitalize transition-all duration-150 ${
                      config.retrieval_type === strategy 
                        ? "bg-accentBlue text-white shadow-sm" 
                        : "text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    {strategy}
                  </button>
                ))}
              </div>
            </div>

            {/* Dynamic Hybrid Weights */}
            {config.retrieval_type === "hybrid" && (
              <div className="flex flex-col gap-2 p-2.5 bg-brandDark/30 border border-white/5 rounded-lg">
                <div className="flex items-center justify-between text-[11px]">
                  <span className="text-slate-400">Dense Vector Weight: {config.vector_weight}</span>
                  <span className="text-slate-400">Sparse BM25 Weight: {config.keyword_weight}</span>
                </div>
                <input 
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  value={config.vector_weight}
                  onChange={(e) => {
                    const vec = parseFloat(e.target.value);
                    setConfig({ 
                      ...config, 
                      vector_weight: vec,
                      keyword_weight: parseFloat((1.0 - vec).toFixed(1))
                    });
                  }}
                  className="w-full accent-accentBlue"
                />
              </div>
            )}

            {/* Slider Settings */}
            <div className="flex flex-col gap-3">
              {/* Top K */}
              <div>
                <div className="flex justify-between text-xs mb-1 font-semibold text-slate-400">
                  <span>Retrieve Count (Top K)</span>
                  <span className="text-accentBlue">{config.top_k} Chunks</span>
                </div>
                <input 
                  type="range"
                  min="1"
                  max="10"
                  value={config.top_k}
                  onChange={(e) => setConfig({ ...config, top_k: parseInt(e.target.value) })}
                  className="w-full accent-accentBlue"
                />
              </div>

              {/* Temperature */}
              <div>
                <div className="flex justify-between text-xs mb-1 font-semibold text-slate-400">
                  <span>LLM Temperature</span>
                  <span className="text-accentPurple">{config.temperature}</span>
                </div>
                <input 
                  type="range"
                  min="0.0"
                  max="1.0"
                  step="0.1"
                  value={config.temperature}
                  onChange={(e) => setConfig({ ...config, temperature: parseFloat(e.target.value) })}
                  className="w-full accent-accentPurple"
                />
              </div>

              {/* Ingestion Config parameters */}
              <div className="grid grid-cols-2 gap-3 border-t border-white/5 pt-3">
                <div>
                  <label className="text-[11px] font-semibold text-slate-500">Chunk Size (chars)</label>
                  <input 
                    type="number"
                    value={config.chunk_size}
                    onChange={(e) => setConfig({ ...config, chunk_size: parseInt(e.target.value) || 1000 })}
                    className="w-full mt-1 text-xs px-2.5 py-1.5 bg-brandDark border border-white/10 rounded-lg outline-none focus:border-accentBlue"
                  />
                </div>
                <div>
                  <label className="text-[11px] font-semibold text-slate-500">Chunk Overlap</label>
                  <input 
                    type="number"
                    value={config.chunk_overlap}
                    onChange={(e) => setConfig({ ...config, chunk_overlap: parseInt(e.target.value) || 200 })}
                    className="w-full mt-1 text-xs px-2.5 py-1.5 bg-brandDark border border-white/10 rounded-lg outline-none focus:border-accentBlue"
                  />
                </div>
              </div>
            </div>

            {/* Re-ranker Switch */}
            <div className="flex items-center justify-between border-t border-white/5 pt-3">
              <div className="flex flex-col">
                <span className="text-xs font-semibold text-slate-400">Enable Cross-Encoder Re-ranking</span>
                <span className="text-[10px] text-slate-500">Improves retrieval quality using semantic relevance.</span>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input 
                  type="checkbox" 
                  checked={config.use_reranker}
                  onChange={(e) => setConfig({ ...config, use_reranker: e.target.checked })}
                  className="sr-only peer"
                />
                <div className="w-9 h-5 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-accentBlue"></div>
              </label>
            </div>
          </div>
        </section>

        {/* Right Panel: Chat Space */}
        <section className="flex-1 glass-panel rounded-2xl flex flex-col overflow-hidden h-full">
          {/* Chat Header */}
          <div className="px-5 py-4 border-b border-white/5 flex items-center justify-between bg-brandDark/20">
            <div className="flex items-center gap-2">
              <MessageSquare className="w-4 h-4 text-accentBlue" />
              <h2 className="text-sm font-semibold text-slate-300">RAG Conversation Workspace</h2>
            </div>
            
            <button 
              onClick={() => setMessages([])}
              className="text-xs text-slate-500 hover:text-slate-300 transition-colors"
              disabled={messages.length === 0}
            >
              Clear Chat
            </button>
          </div>

          {/* Messages Feed */}
          <div className="flex-1 overflow-y-auto p-5 flex flex-col gap-4">
            {messages.length === 0 ? (
              <div className="flex-1 flex flex-col items-center justify-center text-center p-6 gap-3">
                <div className="p-4 bg-brandDark border border-white/5 rounded-2xl text-accentBlue/80">
                  <MessageSquare className="w-8 h-8" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-slate-200">Start Grounded Conversations</h3>
                  <p className="text-xs text-slate-400 max-w-sm mt-1">
                    Upload documents on the left and ask questions. The system will retrieve relevant excerpts to craft a grounded response.
                  </p>
                </div>
              </div>
            ) : (
              messages.map((msg, idx) => (
                <div key={idx} className={`flex flex-col ${msg.role === "user" ? "items-end" : "items-start"}`}>
                  
                  {/* Message Bubble */}
                  <div className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm shadow-sm ${
                    msg.role === "user" 
                      ? "bg-accentBlue text-white rounded-tr-none" 
                      : "bg-brandDark border border-white/5 rounded-tl-none text-slate-200"
                  }`}>
                    {/* Render message (supports basic breaks) */}
                    <div className="whitespace-pre-line leading-relaxed">{msg.text}</div>
                    
                    {msg.role === "assistant" && msg.model && (
                      <div className="text-[10px] text-slate-500 mt-2 flex items-center gap-1">
                        <Sparkles className="w-3 h-3 text-accentPurple" /> Grounded via {msg.model}
                      </div>
                    )}
                  </div>

                  {/* Sources Section for Assistant Messages */}
                  {msg.role === "assistant" && msg.sources && msg.sources.length > 0 && (
                    <div className="w-full max-w-[85%] mt-2 flex flex-col gap-1.5">
                      <div className="flex items-center gap-1.5 text-xs text-slate-400">
                        <Info className="w-3.5 h-3.5 text-accentCyan" />
                        <span className="font-medium">Retrieved Sources:</span>
                      </div>
                      
                      <div className="flex flex-wrap gap-2">
                        {msg.sources.map((src, srcIdx) => (
                          <button
                            key={srcIdx}
                            onClick={() => setActiveCitation(activeCitation?.msgIdx === idx && activeCitation?.srcIdx === srcIdx ? null : { msgIdx: idx, srcIdx, data: src })}
                            className={`text-xs px-2.5 py-1 rounded-md border flex items-center gap-1.5 transition-all duration-150 ${
                              activeCitation?.msgIdx === idx && activeCitation?.srcIdx === srcIdx
                                ? "bg-accentCyan/10 border-accentCyan text-accentCyan"
                                : "bg-brandDark/40 border-white/5 hover:border-white/10 text-slate-300"
                            }`}
                          >
                            <FileText className="w-3 h-3" />
                            <span className="max-w-[120px] truncate">{src.metadata?.source || "Source"}</span>
                            <span className="text-[10px] opacity-75 font-semibold">
                              (Score: {src.score.toFixed(2)})
                            </span>
                          </button>
                        ))}
                      </div>

                      {/* Display Active Citation Text */}
                      {activeCitation && activeCitation.msgIdx === idx && (
                        <div className="bg-brandDark/60 border border-accentCyan/20 rounded-xl p-3.5 mt-2 animate-float text-xs text-slate-300 relative">
                          <button 
                            onClick={() => setActiveCitation(null)}
                            className="absolute top-2.5 right-2.5 p-0.5 rounded-md hover:bg-white/5 text-slate-500 hover:text-slate-300"
                          >
                            <X className="w-3.5 h-3.5" />
                          </button>
                          <div className="flex items-center gap-2 mb-2 text-[10px] uppercase font-bold text-accentCyan tracking-wider">
                            <span>Excerpt from: {activeCitation.data.metadata?.source}</span>
                            {activeCitation.data.metadata?.page !== undefined && (
                              <span>• Page {activeCitation.data.metadata.page + 1}</span>
                            )}
                          </div>
                          <p className="italic leading-relaxed whitespace-pre-line bg-black/20 p-2.5 rounded-lg border border-white/5 text-slate-400">
                            "... {activeCitation.data.content} ..."
                          </p>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))
            )}

            {/* Spinner for response */}
            {loading && (
              <div className="flex items-start">
                <div className="bg-brandDark border border-white/5 rounded-2xl rounded-tl-none px-4 py-3.5 max-w-[80%] flex items-center gap-2.5 text-xs text-slate-400">
                  <RefreshCw className="w-3.5 h-3.5 animate-spin text-accentPurple" />
                  <span>Searching databases, extracting citations, and generating response...</span>
                </div>
              </div>
            )}
            
            <div ref={chatEndRef} />
          </div>

          {/* Input Box */}
          <form onSubmit={handleQuery} className="p-4 border-t border-white/5 bg-brandDark/10 flex gap-3">
            <input 
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question based on your uploaded documents..."
              className="flex-1 glass-input px-4 py-3 rounded-xl text-sm"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={!input.trim() || loading}
              className="px-4 py-3 rounded-xl bg-accentBlue text-white hover:bg-accentHover disabled:bg-slate-700 disabled:text-slate-500 font-semibold transition-all duration-150 flex items-center justify-center shrink-0"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </section>
      </main>
    </div>
  );
}

export default App;
