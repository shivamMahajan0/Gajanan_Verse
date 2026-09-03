import React, { useState, useRef, useEffect } from 'react';
import { Moon, Sun, Send, MessageCircle, Info, BookOpen, User, AlignRight, Globe, Loader } from 'lucide-react';

export default function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'system',
      text: 'Welcome to the Spiritual Guide\nI am here to offer calm, respectful, and meaningful guidance drawn entirely from the verses of Shri Gajanan Vijay. How may I assist you today?',
      verses: []
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(true);
  
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  useEffect(() => {
    if (isDarkMode) {
      document.body.classList.remove('light-mode');
    } else {
      document.body.classList.add('light-mode');
    }
  }, [isDarkMode]);

  const handleSuggestionClick = (query) => {
    setInputValue(query);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userQuery = inputValue.trim();
    setInputValue('');
    
    // Add user message
    setMessages(prev => [...prev, { id: Date.now(), role: 'user', text: userQuery, verses: [] }]);
    setIsLoading(true);

    try {
      // Connect to FastAPI backend
      const response = await fetch('https://gajanan-verse-ptlh.onrender.com/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userQuery })
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setMessages(prev => [...prev, { id: Date.now(), role: 'system', text: data.answer, verses: data.verses }]);
    } catch (error) {
      console.error('Error fetching chat:', error);
      setMessages(prev => [...prev, { id: Date.now(), role: 'system', text: 'Sorry, I encountered an error. Ensure the FastAPI backend is running.', verses: [] }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Helper to parse basic markdown inside the text
  const formatText = (text) => {
    return text.split('\n').filter(p => p.trim() !== '').map((para, idx) => {
      // Split by ** for bold
      const parts = para.split(/(\*\*.*?\*\*)/g);
      return (
        <p key={idx}>
          {parts.map((p, i) => {
            if (p.startsWith('**') && p.endsWith('**')) {
              return <strong key={i}>{p.slice(2, -2)}</strong>;
            }
            return p;
          })}
        </p>
      );
    });
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <h2>Spiritual Guide</h2>
          <p>Shri Gajanan Vijay</p>
        </div>
        
        <div className="sidebar-menu">
          <button className="menu-btn active">
            <MessageCircle size={18} /> Chat Guide
          </button>
          
          <div className="suggested-queries">
            <h3>SUGGESTED QUERIES</h3>
            {[
              "I have low knowledge",
              "Give me a verse about hope",
              "I feel low energytic",
              "Guidance for a new task"
            ].map((query, i) => (
              <button 
                key={i} 
                className="suggestion-chip"
                onClick={() => handleSuggestionClick(query)}
              >
                {query}
              </button>
            ))}
          </div>
        </div>
        
        <div className="sidebar-footer">
          <p>Rooted exclusively in the structured JSON dataset.</p>
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="chat-area">
        <header className="chat-header">
          <div className="header-info">
            <h1>Conversational AI</h1>
            <span className="status-badge"><span className="dot online"></span> Production Mode</span>
          </div>
          <button 
            className="icon-btn" 
            onClick={() => setIsDarkMode(!isDarkMode)}
            aria-label="Toggle Dark Mode"
          >
            {isDarkMode ? <Sun size={20} /> : <Moon size={20} />}
          </button>
        </header>

        <div className="chat-window">
          {messages.map((msg) => (
            <div key={msg.id} className={`message ${msg.role}-message`}>
              <div className="message-avatar">
                {msg.role === 'user' ? <User size={20} /> : <BookOpen size={20} />}
              </div>
              <div className="message-content">
                <div style={{ fontSize: '1.1rem', fontWeight: msg.role === 'system' ? '500' : '400', lineHeight: '1.7' }}>
                  {formatText(msg.text)}
                </div>

                {msg.verses && msg.verses.length > 0 && (
                  <div className="sources-list" style={{ marginTop: '24px' }}>
                    <h3 style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '16px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Retrieved Context</h3>
                    {msg.verses.map((src, idx) => (
                      <div key={idx} className="source-card">
                        <div className="source-header">
                            <span className="verse-id">Verse {src.verse_id}</span>
                            <span className="adhyaya-badge">Adhyaya {src.adhyaya}</span>
                        </div>
                        <div className="source-body">
                            <div className="text-section marathi-text">
                                <h4><AlignRight size={14} /> Marathi</h4>
                                <p>{src.marathi || 'N/A'}</p>
                            </div>
                            <div className="text-section english-text">
                                <h4><Globe size={14} /> English</h4>
                                <p>{src.english || 'N/A'}</p>
                            </div>
                            {src.teaching && (
                              <div className="text-section teaching-text">
                                  <h4><Info size={14} /> Teaching Summary</h4>
                                  <p>{src.teaching}</p>
                              </div>
                            )}
                        </div>
                        {src.themes && (
                            <div className="source-footer">
                                <span className="tag-label">Themes:</span>
                                <div className="themes-container">
                                    {src.themes.split(',').map((t, i) => t.trim() ? (
                                        <span key={i} className="theme-tag">{t.trim()}</span>
                                    ) : null)}
                                </div>
                            </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="message system-message">
              <div className="message-avatar">
                <Loader size={20} style={{ animation: 'spin 2s linear infinite' }} />
              </div>
              <div className="message-content">
                  <div className="typing-indicator">
                      <div className="typing-dot"></div>
                      <div className="typing-dot"></div>
                      <div className="typing-dot"></div>
                  </div>
              </div>
            </div>
          )}
          
          <div ref={chatEndRef} />
        </div>

        <div className="input-container">
          <form className="chat-form" onSubmit={handleSubmit}>
            <div className="input-wrapper">
              <input 
                type="text" 
                className="chat-input" 
                placeholder="Ask a question or request a verse..." 
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                disabled={isLoading}
              />
              <button type="submit" className="send-btn" disabled={isLoading || !inputValue.trim()}>
                <Send size={18} />
              </button>
            </div>
          </form>
          <div className="input-footer">
              Retrieval Augmented Generation (RAG) System Powered by ChromaDB & OpenRouter.
          </div>
        </div>
      </main>
    </div>
  );
}
