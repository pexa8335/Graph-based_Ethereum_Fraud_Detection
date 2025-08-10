import { AnalysisApiResponse, FeatureCardProps } from "@/types/analysis";
import { featureExplanations } from "@/data/featureExplanations";
import { InfoTooltip } from "@/components/ui/InfoTooltip";
import { AlertTriangle, CheckCircle, Activity } from "lucide-react";
import React from "react";
export const FeatureCard = ({ label, featureKey, value }: FeatureCardProps) => {
  const explanation =
    featureExplanations[featureKey as keyof typeof featureExplanations] ||
    "No detailed explanation available.";

  const formatValue = (val: any): React.JSX.Element => {
    if (val === null || val === undefined || val === "null" || val === "N/A" || val === -1) {
      return <span>0</span>;
    }
    if (typeof val === "number") {
      if (val > 1e18 || (val < 1e-10 && val !== 0)) {
        return <span>{val.toExponential(4)}</span>;
      }
      return (
        <span>{val % 1 === 0 ? val.toLocaleString() : val.toFixed(4)}</span>
      );
    }
    return <span>{String(val)}</span>;
  };

  return (
    <div className="bg-slate-800/70 p-4 rounded-xl backdrop-blur-sm border border-slate-700/50">
      <div className="flex items-center justify-between mb-1">
        <p className="text-sm text-slate-400">{label}</p>
        <InfoTooltip text={explanation} />
      </div>
      <p
        className="text-xl font-bold text-white truncate"
        title={String(value)}
      >
        {formatValue(value)}
      </p>
    </div>
  );
};

interface SummaryPanelProps {
  result: AnalysisApiResponse;
}

export const SummaryPanel = ({ result }: SummaryPanelProps) => {
  const isFraudulent = result.prediction === "Fraud";
  const confidence = result.probability_fraud ?? 0;
  const featureImportanceEntries = result.feature_importance
    ? Object.entries(result.feature_importance)
    : [];

  const sortedImportantFeatures = featureImportanceEntries
    .sort(([, weightA], [, weightB]) => Math.abs(weightB) - Math.abs(weightA)) 
    .slice(0, 3);

  const summaryPoints = sortedImportantFeatures.map(([featureKey, weight]) => {
    const detailedExplanation =
      featureExplanations[featureKey as keyof typeof featureExplanations] ||
      "A key indicator influencing the result."
    return `The factor "${featureKey.replace(/_/g, " ").trim()}" (Importance: ${weight.toFixed(2)}) is one of the key indicators influencing the result. ${detailedExplanation}`;
  });

  if (summaryPoints.length === 0) {
    summaryPoints.push(
      "No clear signs of abnormal activity found in the transaction patterns."
    );
  }

  return (
    <div
      className={`rounded-2xl p-6 md:p-8 flex flex-col md:flex-row gap-8 ${
        isFraudulent
          ? "bg-red-900/30 border border-red-700"
          : "bg-green-900/30 border border-green-700"
      }`}
    >
      <div className="text-center md:text-left flex-shrink-0">
        {isFraudulent ? (
          <AlertTriangle className="h-12 w-12 text-red-400 mx-auto md:mx-0" />
        ) : (
          <CheckCircle className="h-12 w-12 text-green-400 mx-auto md:mx-0" />
        )}
        <h2 className="text-3xl font-bold mt-4">
          {result.prediction === null
            ? "Prediction Pending"
            : isFraudulent
            ? "High Risk"
            : "Low Risk"}
        </h2>
        <p className="text-slate-300 text-lg">
          Confidence:{" "}
          <span className="font-bold text-white">
            {(confidence * 100).toFixed(2)}%
          </span>
        </p>
      </div>
      <div className="flex-1 border-t-2 md:border-t-0 md:border-l-2 pt-6 md:pt-0 md:pl-8 border-white/10">
        <h3 className="font-bold text-xl mb-3">Key Insights</h3>
        <ul className="space-y-2 list-disc list-inside text-slate-300">
          {summaryPoints.map((point, i) => (
            <li key={i}>{point}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

interface StatsPanelProps {
  features: Record<string, number>;
}

export const StatsPanel = ({ features }: StatsPanelProps) => {
  const allStats = [
    [
      "Total Transactions",
      "total transactions (including tnx to create contract",
    ],
    ["Sent Transactions", "Sent tnx"],
    ["Received Tnx", "Received Tnx"],
    ["Unique Sent To", "Unique Sent To Addresses"],
    ["Unique Received From", "Unique Received From Addresses"],
    ["Created Contracts", "Number of Created Contracts"],
    ["Active Time (Mins)", "Time Diff between first and last (Mins)"],
    ["Avg Time Sent (Mins)", "Avg min between sent tnx"],
    ["Avg Time Received (Mins)", "Avg min between received tnx"],

    ["Total ETH Sent", "total Ether sent"],
    ["Total ETH Received", "total ether received"],
    ["Current ETH Balance", "total ether balance"],
    ["Min ETH Received", "min value received"],
    ["Max ETH Received", "max value received"],
    ["Avg ETH Received", "avg val received"],
    ["Min ETH Sent", "min val sent"],
    ["Max ETH Sent", "max val sent"],
    ["Avg ETH Sent", "avg val sent"],
    ["Min ETH Sent to Contract", "min value sent to contract"],
    ["Max ETH Sent to Contract", "max val sent to contract"],
    ["Avg ETH Sent to Contract", "avg value sent to contract"],

    ["Total ERC20 Txs", "Total ERC20 tnxs"],
    ["Unique Sent Tokens", "ERC20 uniq sent token name"],
    ["Unique Received Tokens", "ERC20 uniq rec token name"],
    ["Most Sent Token Type", "ERC20 most sent token type"], 
    ["Most Received Token Type", "ERC20_most_rec_token_type"], 
    ["Total ERC20 Received", "ERC20 total Ether received"],
    ["Total ERC20 Sent", "ERC20 total ether sent"],
    ["Total ERC20 Sent to Contract", "ERC20 total Ether sent contract"],
    ["Unique ERC20 Sent Addr", "ERC20 uniq sent addr"],
    ["Unique ERC20 Received Addr", "ERC20 uniq rec addr"],
    ["Unique ERC20 Sent Addr (Alt)", "ERC20 uniq sent addr.1"],
    ["Unique ERC20 Rec Contract Addr", "ERC20 uniq rec contract addr"],
    ["Avg Time Between ERC20 Sent", "ERC20 avg time between sent tnx"],
    ["Avg Time Between ERC20 Rec", "ERC20 avg time between rec tnx"],
    ["Avg Time Between ERC20 Rec 2", "ERC20 avg time between rec 2 tnx"],
    ["Avg Time Between ERC20 Contract", "ERC20 avg time between contract tnx"],
    ["Min ERC20 Rec Value", "ERC20 min val rec"],
    ["Max ERC20 Rec Value", "ERC20 max val rec"],
    ["Avg ERC20 Rec Value", "ERC20 avg val rec"],
    ["Min ERC20 Sent Value", "ERC20 min val sent"],
    ["Max ERC20 Sent Value", "ERC20 max val sent"],
    ["Avg ERC20 Sent Value", "ERC20 avg val sent"],
    ["Min ERC20 Sent to Contract Value", "ERC20 min val sent contract"],
    ["Max ERC20 Sent to Contract Value", "ERC20 max val sent contract"],
    ["Avg ERC20 Sent to Contract Value", "ERC20 avg val sent contract"],
  ] as const;

  const formatValue = (val: any): React.JSX.Element => {
    if (val === null || val === undefined || val === "null" || val === "N/A" || val === -1) {
      return <span>0</span>;
    }
    if (typeof val === "number") {
      if (val > 1e18 || (val < 1e-10 && val !== 0)) {
        return <span>{val.toExponential(4)}</span>;
      }
      return (
        <span>{val % 1 === 0 ? val.toLocaleString() : val.toFixed(4)}</span>
      );
    }
    return <span>{String(val)}</span>;
  };

  return (
    <div className="bg-slate-800/40 rounded-2xl p-6 space-y-6">
      <h2 className="text-xl font-bold tracking-wider text-cyan-400 flex items-center">
        <Activity className="mr-2" /> Detailed Feature Statistics
      </h2>
      <p className="text-xs italic text-slate-400 mb-4">
       The values here represent the influence (Weight-based) of each feature on the prediction, not the raw feature value
      </p>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-slate-700">
              <th className="px-4 py-3 font-medium text-slate-400 w-1/3">
                Feature
              </th>
              <th className="px-4 py-3 font-medium text-slate-400 w-1/4">
                Weight-based
              </th>
              <th className="px-4 py-3 font-medium text-slate-400 w-auto">
                Explanation
              </th>
            </tr>
          </thead>
          <tbody>
            {allStats.map(([label, featureKey]) => (
              <tr
                key={featureKey}
                className="border-b border-slate-800 hover:bg-slate-700/50 transition-colors"
              >
                <td className="px-4 py-3 font-semibold text-white">
                  <div className="flex items-center gap-2">
                    {label}
                    <InfoTooltip
                      text={
                        featureExplanations[
                          featureKey as keyof typeof featureExplanations
                        ] || "No detailed explanation available."
                      }
                    />
                  </div>
                </td>
                <td className="px-4 py-3 font-mono text-cyan-300">
                  {/* Simplest and most correct approach: directly pass the value (which might be undefined) to formatValue */}
                  {formatValue(features?.[featureKey])}
                </td>
                <td className="px-4 py-3 text-slate-400 text-sm">
                  {featureExplanations[
                    featureKey as keyof typeof featureExplanations
                  ] || "Explanation not available."}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};