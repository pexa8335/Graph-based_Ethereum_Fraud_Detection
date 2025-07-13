import { fetchAnalysisData, AnalysisResult } from '@/services/analysisService';
import { SummaryPanel, StatsPanel } from '@/components/analysis/AnalysisPanels';


export default async function AnalysisPage({ params }: { params: { searchTerm: string } }) {
  const address = params.searchTerm;
  let analysisResult: AnalysisResult | null = null;
  let error: string | null = null;

  try {
    analysisResult = await fetchAnalysisData(address);
  } catch (e: any) {
    error = e.message || 'Có lỗi không xác định xảy ra.';
  }
  if (error || !analysisResult) {
    return (
        <div className="p-8 text-white text-center">
            <h1 className="text-2xl font-bold text-red-400">Phân tích thất bại</h1>
            <p className="text-slate-400 mt-2">{error || 'Không nhận được dữ liệu.'}</p>
        </div>
    );
  }
  return (
    <div className="p-4 md:p-8 text-white">
      <div className="max-w-7xl mx-auto space-y-8">
        <div>
          <p className="text-sm text-gray-400">Kết quả phân tích cho ví</p>
          <h1 className="text-2xl md:text-3xl font-mono break-all text-cyan-300">{address}</h1>
        </div>
        <SummaryPanel result={analysisResult} />
        <StatsPanel features={analysisResult.features} />

      </div>
    </div>
  );
}