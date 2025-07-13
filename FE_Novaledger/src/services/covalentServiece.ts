import axios from 'axios';
import { Buffer } from 'buffer';
import { CovalentTransaction, BalanceItem, WalletFeatures } from '@/types/analysis';

const COVALENT_API_KEY = process.env.COVALENT_API_KEY!;
const CHAIN_NAME = 'eth-mainnet';
const MAX_PAGES_TO_FETCH = 50;
console.log(`Covalent API Key: ${COVALENT_API_KEY ? 'Loaded' : 'Not Loaded'}`);

const headers = {
  Authorization: `Bearer ${COVALENT_API_KEY}`,
};

async function fetchAllTransactions(address: string): Promise<CovalentTransaction[]> {
  const allItems: CovalentTransaction[] = [];
  let pageNumber = 0;
  let hasMore = true;

  while (hasMore && pageNumber < MAX_PAGES_TO_FETCH) {
    const url = `https://api.covalenthq.com/v1/${CHAIN_NAME}/address/${address}/transactions_v3/?page-number=${pageNumber}`;
    try {
      const res = await axios.get(url, { headers });
      const data = res.data?.data;
      if (data?.items) {
        allItems.push(...data.items);
        hasMore = data.pagination?.has_more ?? false;
      } else {
        hasMore = false;
      }
      pageNumber++;
    } catch (error: any) {
      console.error(`Covalent API Error on page ${pageNumber}: ${error.response?.data?.error_message || error.message}`);
      hasMore = false;
    }
  }

  return allItems;
}

async function fetchBalance(address: string): Promise<{ items: BalanceItem[] }> {
  const url = `https://api.covalenthq.com/v1/${CHAIN_NAME}/address/${address}/balances_v2/`;
  const res = await axios.get(url, { headers });
  return res.data.data;
}

function calculateAllFeatures(address: string, allTxs: CovalentTransaction[], balanceData: { items: BalanceItem[] }): WalletFeatures {
  const addr = address.toLowerCase();
  const features: Partial<WalletFeatures> = {};

  const toEther = (wei: string | undefined) => wei ? Number(BigInt(wei)) / 1e18 : 0;
  const getStats = (arr: number[]) => {
    if (arr.length === 0) return { min: 0, max: 0, avg: 0 };
    const sum = arr.reduce((a, b) => a + b, 0);
    return { min: Math.min(...arr), max: Math.max(...arr), avg: sum / arr.length };
  };
  const getTimeDiffs = (txs: any[]) => {
    if (txs.length < 2) return [];
    const ts = txs.map(tx => new Date(tx.block_signed_at).getTime()).sort((a, b) => a - b);
    return ts.slice(1).map((t, i) => (t - ts[i]) / 60000); // phút
  };
  const getAvg = (arr: number[]) => arr.length === 0 ? 0 : arr.reduce((a, b) => a + b, 0) / arr.length;
  const getMostCommon = (arr: (string | null | undefined)[]) => {
    const counts = arr.reduce((acc, val) => {
      if (!val) return acc;
      acc[val] = (acc[val] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);
    return Object.entries(counts).reduce((a, b) => a[1] > b[1] ? a : b, ['', 0])[0] || null;
  };

  const sentTxs = allTxs.filter(tx => tx.from_address.toLowerCase() === addr);
  const receivedTxs = allTxs.filter(tx => tx.to_address?.toLowerCase() === addr);
  const contractCreationTxs = sentTxs.filter(tx => tx.to_address === null);
  const sentToContractTxs = sentTxs.filter(tx => tx.to_address_is_contract);

  const tokenTransfers = allTxs.flatMap(tx => tx.log_events || [])
    .filter(log => log.decoded?.name === "Transfer" && log.decoded.params)
    .map(log => {
      const from = log.decoded.params.find((p: any) => p.name === 'from');
      const to = log.decoded.params.find((p: any) => p.name === 'to');
      const value = log.decoded.params.find((p: any) => p.name === 'value');
      return {
        block_signed_at: log.block_signed_at,
        from_address: from?.value,
        to_address: to?.value,
        to_address_is_contract: to?.is_contract,
        token_symbol: log.sender_contract_ticker_symbol,
        value_quote: value?.value_quote ? Number(value.value_quote) : 0
      };
    })
    .filter(t => t.from_address && t.to_address);

  const sentTokens = tokenTransfers.filter(t => t.from_address?.toLowerCase() === addr);
  const receivedTokens = tokenTransfers.filter(t => t.to_address?.toLowerCase() === addr);
  const sentTokensToContract = sentTokens.filter(t => t.to_address_is_contract);

  const allTimestamps = allTxs.map(tx => new Date(tx.block_signed_at).getTime());
  const firstTxTime = allTimestamps.length > 0 ? Math.min(...allTimestamps) : 0;
  const lastTxTime = allTimestamps.length > 0 ? Math.max(...allTimestamps) : 0;

  features.Index = 0;
  features.Address = address;
  features.FLAG = 0;

  features['Time Diff between first and last (Mins)'] = allTimestamps.length > 1 ? (lastTxTime - firstTxTime) / 60000 : 0;
  features['Avg min between sent tnx'] = getAvg(getTimeDiffs(sentTxs));
  features['Avg min between received tnx'] = getAvg(getTimeDiffs(receivedTxs));
  features['Sent tnx'] = sentTxs.length;
  features['Received Tnx'] = receivedTxs.length;
  features['Number of Created Contracts'] = contractCreationTxs.length;
  features['Unique Received From Addresses'] = new Set(receivedTxs.map(tx => tx.from_address)).size;
  features['Unique Sent To Addresses'] = new Set(sentTxs.map(tx => tx.to_address).filter(Boolean)).size;

  const sentValues = sentTxs.map(tx => toEther(tx.value));
  const recValues = receivedTxs.map(tx => toEther(tx.value));
  const sentContractValues = sentToContractTxs.map(tx => toEther(tx.value));

  const sentStats = getStats(sentValues);
  const recStats = getStats(recValues);
  const sentContractStats = getStats(sentContractValues);

  features['min value received'] = recStats.min;
  features['max value received'] = recStats.max;
  features['avg val received'] = recStats.avg;
  features['min val sent'] = sentStats.min;
  features['max val sent'] = sentStats.max;
  features['avg val sent'] = sentStats.avg;
  features['min value sent to contract'] = sentContractStats.min;
  features['max val sent to contract'] = sentContractStats.max;
  features['avg value sent to contract'] = sentContractStats.avg;

  features['total transactions (including tnx to create contract)'] = allTxs.length;
  features['total Ether sent'] = sentValues.reduce((a, b) => a + b, 0);
  features['total ether received'] = recValues.reduce((a, b) => a + b, 0);
  features['total ether sent contracts'] = sentContractValues.reduce((a, b) => a + b, 0);

  const ethToken = balanceData.items.find(token => token.native_token);
  features['total ether balance'] = ethToken ? Number(ethToken.balance) / (10 ** ethToken.contract_decimals) : 0;

  features['Total ERC20 tnxs'] = tokenTransfers.length;
  features['ERC20 total Ether received'] = receivedTokens.reduce((sum, t) => sum + t.value_quote, 0);
  features['ERC20 total ether sent'] = sentTokens.reduce((sum, t) => sum + t.value_quote, 0);
  features['ERC20 total Ether sent contract'] = sentTokensToContract.reduce((sum, t) => sum + t.value_quote, 0);
  features['ERC20 uniq sent addr'] = new Set(sentTokens.map(t => t.to_address)).size;
  features['ERC20 uniq rec addr'] = new Set(receivedTokens.map(t => t.from_address)).size;
  features['ERC20 uniq rec contract addr'] = new Set(receivedTokens.filter(t => t.to_address_is_contract).map(t => t.from_address)).size;
  features['ERC20 avg time between sent tnx'] = getAvg(getTimeDiffs(sentTokens));
  features['ERC20 avg time between rec tnx'] = getAvg(getTimeDiffs(receivedTokens));
  features['ERC20 avg time between contract tnx'] = getAvg(getTimeDiffs(sentTokensToContract));

  const erc20SentStats = getStats(sentTokens.map(t => t.value_quote));
  const erc20RecStats = getStats(receivedTokens.map(t => t.value_quote));
  const erc20SentContractStats = getStats(sentTokensToContract.map(t => t.value_quote));

  features['ERC20 min val rec'] = erc20RecStats.min;
  features['ERC20 max val rec'] = erc20RecStats.max;
  features['ERC20 avg val rec'] = erc20RecStats.avg;
  features['ERC20 min val sent'] = erc20SentStats.min;
  features['ERC20 max val sent'] = erc20SentStats.max;
  features['ERC20 avg val sent'] = erc20SentStats.avg;
  features['ERC20 min val sent contract'] = erc20SentContractStats.min;
  features['ERC20 max val sent contract'] = erc20SentContractStats.max;
  features['ERC20 avg val sent contract'] = erc20SentContractStats.avg;

  features['ERC20 uniq sent token name'] = new Set(sentTokens.map(t => t.token_symbol)).size;
  features['ERC20 uniq rec token name'] = new Set(receivedTokens.map(t => t.token_symbol)).size;
  features['ERC20 most sent token type'] = getMostCommon(sentTokens.map(t => t.token_symbol));
  features['ERC20 most rec token type'] = getMostCommon(receivedTokens.map(t => t.token_symbol));

  return features as WalletFeatures;
}

export async function analyzeWalletAddress(address: string): Promise<WalletFeatures> {
  try {
    console.log(`Starting analysis for address: ${address}`);

    const [allTxs, balanceData] = await Promise.all([
      fetchAllTransactions(address),
      fetchBalance(address),
    ]);

    const features = calculateAllFeatures(address, allTxs, balanceData);
    console.log(`Analysis complete for ${address}`);
    return features;

  } catch (error: any) {
    console.error(`Failed to analyze wallet ${address}:`, error.message);
    throw error;
  }
}
