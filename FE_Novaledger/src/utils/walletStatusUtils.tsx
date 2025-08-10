import { AlertTriangle, ShieldCheck, SignalMedium } from "lucide-react";
import { JSX } from "react";

interface StatusInfo {
  icon: JSX.Element | null;
  text: string;
  className: string;
}

export const getStatusInfo = (status: string | null | undefined): StatusInfo => {
  switch (status) {
    case "High":
    case "Fraud":
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
    case "Non-Fraud":
      return {
        icon: <ShieldCheck className="h-4 w-4" />,
        text: "Safe",
        className:
          "bg-green-500/10 text-green-400 border border-green-500/20",
      };
    default:
      return {
        icon: null,
        text: "Undetermined",
        className: "bg-slate-700/10 text-slate-400 border border-slate-700/20",
      };
  }
};