import { WalletFeatures, AnalysisApiResponse } from '@/types/analysis';
import { featureExplanations } from '@/data/featureExplanations';
import { InfoTooltip } from '@/components/ui/InfoTooltip';
import { AlertTriangle, CheckCircle, ArrowUp, Activity } from 'lucide-react';
interface FeatureCardProps {
    label: string;
    featureKey: keyof WalletFeatures; 
    value: any;
}

export const FeatureCard = ({ label, featureKey, value }: FeatureCardProps) => {
    const explanation = featureExplanations[featureKey] || 'Không có giải thích chi tiết.';
    
    const formatValue = (val: any) => {
        if (val === null || val === undefined || val === 'null' || val === 'N/A') {
            return <span className="text-slate-500">-</span>;
        }
        if (typeof val === 'number') {
            return val % 1 === 0 ? val : val.toFixed(4);
        }
        return val;
    };

    return (
        <div className="bg-slate-800/70 p-4 rounded-xl backdrop-blur-sm border border-slate-700/50">
            <div className="flex items-center justify-between mb-1">
                <p className="text-sm text-slate-400">{label}</p>
                <InfoTooltip text={explanation} />
            </div>
            <p className="text-xl font-bold text-white truncate" title={value}>
                {formatValue(value)}
            </p>
        </div>
    );
};
interface SummaryPanelProps {
    result: AnalysisApiResponse; 
}

export const SummaryPanel = ({ result }: SummaryPanelProps) => {
    const isFraudulent = result.prediction === 'Fraud' || result.prediction === 1;
    const confidence = result.confidence ?? result.probability_fraud ?? 0;
    const summaryPoints = result.explanation
        .slice(0, 3) 
        .map(([featureString, weight]) => {
            const featureName = featureString.split(' ')[0];
            return `Yếu tố "${featureName}" là một trong những chỉ số ảnh hưởng chính đến kết quả.`;
        });
    
    if (summaryPoints.length === 0) {
        summaryPoints.push("Các mẫu giao dịch không cho thấy dấu hiệu bất thường rõ rệt.");
    }

    return (
        <div className={`rounded-2xl p-6 md:p-8 flex flex-col md:flex-row gap-8 ${ isFraudulent ? 'bg-red-900/30 border border-red-700' : 'bg-green-900/30 border border-green-700' }`}>
            <div className="text-center md:text-left flex-shrink-0">
                {isFraudulent ? <AlertTriangle className="h-12 w-12 text-red-400 mx-auto md:mx-0" /> : <CheckCircle className="h-12 w-12 text-green-400 mx-auto md:mx-0" />}
                <h2 className="text-3xl font-bold mt-4">{isFraudulent ? 'Rủi ro cao' : 'Rủi ro thấp'}</h2>
                <p className="text-slate-300 text-lg">Độ tin cậy: <span className="font-bold text-white">{(confidence * 100).toFixed(2)}%</span></p>
            </div>
            <div className="flex-1 border-t-2 md:border-t-0 md:border-l-2 pt-6 md:pt-0 md:pl-8 border-white/10">
                <h3 className="font-bold text-xl mb-3">Nhận xét chính (Từ AI)</h3>
                <ul className="space-y-2 list-disc list-inside text-slate-300">
                    {summaryPoints.map((point, i) => <li key={i}>{point}</li>)}
                    <li>Ví đã hoạt động được { (result.features.timeDiffBetweenFirstAndLastMins / 1440).toFixed(1) } ngày.</li>
                </ul>
            </div>
        </div>
    );
};
interface StatsPanelProps {
    features: WalletFeatures;
}

export const StatsPanel = ({ features }: StatsPanelProps) => {
    const generalStats: [string, keyof WalletFeatures][] = [
        ['Total Txs', 'totalTransactions'],
        ['Sent Txs', 'sentTnx'],
        ['Received Txs', 'receivedTnx'],
        ['Unique Sent To', 'uniqueSentToAddresses'],
        ['Unique Received From', 'uniqueReceivedFromAddresses'],
        ['Created Contracts', 'createdContractsCount'],
    ];
    const timeStats: [string, keyof WalletFeatures][] = [
        ['Active Time (Mins)', 'timeDiffBetweenFirstAndLastMins'],
        ['Avg Time Sent (Mins)', 'avgMinBetweenSentTnx'],
        ['Avg Time Received (Mins)', 'avgMinBetweenReceivedTnx'],
    ];
    const ethValueStats: [string, keyof WalletFeatures][] = [
        ['Total ETH Sent', 'totalEtherSent'],
        ['Total ETH Received', 'totalEtherReceived'],
        ['Current ETH Balance', 'totalEtherBalance'],
    ];
    const erc20Stats: [string, keyof WalletFeatures][] = [
        ['Total ERC20 Txs', 'totalErc20Tnxs'],
        ['Uniq Sent Tokens', 'erc20UniqSentTokenName'],
        ['Uniq Rec Tokens', 'erc20UniqRecTokenName'],
        ['Most Sent Token', 'erc20MostSentTokenType'],
        ['Most Rec Token', 'erc20MostRecTokenType'],
    ];

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="bg-slate-800/40 rounded-2xl p-6 space-y-6">
                <h3 className="text-xl font-bold tracking-wider text-cyan-400 flex items-center"><Activity className="mr-2"/> Thống kê chung & Thời gian</h3>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                    {[...generalStats, ...timeStats].map(([label, featureKey]) => (
                        <FeatureCard 
                            key={featureKey} 
                            label={label} 
                            featureKey={featureKey} 
                            value={features[featureKey]} 
                        />
                    ))}
                </div>
            </div>
            <div className="bg-slate-800/40 rounded-2xl p-6 space-y-6">
                 <h3 className="text-xl font-bold tracking-wider text-cyan-400 flex items-center"><ArrowUp className="mr-2"/> Phân tích giá trị (ETH & ERC20)</h3>
                 <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                    {[...ethValueStats, ...erc20Stats].map(([label, featureKey]) => (
                        <FeatureCard 
                            key={featureKey} 
                            label={label} 
                            featureKey={featureKey} 
                            value={features[featureKey]} 
                        />
                    ))}
                </div>
            </div>
        </div>
    );
};