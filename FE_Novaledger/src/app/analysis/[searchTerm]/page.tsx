import {
  fetchAnalysisData,
} from "@/services/analysisService";
import { SummaryPanel, StatsPanel } from "@/components/analysis/AnalysisPanels";
import { GraphDisplay } from "@/components/analysis/GraphDisplay";
import { AnalysisApiResponse } from "@/types/analysis";

export default async function AnalysisPage({
  params,
}: {
  params: { searchTerm: string };
}) {
  const address = params.searchTerm;
  let analysisResult: AnalysisApiResponse | null = null;
  let error: string | null = null;

  try {
    analysisResult = await fetchAnalysisData(address);
  } catch (e: any) {
    error = e.message || "An unknown error occurred.";
  }

  if (error || !analysisResult) {
    return (
      <div className="p-8 text-white text-center">
        <h1 className="text-2xl font-bold text-red-400">Analysis Failed</h1>
        <p className="text-slate-400 mt-2">{error || "No data received."}</p>
      </div>
    );
  }

  return (
    <div className="p-4 md:p-8 text-white">
      <div className="max-w-7xl mx-auto space-y-8">
        <div>
          <p className="text-sm text-gray-400">Analysis result for address</p>
          <h1 className="text-2xl md:text-3xl font-mono break-all text-cyan-300">
            {address}
          </h1>
        </div>
        <SummaryPanel result={analysisResult} />
        {analysisResult.feature_importance && (
          <StatsPanel features={analysisResult.feature_importance} />
        )}
        <GraphDisplay address={address} />
      </div>
    </div>
  );
}