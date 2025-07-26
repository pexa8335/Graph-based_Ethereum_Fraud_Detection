"use client";
import { useEffect, useState } from "react";
import { Loader2, ServerCrash } from "lucide-react";

interface GraphDisplayProps {
  address: string;
}

export const GraphDisplay = ({ address }: GraphDisplayProps) => {
  const [htmlContent, setHtmlContent] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchGraph = async () => {
      setIsLoading(true);
      setError(null);
      setHtmlContent(null);
      try {
        // Call internal Next.js API route to fetch graph HTML
        const response = await fetch("/api/graph", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ address }),
        });
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || "Failed to fetch graph");
        }
        const html = await response.text();
        setHtmlContent(html);
      } catch (error: any) {
        console.error("Error loading graph:", error);
        setError(error.message || "Unknown error occurred while loading the graph.");
      } finally {
        setIsLoading(false);
      }
    };
    fetchGraph();
  }, [address]);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center h-96 bg-slate-800 rounded-lg">
        <Loader2 className="h-12 w-12 animate-spin text-cyan-400" />
        <p className="mt-4 text-slate-400">Generating transaction network graph...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-96 bg-slate-800 rounded-lg text-red-400">
        <ServerCrash className="h-12 w-12" />
        <p className="mt-4">Error loading graph: {error}</p>
      </div>
    );
  }

  if (!htmlContent) {
    return (
      <div className="flex flex-col items-center justify-center h-96 bg-slate-800 rounded-lg text-slate-500">
        <p>No graph available to display.</p>
      </div>
    );
  }

  return (
    <div className="bg-slate-800/40 rounded-2xl p-6 h-[800px] flex flex-col">
      <h3 className="text-xl font-bold tracking-wider text-cyan-400 mb-4">
        Transaction Network Graph
      </h3>
      <iframe
        srcDoc={htmlContent}
        title={`Transaction Network for ${address}`}
        className="flex-grow w-full border-none rounded-lg"
        sandbox="allow-scripts allow-same-origin"
      />
    </div>
  );
};
