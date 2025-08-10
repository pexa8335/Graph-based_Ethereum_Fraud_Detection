"use client";

import React, { useState, useEffect, useRef, FormEvent } from "react";
import { Sparkles, ChevronDown, ChevronUp, Bot, Send, Paperclip, Mic, Smile } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

interface Message {
  text: string;
  sender: "user" | "bot";
}

const ACCENT_COLOR = 'cyan'; 
const BG_CARD = 'bg-slate-800';
const BG_DARK = 'bg-slate-900';
const BG_INPUT = 'bg-slate-700';
const BORDER_COLOR = 'border-slate-600';
const TEXT_COLOR_PRIMARY = 'text-slate-200';
const TEXT_COLOR_SECONDARY = 'text-slate-400';

export default function ChatbotComponent() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    { text: "Hello! I am the Aegis Assistant. How can I help you today?", sender: "bot" }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [thinkingProcess, setThinkingProcess] = useState('');
  const [showThinkingProcess, setShowThinkingProcess] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const FASTAPI_BASE_URL = process.env.NEXT_PUBLIC_FASTAPI_BASE_URL || "http://localhost:8000";

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, thinkingProcess]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { text: input, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);
    const currentInput = input;
    setInput("");
    setIsLoading(true);
    setError(''); 
    setThinkingProcess('');

    try {
      const response = await fetch(`${FASTAPI_BASE_URL}/api/v1/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: currentInput }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || errorData.error || "Failed to get response from server.");
      }

      const data = await response.json();
      const botMessage: Message = { text: data.answer, sender: "bot" };
      setMessages((prev) => [...prev, botMessage]);
      setThinkingProcess(data.thinking_steps || '');

    } catch (error: any) {
      console.error("Chatbot Error:", error);
      const errorMessage: Message = {
        text: "Xin lỗi, tôi đang gặp sự cố kết nối. Vui lòng thử lại sau.",
        sender: "bot",
      };
      setMessages((prev) => [...prev, errorMessage]);
      setError(error.message || "Không thể kết nối đến máy chủ chatbot.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`w-96 h-[70vh] flex flex-col ${BG_CARD} ${BORDER_COLOR} border rounded-lg shadow-2xl animate-fade-in-up`}>
      {/* Header */}
      <div className={`flex justify-between items-center p-3 ${BG_DARK} ${BORDER_COLOR} border-b rounded-t-lg`}>
        <h3 className={`text-white font-semibold flex items-center gap-2`}>
          <Bot size={20} className={`text-${ACCENT_COLOR}-400`}/>
          Aegis Assistant
        </h3>
      </div>

      {/* Khu vực điều khiển Thoughts */}
      <div className={`flex items-center justify-between p-3 ${BORDER_COLOR} border-b flex-shrink-0`}>
          <button
              onClick={() => setShowThinkingProcess(!showThinkingProcess)}
              className={`flex items-center gap-2 px-3 py-1 bg-slate-700 hover:bg-slate-600 ${TEXT_COLOR_SECONDARY} text-sm rounded-full focus:outline-none`}
          >
              <Sparkles size={16} className={`text-${ACCENT_COLOR}-400`} />
              Thoughts <span className="text-xs text-slate-400">(experimental)</span>
              {showThinkingProcess ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </button>
          {/* Bạn có thể thêm nút "Auto" nếu muốn, hiện tại không có chức năng */}
          <button className={`flex items-center gap-1 text-sm ${TEXT_COLOR_SECONDARY}`}>
              Auto <ChevronDown size={16} />
          </button>
      </div>

      {/* Khu vực hiển thị luồng suy nghĩ */}
      {showThinkingProcess && (
          <div className={`p-3 text-sm bg-slate-900 ${TEXT_COLOR_SECONDARY} overflow-y-auto max-h-40 ${BORDER_COLOR} border-b relative flex-shrink-0`}>
              <div id="thinking-log" className="prose prose-sm max-w-none prose-invert" 
                   dangerouslySetInnerHTML={{ __html: thinkingProcess || 'Chưa có bước suy nghĩ nào.' }}></div>
          </div>
      )}

      {/* Chatbot Body */}
      <div id="chat-messages-container" className="flex-1 p-4 overflow-y-auto space-y-4">
        {messages.map((msg, index) => (
          <div key={index} className={`flex items-end gap-2 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            {msg.sender === 'bot' && (
              <div className="w-8 h-8 rounded-full flex-shrink-0 bg-slate-700 flex items-center justify-center">
                <Bot size={20} className={`text-${ACCENT_COLOR}-400`} />
              </div>
            )}
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg prose prose-sm prose-p:my-1 prose-ul:my-1 prose-ol:my-1 text-inherit prose-invert ${
                msg.sender === 'user'
                  ? `bg-${ACCENT_COLOR}-500 text-white rounded-br-none`
                  : `${BG_INPUT} ${TEXT_COLOR_PRIMARY} rounded-bl-none`
              }`}
            > 
              <ReactMarkdown>{msg.text}</ReactMarkdown>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
              <div className={`${BG_INPUT} ${TEXT_COLOR_SECONDARY} px-4 py-2 rounded-lg rounded-bl-none`}>
                  <span className="animate-pulse">Typing...</span>
              </div>
          </div>
        )}
        {error && <div className={`text-center text-red-400 text-sm py-2`}>{error}</div>}
        <div ref={messagesEndRef} />
      </div>

      {/* Chatbot Footer */}
      <form onSubmit={handleSubmit} className={`p-3 flex items-center ${BORDER_COLOR} border-t ${BG_DARK} rounded-b-lg flex-shrink-0`}>
        <div className={`flex items-center gap-2 rounded-xl p-1 ${BORDER_COLOR} border focus-within:ring-2 focus-within:ring-${ACCENT_COLOR}-500 flex-1`}>
            {/* Các nút chức năng thêm (hiện tại không có chức năng) */}
            <button type="button" className={`p-2 ${TEXT_COLOR_SECONDARY} hover:text-${ACCENT_COLOR}-400`}><Smile size={20} /></button>
            <button type="button" className={`p-2 ${TEXT_COLOR_SECONDARY} hover:text-${ACCENT_COLOR}-400`}><Paperclip size={20} /></button>
            
            <textarea
                placeholder="Ask about financial risk..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) handleSubmit(e); }}
                className={`flex-grow resize-none bg-transparent focus:outline-none text-sm p-1 max-h-24 text-white placeholder-slate-400`}
                rows={1}
                disabled={isLoading}
            />
            <button type="button" className={`p-2 ${TEXT_COLOR_SECONDARY} hover:text-${ACCENT_COLOR}-400`}><Mic size={20} /></button>
        </div>
        <button type="submit" className={`ml-3 p-2.5 bg-${ACCENT_COLOR}-500 rounded-full text-white hover:bg-${ACCENT_COLOR}-600 disabled:bg-slate-500 disabled:cursor-not-allowed transition-all`} disabled={isLoading || !input.trim()}>
          <Send size={18}/>
        </button>
      </form>
    </div>
  );
}