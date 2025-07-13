export interface CovalentTransaction {
  tx_hash?: string;
  block_signed_at: string;
  from_address: string;
  to_address: string | null;
  to_address_is_contract?: boolean;
  value: string;
  log_events?: any[];
}

export interface BalanceItem {
  native_token: boolean;
  balance: string;
  contract_decimals: number;
}

export interface WalletFeatures {
  Index: number;
  Address?: string; 
  FLAG: number; 

  'Time Diff between first and last (Mins)': number;
  'Avg min between sent tnx': number;
  'Avg min between received tnx': number;
  
  'Sent tnx': number;
  'Received Tnx': number;
  'Number of Created Contracts': number;
  'Unique Received From Addresses': number;
  'Unique Sent To Addresses': number;
  'total transactions (including tnx to create contract': number;
  
  'min value received': number;
  'max value received': number;
  'avg val received': number;
  'min val sent': number;
  'max val sent': number;
  'avg val sent': number;
  'min value sent to contract': number;
  'max val sent to contract': number;
  'avg value sent to contract': number;
  'total Ether sent': number;
  'total ether received': number;
  'total ether sent contracts': number;
  'total ether balance': number;

  'Total ERC20 tnxs': number;
  'ERC20 total Ether received': number;
  'ERC20 total ether sent': number;
  'ERC20 total Ether sent contract': number;
  'ERC20 uniq sent addr': number;
  'ERC20 uniq rec addr': number;
  'ERC20 uniq sent addr.1': number; 
  'ERC20 uniq rec contract addr': number;
  'ERC20 avg time between sent tnx': number;
  'ERC20 avg time between rec tnx': number;
  'ERC20 avg time between rec 2 tnx': number;
  'ERC20 avg time between contract tnx': number;
  'ERC20 min val rec': number;
  'ERC20 max val rec': number;
  'ERC20 avg val rec': number;
  'ERC20 min val sent': number;
  'ERC20 max val sent': number;
  'ERC20 avg val sent': number;
  'ERC20 min val sent contract': number;
  'ERC20 max val sent contract': number;
  'ERC20 avg val sent contract': number;
  'ERC20 uniq sent token name': number;
  'ERC20 uniq rec token name': number;
  'ERC20 most sent token type': string | null;
  'ERC20_most_rec_token_type': string | null;
  'ERC20 most sent token type_label': number | null; 
  'ERC20_most_rec_token_type_label': number | null; 
}

export interface AnalysisApiResponse {
  address: string; 
  prediction: 'Fraud' | 'Non-Fraud' | null; 
  probability_fraud: number | null; 

  features: WalletFeatures; 
  lime_explanation: Array<[string, number]>;
  shap_force_plot_base64: string; 
  shap_values: { [key: string]: number }; 
}