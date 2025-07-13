'use client';
const MOCK_CHART_DATA = [
  { month: 'Jan', high: 12, medium: 5 },
  { month: 'Feb', high: 19, medium: 7 },
  { month: 'Mar', high: 15, medium: 10 },
  { month: 'Apr', high: 28, medium: 15 },
  { month: 'May', high: 22, medium: 18 },
  { month: 'Jun', high: 35, medium: 25 },
];

export default function LineChartClient() {
  return (
    <div className="h-full w-full flex flex-col justify-between">
      {/* Phần thân biểu đồ */}
      <div className="relative flex-grow">
        {/* Đường kẻ ngang */}
        <div className="absolute top-1/4 left-0 right-0 h-px bg-slate-700 border-b border-dashed border-slate-600"></div>
        <div className="absolute top-2/4 left-0 right-0 h-px bg-slate-700 border-b border-dashed border-slate-600"></div>
        <div className="absolute top-3/4 left-0 right-0 h-px bg-slate-700 border-b border-dashed border-slate-600"></div>

        {/* SVG để vẽ các đường cong */}
        <svg className="absolute inset-0 w-full h-full" width="100%" height="100%">
          <defs>
            <linearGradient id="highRiskGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#ef4444" stopOpacity="0.3"/>
              <stop offset="100%" stopColor="#ef4444" stopOpacity="0"/>
            </linearGradient>
            <linearGradient id="mediumRiskGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.3"/>
              <stop offset="100%" stopColor="#f59e0b" stopOpacity="0"/>
            </linearGradient>
          </defs>
          {/* Đường "Rủi ro cao" */}
          <path d="M0,80 C50,60 150,20 200,40 S300,80 350,60 S450,40 500,50" 
                stroke="#ef4444" fill="url(#highRiskGradient)" strokeWidth="2" />
          {/* Đường "Cần xem xét" */}
          <path d="M0,90 C50,80 150,70 200,85 S300,95 350,80 S450,70 500,75" 
                stroke="#f59e0b" fill="url(#mediumRiskGradient)" strokeWidth="2" />
        </svg>
      </div>

      {/* Chú thích trục X (Tháng) */}
      <div className="flex justify-between text-xs text-slate-500 pt-2 border-t border-slate-700">
        {MOCK_CHART_DATA.map(d => <span key={d.month}>{d.month}</span>)}
      </div>
    </div>
  );
}