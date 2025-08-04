"use client";

import { useState } from "react";
import { MessageSquare, X } from 'lucide-react';
import ChatbotComponent from "./ChatbotComponent";


export default function ChatbotWidget() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="fixed bottom-5 right-5 z-50">
      {isOpen && (
        <div className="animate-fade-in-up">
          <ChatbotComponent />
          <button 
            onClick={() => setIsOpen(false)} 
            className="absolute top-3 right-3 text-slate-400 hover:text-white z-10" // Đảm bảo nút X nằm trên cùng
            aria-label="Close Chat"
          >
            <X size={20} />
          </button>
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