import { Info } from 'lucide-react';

interface InfoTooltipProps {
  text: string;
}

export const InfoTooltip = ({ text }: InfoTooltipProps) => {
  return (
    <div className="group relative inline-flex">
      <button className="text-gray-500 hover:text-cyan-400 transition-colors">
        <Info className="h-4 w-4" />
      </button>

      <div 
        className="
          absolute bottom-full left-1/2 mb-2 w-64 -translate-x-1/2
          transform rounded-lg bg-gray-900 px-3 py-2 text-center text-sm text-white shadow-lg
          opacity-0 transition-opacity duration-300 group-hover:opacity-100
          invisible group-hover:visible pointer-events-none group-hover:pointer-events-auto
        "
      >
        {text}
        <div 
          className="absolute left-1/2 top-full h-0 w-0 -translate-x-1/2 
                     border-x-8 border-t-8 border-x-transparent border-t-gray-900"
        ></div>
      </div>
    </div>
  );
};