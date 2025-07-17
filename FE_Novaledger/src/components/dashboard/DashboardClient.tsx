"use client";

import {
  AlertTriangle,
  ShieldCheck,
  LineChart,
  PieChart,
  SignalMedium,
  Shuffle,
  Droplets,
  Image,
  ArrowRightLeft,
} from "lucide-react";
import { useRouter } from "next/navigation";
import LineChartClient from "./LineChartClient";
import PieChartClient from "./PieChartClient";

type RiskStatus = "High" | "Medium" | "Safe";
type OnChainActivityType =
  | "Token Swap"
  | "NFT Mint"
  | "DeFi Interaction"
  | "Anonymous Deposit"
  | "Unknown Contract Interaction"
  | "ETH/Token Transfer";

interface OnChainTransaction {
  txHash: string;
  to: string;
  value: number;
  asset: string;
  activityType: OnChainActivityType;
  status: RiskStatus;
  risk: number;
}

const DUMMY_STATS = [
  {
    label: "High-Risk Transactions (24h)",
    value: "132",
    icon: <AlertTriangle className="h-6 w-6 text-red-400" />,
  },
  {
    label: "New Risky Contracts",
    value: "18",
    icon: <SignalMedium className="h-6 w-6 text-yellow-400" />,
  },
  {
    label: "Total Scanned Transactions",
    value: "3,102,482",
    icon: <ShieldCheck className="h-6 w-6 text-green-400" />,
  },
];

const DUMMY_TRANSACTIONS: OnChainTransaction[] = [
  {
    txHash: "0x1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t",
    to: "Tornado.Cash",
    value: 10.5,
    asset: "ETH",
    activityType: "Anonymous Deposit",
    status: "High",
    risk: 98,
  },
  {
    txHash: "0x3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1a2b",
    to: "Uniswap Router",
    value: 5.2,
    asset: "ETH",
    activityType: "Token Swap",
    status: "Safe",
    risk: 15,
  },
  {
    txHash: "0x5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1a2b3c4d",
    to: "ArtBlocks Minter",
    value: 1.0,
    asset: "ETH",
    activityType: "NFT Mint",
    status: "Medium",
    risk: 45,
  },
  {
    txHash: "0x7g8h9i0j1k2l3m4n5o6p7q8r9s0t1a2b3c4d5e6f",
    to: "Aave Lending Pool",
    value: 25.0,
    asset: "USDC",
    activityType: "DeFi Interaction",
    status: "Safe",
    risk: 20,
  },
  {
    txHash: "0x9i0j1k2l3m4n5o6p7q8r9s0t1a2b3c4d5e6f7g8h",
    to: "0xAb58...",
    value: 0.05,
    asset: "ETH",
    activityType: "ETH/Token Transfer",
    status: "Safe",
    risk: 5,
  },
  {
    txHash: "0x2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1a",
    to: "Unknown Contract",
    value: 0.1,
    asset: "ETH",
    activityType: "Unknown Contract Interaction",
    status: "High",
    risk: 88,
  },
];

export default function DashboardClient() {
  const router = useRouter();

  const getStatusInfo = (status: RiskStatus) => {
    switch (status) {
      case "High":
        return {
          icon: <AlertTriangle className="h-4 w-4" />,
          text: "High Risk",
          className: "bg-red-500/10 text-red-400 border border-red-500/20",
        };
      case "Medium":
        return {
          icon: <SignalMedium className="h-4 w-4" />,
          text: "Medium Risk",
          className:
            "bg-yellow-500/10 text-yellow-400 border border-yellow-500/20",
        };
      case "Safe":
        return {
          icon: <ShieldCheck className="h-4 w-4" />,
          text: "Safe",
          className: "bg-green-500/10 text-green-400 border border-green-500/20",
        };
    }
  };

  const getActivityIcon = (type: OnChainActivityType) => {
    switch (type) {
      case "Token Swap":
        return <Shuffle className="h-5 w-5 text-purple-400" />;
      case "NFT Mint":
        return <Image className="h-5 w-5 text-cyan-400" />;
      case "DeFi Interaction":
        return <Droplets className="h-5 w-5 text-blue-400" />;
      case "Anonymous Deposit":
        return <AlertTriangle className="h-5 w-5 text-red-400" />;
      case "Unknown Contract Interaction":
        return <AlertTriangle className="h-5 w-5 text-yellow-400" />;
      default:
        return <ArrowRightLeft className="h-5 w-5 text-slate-400" />;
    }
  };

  const handleTransactionClick = (txHash: string) => {
    router.push(`/analysis/${txHash}`);
  };

  return (
    <main className="p-4 sm:p-6 lg:p-8 bg-slate-900 text-white min-h-screen">
      <h1 className="text-3xl font-bold mb-6">Ethereum Network Overview</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        {DUMMY_STATS.map((stat) => (
          <div
            key={stat.label}
            className="bg-slate-800 border border-slate-700 rounded-lg p-6 flex items-center justify-between"
          >
            <div>
              <p className="text-slate-400 text-sm">{stat.label}</p>
              <p className="text-3xl font-bold">{stat.value}</p>
            </div>
            {stat.icon}
          </div>
        ))}
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6 mb-6">
        <div className="lg:col-span-3 bg-slate-800 border border-slate-700 rounded-lg p-6">
          <h2 className="text-lg font-semibold mb-4 flex items-center">
            <LineChart className="h-5 w-5 mr-2" />
            Risk Trend Over Time
          </h2>
          <div className="h-64">
            <LineChartClient />
          </div>
        </div>
        <div className="lg:col-span-2 bg-slate-800 border border-slate-700 rounded-lg p-6">
          <h2 className="text-lg font-semibold mb-4 flex items-center">
            <PieChart className="h-5 w-5 mr-2" />
            Activity Breakdown
          </h2>
          <div className="h-64">
            <PieChartClient />
          </div>
        </div>
      </div>
      <div className="bg-slate-800 border border-slate-700 rounded-lg">
        <div className="p-6">
          <h2 className="text-lg font-semibold">Recent On-chain Activity</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="border-b border-slate-700 text-sm text-slate-400">
              <tr>
                <th className="p-4 font-medium">Transaction</th>
                <th className="p-4 font-medium">Activity Type</th>
                <th className="p-4 font-medium">Value</th>
                <th className="p-4 font-medium text-center">Risk Level</th>
              </tr>
            </thead>
            <tbody>
              {DUMMY_TRANSACTIONS.map((tx) => {
                const status = getStatusInfo(tx.status);
                return (
                  <tr
                    key={tx.txHash}
                    className="border-b border-slate-800 hover:bg-slate-700/50 cursor-pointer transition-colors"
                    onClick={() => handleTransactionClick(tx.txHash)}
                  >
                    <td className="p-4">
                      <p className="font-semibold font-mono text-cyan-400">
                        {tx.txHash.slice(0, 8)}...{tx.txHash.slice(-6)}
                      </p>
                      <p className="text-xs text-slate-500">To: {tx.to}</p>
                    </td>
                    <td className="p-4">
                      <div className="flex items-center gap-3">
                        {getActivityIcon(tx.activityType)}
                        <span className="text-slate-300">
                          {tx.activityType}
                        </span>
                      </div>
                    </td>
                    <td className="p-4 font-mono">
                      {tx.value.toLocaleString("en-US")}{" "}
                      <span className="text-slate-500">{tx.asset}</span>
                    </td>
                    <td className="p-4">
                      <div className="flex justify-center">
                        <span
                          className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold ${status.className}`}
                        >
                          {status.icon}
                          {status.text} ({tx.risk})
                        </span>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
}
