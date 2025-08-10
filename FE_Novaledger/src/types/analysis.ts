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
  status?: string; 
  percent?: number; 
  confidence_score?: number; 
  explanation?: string;
  feature_importance?: { [key: string]: number }; 
  prediction?: 'Fraud' | 'Non-Fraud' | null;
  probability_fraud?: number | null; 
}
export interface FeatureCardProps {
  label: string;
  featureKey: string;
  value: any;
}