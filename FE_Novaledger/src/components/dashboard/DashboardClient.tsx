"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import MOCK_WALLETS from "@/data/mockAddresses";
import { WalletAnalysisResult } from "@/types/dashboard"; 
import { getStatusInfo } from "@/utils/walletStatusUtils";
import { sendAlert as sendTelegramAlert } from "@/services/alertService";
import { fetchAnalysisData } from "@/services/analysisService"; 
import { Loader2 } from "lucide-react"; 
const SCAM_WALLET_ADDRESS = "0x742d35Cc6634C05329a2Ea0e04737057Ca79ed46";

export default function DashboardClient() {
  const router = useRouter();
  const [walletData, setWalletData] = useState<WalletAnalysisResult[]>([]);

  const handleAnalyzeClick = (address: string) => {
    router.push(`/analysis/${address}`);
  };

  useEffect(() => {
    const fetchAllWalletData = async () => {
      const initialWalletStates: WalletAnalysisResult[] = MOCK_WALLETS.map(address => ({
        address,
        isLoading: true,
        error: null,
        prediction: undefined,
        probability_fraud: undefined,
        status: undefined,
        percent: undefined,
        confidence_score: undefined,
        explanation: undefined,
        feature_importance: undefined,
      }));
      setWalletData(initialWalletStates);

      for (const address of MOCK_WALLETS) {
        try {
          const result = await fetchAnalysisData(address);
          setWalletData(prevData => prevData.map(wallet =>
            wallet.address === address
              ? { ...result, isLoading: false, error: null }
              : wallet
          ));

          if (address === SCAM_WALLET_ADDRESS && result.prediction === "Fraud") {
            const scamReasons = [
              "- Extremely high ERC20 token outflows observed.",
              "- Funds dispersed across a high number of unique recipient addresses.",
              "- Discrepancy between very low ETH balance and massive ERC20 activity."
            ];
            const detailedMessage = `🚨 ALERT: Wallet "${address.slice(0, 10)}..." identified as a scam or high-risk wallet.\n\nReasons for high risk:\n${scamReasons.join('\n')}`;
            sendTelegramAlert(detailedMessage);
          }

        } catch (e: any) {
          console.error(`[DashboardClient] Failed to fetch data for ${address}:`, e);
          setWalletData(prevData => prevData.map(wallet =>
            wallet.address === address
              ? { ...wallet, isLoading: false, error: e.message || "Failed to fetch analysis" }
              : wallet
          ));
        }
      }
    };

    fetchAllWalletData();
  }, []); 
  const isAnyWalletLoading = walletData.some(wallet => wallet.isLoading);

  return (
    <main className="p-4 sm:p-6 lg:p-8 bg-slate-900 text-white min-h-screen">
      <h1 className="text-3xl font-bold mb-6">Ethereum Wallet Overview</h1>

      {isAnyWalletLoading && (
        <div className="text-center py-8 flex items-center justify-center text-slate-400">
          <Loader2 className="h-6 w-6 animate-spin mr-2" />
          <p>Loading wallet analysis results...</p>
        </div>
      )}

      {!isAnyWalletLoading && walletData.length === 0 && (
        <div className="text-center py-8 text-slate-400">
          <p>No wallet data to display after analysis attempt.</p>
        </div>
      )}

      {walletData.length > 0 && (
        <div className="bg-slate-800 border border-slate-700 rounded-lg overflow-hidden">
          <div className="p-6">
            <h2 className="text-lg font-semibold">Wallet List and Risk Assessment</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead className="border-b border-slate-700 text-sm text-slate-400">
                <tr>
                  <th className="p-4 font-medium">Wallet Address</th>
                  <th className="p-4 font-medium">Risk Level Assessment</th>
                  <th className="p-4 font-medium">Analysis Link</th>
                </tr>
              </thead>
              <tbody>
                {walletData.map((wallet) => {
                  const statusInfo = getStatusInfo(wallet.prediction);

                  return (
                    <tr
                      key={wallet.address}
                      className="border-b border-slate-800 hover:bg-slate-700/50 transition-colors"
                    >
                      <td className="p-4">
                        <p className="font-semibold font-mono text-cyan-400">
                          {wallet.address.slice(0, 10)}...{wallet.address.slice(-8)}
                        </p>
                      </td>
                      <td className="p-4">
                        {wallet.isLoading ? (
                          <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-gray-500/20 text-gray-400">
                            <Loader2 className="h-4 w-4 animate-spin" /> Analyzing...
                          </span>
                        ) : wallet.error ? (
                          <span className="text-red-400" title={wallet.error}>
                            Error: {wallet.error.substring(0, 30)}...
                          </span>
                        ) : (
                          <span
                            className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold ${statusInfo.className}`}
                          >
                            {statusInfo.icon}
                            {statusInfo.text}{" "}
                            {wallet.probability_fraud !== null && wallet.probability_fraud !== undefined &&
                              `(${Math.round(wallet.probability_fraud * 100)}%)`}
                          </span>
                        )}
                      </td>
                      <td className="p-4">
                        {wallet.isLoading || wallet.error ? (
                          <button
                            className="text-slate-500 cursor-not-allowed px-4 py-2 rounded-md"
                            disabled
                          >
                            Not Available
                          </button>
                        ) : (
                          <button
                            onClick={() => handleAnalyzeClick(wallet.address)}
                            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md transition-colors cursor-pointer"
                          >
                            Detailed Analysis
                          </button>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </main>
  );
}