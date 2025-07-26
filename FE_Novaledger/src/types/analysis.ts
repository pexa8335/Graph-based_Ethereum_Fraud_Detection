export interface CovalentTransaction {
  tx_hash?: string;
  block_signed_at: string;
  from_address: string;
  to_address: string | null;
  to_address_is_contract?: boolean;
  value: string;
  log_events?: any[];
}
export interface AnalysisApiResponse {
  address: string;
  prediction?: 'Fraud' | 'Non-Fraud' | null;
  probability_fraud?: number | null;
  lime_explanation?: Array<[string, number]>;
  shap_values?: { [key: string]: number };
}