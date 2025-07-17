import { 
    Cpu,          
    Server,      
    Laptop,       
    User,        
    ArrowRight,   
    Workflow      
} from 'lucide-react';

export default function DocsPage() {
    const flowSteps = [
        {
            step: 1,
            title: "Initialize Request",
            actor: "User (Frontend)",
            icon: <User className="h-8 w-8 text-cyan-400" />,
            description: "The user enters a wallet address, TxHash, or ENS name into the search bar and clicks 'Analyze'."
        },
        {
            step: 2,
            title: "Internal API Call",
            actor: "Frontend → Backend",
            icon: <Laptop className="h-8 w-8 text-cyan-400" />,
            description: "The interface (Next.js Client Component) sends a POST request to a secure proxy endpoint at `/api/analysis`."
        },
        {
            step: 3,
            title: "Data Collection & Processing",
            actor: "Backend (Next.js Server)",
            icon: <Server className="h-8 w-8 text-cyan-400" />,
            description: "The Next.js server receives the request, then calls Covalent's API to fetch raw on-chain data and processes it to generate 50 distinctive features."
        },
        {
            step: 4,
            title: "Prediction via AI",
            actor: "Backend → AI Model",
            icon: <Cpu className="h-8 w-8 text-cyan-400" />,
            description: "The 50 processed features are sent to an AI Model via a Flask API at `/predict` to receive a risk score and confidence level."
        },
        {
            step: 5,
            title: "Display Results",
            actor: "Backend → Frontend",
            icon: <Laptop className="h-8 w-8 text-cyan-400" />,
            description: "The prediction results are returned to the frontend and visually displayed via Gauge Charts, Risk Factor Lists, and Network Graphs."
        }
    ];

    return (
        <main className="p-4 sm:p-6 lg:p-8 bg-slate-900 text-white min-h-screen">
            <div className="max-w-4xl mx-auto">
                <h1 className="text-4xl font-bold text-center mb-4">How does NovaLedger work?</h1>
                <p className="text-lg text-slate-400 text-center mb-12">
                    Learn about the architecture and end-to-end data flow of our intelligent on-chain analysis platform.
                </p>
                <div className="mb-16">
                    <div className="flex flex-col sm:flex-row items-center justify-center gap-2 text-center text-xs sm:text-sm">
                        <div className="flex flex-col items-center p-3 bg-slate-800 rounded-lg border border-slate-700 w-24 sm:w-auto">
                            <User className="h-6 w-6 mb-1 text-cyan-400"/><span>User</span>
                        </div>
                        <ArrowRight className="h-6 w-6 text-slate-500 rotate-90 sm:rotate-0" />
                        <div className="flex flex-col items-center p-3 bg-slate-800 rounded-lg border border-slate-700 w-24 sm:w-auto">
                            <Laptop className="h-6 w-6 mb-1 text-cyan-400"/><span>Frontend</span>
                        </div>
                        <ArrowRight className="h-6 w-6 text-slate-500 rotate-90 sm:rotate-0" />
                        <div className="flex flex-col items-center p-3 bg-slate-800 rounded-lg border border-slate-700 w-24 sm:w-auto">
                            <Server className="h-6 w-6 mb-1 text-cyan-400"/><span>Backend</span>
                        </div>
                        <ArrowRight className="h-6 w-6 text-slate-500 rotate-90 sm:rotate-0" />
                        <div className="flex flex-col items-center p-3 bg-slate-800 rounded-lg border border-slate-700 w-24 sm:w-auto">
                            <Cpu className="h-6 w-6 mb-1 text-cyan-400"/><span>AI Model</span>
                        </div>
                    </div>
                </div>
                <div className="bg-slate-800 border border-slate-700 rounded-lg p-6 sm:p-8">
                    <h2 className="text-2xl font-semibold mb-6 flex items-center gap-3">
                        <Workflow className="text-cyan-400" />
                        Detailed Workflow
                    </h2>
                    <div className="relative border-l-2 border-slate-600 pl-8">
                        {flowSteps.map((item, index) => (
                            <div key={item.step} className={`relative pb-10 ${index === flowSteps.length - 1 ? 'pb-0' : ''}`}>
                                <div className="absolute -left-[17px] top-0 h-8 w-8 bg-cyan-500 rounded-full flex items-center justify-center font-bold text-black">
                                    {item.step}
                                </div>
                                <div className="ml-4">
                                    <h3 className="text-lg font-semibold text-white">{item.title}</h3>
                                    <p className="text-sm text-slate-400 mb-2">{item.actor}</p>
                                    <p className="text-slate-300">{item.description}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </main>
    );
}
