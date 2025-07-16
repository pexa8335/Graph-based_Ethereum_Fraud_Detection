import { WalletFeatures, AnalysisApiResponse } from '@/types/analysis';
import { featureExplanations } from '@/data/featureExplanations'; 
import { InfoTooltip } from '@/components/ui/InfoTooltip'; 
import { AlertTriangle, CheckCircle, ArrowUp, Activity } from 'lucide-react';

interface FeatureCardProps {
    label: string; 
    featureKey: keyof WalletFeatures; 
    value: any; 
}
interface SummaryPanelProps {
    result: AnalysisApiResponse; 
}
export const FeatureCard = ({ label, featureKey, value }: FeatureCardProps) => {
    const explanation = featureExplanations[featureKey] || 'Không có giải thích chi tiết.';
    
    const formatValue = (val: any) => {
        if (val === null || val === undefined || val === 'null' || val === 'N/A') {
            return <span className="text-slate-500">-</span>;
        }
        if (typeof val === 'number') {
            if (val > 1e18) { 
                return val.toExponential(2);
            }
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
            <p className="text-xl font-bold text-white truncate" title={String(value)}>
                {formatValue(value)}
            </p>
        </div>
    );
};
export const SummaryPanel = ({ result }: SummaryPanelProps) => {
    const isFraudulent = result.prediction === 'Fraud'; 
    const confidence = result.probability_fraud ?? 0; 

    const summaryPoints = result.lime_explanation 
        .slice(0, 5) 
        .map(([featureString, weight]) => {
            const cleanedFeatureName = featureString.split(/ (<=|>|==|!=|>=) /)[0].replace(/_/g, ' ').trim();
            return `Yếu tố "${cleanedFeatureName}" là một trong những chỉ số ảnh hưởng chính đến kết quả.`;
        });
    
    if (summaryPoints.length === 0) {
        summaryPoints.push("Các mẫu giao dịch không cho thấy dấu hiệu bất thường rõ rệt.");
    }

    return (
        <div className={`rounded-2xl p-6 md:p-8 flex flex-col md:flex-row gap-8 ${ isFraudulent ? 'bg-red-900/30 border border-red-700' : 'bg-green-900/30 border border-green-700' }`}>
            <div className="text-center md:text-left flex-shrink-0">
                {isFraudulent ? <AlertTriangle className="h-12 w-12 text-red-400 mx-auto md:mx-0" /> : <CheckCircle className="h-12 w-12 text-green-400 mx-auto md:mx-0" />}
                <h2 className="text-3xl font-bold mt-4">
                    {result.prediction === null ? 'Đang chờ dự đoán' : (isFraudulent ? 'Rủi ro cao' : 'Rủi ro thấp')}
                </h2>
                <p className="text-slate-300 text-lg">
                    Độ tin cậy: <span className="font-bold text-white">{(confidence * 100).toFixed(2)}%</span>
                </p>
            </div>
            <div className="flex-1 border-t-2 md:border-t-0 md:border-l-2 pt-6 md:pt-0 md:pl-8 border-white/10">
                <h3 className="font-bold text-xl mb-3">Nhận xét chính (Từ AI)</h3>
                <ul className="space-y-2 list-disc list-inside text-slate-300">
                    {summaryPoints.map((point, i) => <li key={i}>{point}</li>)}
                    <li>Ví đã hoạt động được { (result.features['Time Diff between first and last (Mins)'] / 1440).toFixed(1) } ngày.</li>
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
        ['Total Txs', 'total transactions (including tnx to create contract'], 
        ['Sent Txs', 'Sent tnx'], 
        ['Received Txs', 'Received Tnx'], 
        ['Unique Sent To', 'Unique Sent To Addresses'], 
        ['Unique Received From', 'Unique Received From Addresses'], 
        ['Created Contracts', 'Number of Created Contracts'],
    ];
    const timeStats: [string, keyof WalletFeatures][] = [
        ['Active Time (Mins)', 'Time Diff between first and last (Mins)'],
        ['Avg Time Sent (Mins)', 'Avg min between sent tnx'],
        ['Avg Time Received (Mins)', 'Avg min between received tnx'],
    ];
    const ethValueStats: [string, keyof WalletFeatures][] = [
        ['Total ETH Sent', 'total Ether sent'],
        ['Total ETH Received', 'total ether received'],
        ['Current ETH Balance', 'total ether balance'],
    ];
    const erc20Stats: [string, keyof WalletFeatures][] = [
        ['Total ERC20 Txs', 'Total ERC20 tnxs'],
        ['Uniq Sent Tokens', 'ERC20 uniq sent token name'],
        ['Uniq Rec Tokens', 'ERC20 uniq rec token name'],
        ['Most Sent Token', 'ERC20 most sent token type_label'], 
        ['Most Rec Token', 'ERC20_most_rec_token_type_label'],
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