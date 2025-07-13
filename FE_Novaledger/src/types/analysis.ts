
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
  index: number;
  address: string;
  flag: number; 

  timeDiffBetweenFirstAndLastMins: number;
  avgMinBetweenSentTnx: number;
  avgMinBetweenReceivedTnx: number;
  
  sentTnx: number;
  receivedTnx: number;
  createdContractsCount: number;
  uniqueReceivedFromAddresses: number;
  uniqueSentToAddresses: number;
  totalTransactions: number;

  minValueReceived: number;
  maxValueReceived: number;
  avgValueReceived: number;
  minValueSent: number;
  maxValueSent: number;
  avgValueSent: number;
  minValueSentToContract: number;
  maxValueSentToContract: number;
  avgValueSentToContract: number;
  totalEtherSent: number;
  totalEtherReceived: number;
  totalEtherSentToContracts: number;
  totalEtherBalance: number;

  totalErc20Tnxs: number;
  erc20TotalEtherReceived: number;
  erc20TotalEtherSent: number;
  erc20TotalEtherSentContract: number;
  erc20UniqSentAddr: number;
  erc20UniqRecAddr: number;
  erc20UniqSentAddr1: number; 
  erc20UniqRecContractAddr: number;
  erc20AvgTimeBetweenSentTnx: number;
  erc20AvgTimeBetweenRecTnx: number;
  erc20AvgTimeBetweenRec2Tnx: number;
  erc20AvgTimeBetweenContractTnx: number;
  erc20MinValueRec: number;
  erc20MaxValueRec: number;
  erc20AvgValueRec: number;
  erc20MinValueSent: number;
  erc20MaxValueSent: number;
  erc20AvgValueSent: number;
  erc20MinValueSentContract: number;
  erc20MaxValueSentContract: number;
  erc20AvgValueSentContract: number;
  erc20UniqSentTokenName: number;
  erc20UniqRecTokenName: number;
  erc20MostSentTokenType: string | null;
  erc20MostRecTokenType: string | null;
}
export interface AnalysisApiResponse {
  prediction: 'Fraud' | 'Non-Fraud' | number;
  probability_fraud?: number;
  confidence?: number;
  features: WalletFeatures; 
  explanation: Array<[string, number]>;
}