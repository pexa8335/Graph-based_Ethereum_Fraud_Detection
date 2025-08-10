'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { 
  Search, 
  Blocks, 
  Gauge,  
  Zap,  
  Loader2 
} from 'lucide-react'; 

export default function OnchainDashboardPage() {
  const router = useRouter();
  const [searchTerm, setSearchTerm] = useState('');
  const [isLoading, setIsLoading] = useState(false); 

  const networkStats = [
    { label: 'Latest Block', value: '19,234,567', icon: <Blocks className="text-cyan-400" size={24} /> },
    { label: 'Gas Price (Gwei)', value: '25', icon: <Gauge className="text-purple-400" size={24} /> },
    { label: 'Transactions / sec', value: '15', icon: <Zap className="h-6 w-6 text-green-400" size={24} /> },
  ];

  const handleAnalysis = async (e: React.FormEvent) => { 
    e.preventDefault();
    if (!searchTerm.trim()) return;

    setIsLoading(true); 
    
    try {
      await new Promise(resolve => setTimeout(resolve, 800));
      
      router.push(`/analysis/${searchTerm.trim()}`);
    } finally {
    }
  };

  return (
    <div
      className="relative min-h-screen w-full bg-cover bg-center flex flex-col items-center justify-center p-4 sm:p-10"
      style={{ backgroundImage: "url('/background.png')" }}
    >
      <div className="absolute inset-0 bg-black/70 z-0"></div>
      
      <div className="relative z-10 w-full max-w-3xl text-center">
        <h1 
          className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-4"
          style={{ textShadow: '0 3px 15px rgba(0, 255, 255, 0.3)' }}
        >
          Aegis Intelligence On-chain 
        </h1>
        
        <p className="text-lg text-slate-300 mb-12">
          Analyze any Wallet Address, Transaction, or Smart Contract on the Ethereum network.
        </p>
        <form onSubmit={handleAnalysis} className="w-full max-w-2xl mx-auto">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <Search className="text-slate-400" />
            </div>
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Enter address, TxHash, or ENS name..."
              className="w-full p-4 pl-12 pr-32 rounded-full text-lg 
                         bg-slate-800/70 border-2 border-slate-600 
                         text-white placeholder-slate-400
                         focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-cyan-400
                         transition-all duration-300"
              disabled={isLoading} 
            />
            <button
              type="submit"
              className="absolute inset-y-0 right-0 m-2 px-6 py-2 rounded-full font-semibold
                         bg-cyan-500 text-black
                         hover:bg-cyan-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-800 focus:ring-cyan-500
                         transition-colors duration-300
                         flex items-center justify-center gap-2" 
              disabled={isLoading} 
            >
              {isLoading ? ( 
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                'Analyze'
              )}
            </button>
          </div>
        </form>
      </div>
      <div className="absolute bottom-10 z-10 w-full max-w-5xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {networkStats.map((stat) => (
            <div 
              key={stat.label}
              className="bg-white/5 backdrop-blur-md border border-white/10 rounded-xl p-4 flex items-center gap-4"
            >
              {stat.icon}
              <div>
                <p className="text-slate-400 text-sm">{stat.label}</p>
                <p className="text-xl font-semibold text-white">{stat.value}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
