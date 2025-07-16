// src/components/ChatbotWidget.tsx

"use client";
import { useState, FormEvent, useRef, useEffect } from "react";
import { MessageSquare, X, Send, Bot } from 'lucide-react'; 
import ReactMarkdown from 'react-markdown'; // <--- (1) IMPORT THÊM DÒNG NÀY

interface Message {
  text: string;
  sender: "user" | "bot";
}

export default function ChatbotWidget() {
  // ... (toàn bộ phần logic của bạn giữ nguyên, không cần thay đổi)
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    { text: "Hello! I am the Nova Assistant. How can I help you today?", sender: "bot" }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    const userMessage: Message = { text: input, sender: "user" };
    const currentHistory = messages.map(msg => ({
      role: msg.sender === 'user' ? 'user' : 'model',
      parts: [{ text: msg.text }],
    }));
    setMessages((prev) => [...prev, userMessage]);
    const currentInput = input;
    setInput("");
    setIsLoading(true);
    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: currentInput, history: currentHistory }),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to get response from server.");
      }
      const data = await response.json();
      const botMessage: Message = { text: data.reply, sender: "bot" };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Chatbot Error:", error);
      const errorMessage: Message = {
        text: "Sorry, I'm having trouble connecting. Please try again later.",
        sender: "bot",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };
  return (
    <div className="fixed bottom-5 right-5 z-50">
      {isOpen && (
        <div className="w-96 h-[70vh] flex flex-col bg-slate-800 border border-slate-600 rounded-lg shadow-2xl animate-fade-in-up">
          <div className="flex justify-between items-center p-3 bg-slate-900 border-b border-slate-600 rounded-t-lg">
            <h3 className="text-white font-semibold flex items-center gap-2">
              <Bot size={20} className="text-cyan-400"/>
              Nova Assistant
            </h3>
            <button onClick={() => setIsOpen(false)} className="text-slate-400 hover:text-white">
              <X size={20} />
            </button>
          </div>
          <div className="flex-1 p-4 overflow-y-auto space-y-4">
            {messages.map((msg, index) => (
              <div key={index} className={`flex items-end gap-2 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div
                  className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                    msg.sender === 'user' 
                      ? 'bg-cyan-500 text-white rounded-br-none' 
                      : 'bg-slate-700 text-slate-200 rounded-bl-none'
                  }`}
                >
                  {msg.sender === 'bot' ? (
                    <ReactMarkdown>{msg.text}</ReactMarkdown>
                  ) : (
                    <p className="whitespace-pre-wrap">{msg.text}</p>
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                  <div className="bg-slate-700 text-slate-400 px-4 py-2 rounded-lg rounded-bl-none">
                      <span className="animate-pulse">Typing...</span>
                  </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <form onSubmit={handleSubmit} className="p-3 flex items-center border-t border-slate-600 bg-slate-900 rounded-b-lg">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about financial risk..."
              className="flex-1 bg-slate-700 border border-slate-600 rounded-full py-2 px-4 text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
              disabled={isLoading}
            />
            <button type="submit" className="ml-3 p-2.5 bg-cyan-500 rounded-full text-white hover:bg-cyan-600 disabled:bg-slate-500 disabled:cursor-not-allowed transition-all" disabled={isLoading || !input.trim()}>
              <Send size={18}/>
            </button>
          </form>
        </div>
      )}
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="p-4 bg-cyan-500 rounded-full text-white shadow-lg hover:bg-cyan-600 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:ring-offset-2 focus:ring-offset-slate-900 transform transition-transform hover:scale-110"
        aria-label="Toggle Chat"
      >
        {isOpen ? <X size={24} /> : <MessageSquare size={24} />}
      </button>
    </div>
  );
}