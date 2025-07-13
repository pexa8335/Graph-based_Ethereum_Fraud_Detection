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
            title: "Khởi tạo Yêu cầu",
            actor: "Người dùng (Frontend)",
            icon: <User className="h-8 w-8 text-cyan-400" />,
            description: "Người dùng nhập một địa chỉ ví, TxHash, hoặc tên miền ENS vào thanh tìm kiếm và nhấn 'Phân tích'."
        },
        {
            step: 2,
            title: "Gọi API Nội bộ",
            actor: "Frontend → Backend",
            icon: <Laptop className="h-8 w-8 text-cyan-400" />,
            description: "Giao diện (Next.js Client Component) gửi một yêu cầu POST đến trạm trung chuyển an toàn tại địa chỉ `/api/analysis`."
        },
        {
            step: 3,
            title: "Thu thập & Xử lý Dữ liệu",
            actor: "Backend (Next.js Server)",
            icon: <Server className="h-8 w-8 text-cyan-400" />,
            description: "Server Next.js nhận yêu cầu, sau đó gọi API của Covalent để lấy dữ liệu on-chain thô và xử lý để tạo ra 50 feature đặc trưng."
        },
        {
            step: 4,
            title: "Dự đoán bằng AI",
            actor: "Backend → AI Model",
            icon: <Cpu className="h-8 w-8 text-cyan-400" />,
            description: "50 feature đã xử lý được gửi đến Model AI thông qua API Flask tại `/predict` để nhận về điểm số và độ tin cậy của dự đoán."
        },
        {
            step: 5,
            title: "Hiển thị Kết quả",
            actor: "Backend → Frontend",
            icon: <Laptop className="h-8 w-8 text-cyan-400" />,
            description: "Kết quả dự đoán được trả về cho giao diện, sau đó được hiển thị một cách trực quan qua Biểu đồ Gauge, Danh sách yếu tố rủi ro và Sơ đồ mạng lưới."
        }
    ];

    return (
        <main className="p-4 sm:p-6 lg:p-8 bg-slate-900 text-white min-h-screen">
            <div className="max-w-4xl mx-auto">
                <h1 className="text-4xl font-bold text-center mb-4">NovaLedger hoạt động như thế nào?</h1>
                <p className="text-lg text-slate-400 text-center mb-12">
                    Tìm hiểu về kiến trúc và luồng dữ liệu end-to-end của nền tảng phân tích on-chain thông minh.
                </p>
                <div className="mb-16">
                    <div className="flex flex-col sm:flex-row items-center justify-center gap-2 text-center text-xs sm:text-sm">
                        <div className="flex flex-col items-center p-3 bg-slate-800 rounded-lg border border-slate-700 w-24 sm:w-auto">
                            <User className="h-6 w-6 mb-1 text-cyan-400"/><span>Người dùng</span>
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
                        Luồng hoạt động chi tiết
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