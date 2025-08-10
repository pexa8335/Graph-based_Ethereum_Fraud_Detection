import { AnalysisApiResponse } from "@/types/analysis";

export interface WalletAnalysisResult extends AnalysisApiResponse {
  isLoading: boolean;
  error: string | null;
}