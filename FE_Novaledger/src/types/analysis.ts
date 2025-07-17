export interface AnalysisApiResponse {
  address: string;
  prediction?: 'Fraud' | 'Non-Fraud' | null;
  probability_fraud?: number | null;
  lime_explanation?: Array<[string, number]>;
  shap_values?: { [key: string]: number };
}