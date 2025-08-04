"use client";
import { useEffect, useState } from "react";
import JSZip from "jszip";
import { Loader2, ServerCrash, FileDown } from "lucide-react";

interface GraphDisplayProps {
  address: string;
}

export const GraphDisplay = ({ address }: GraphDisplayProps) => {
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [csvUrl, setCsvUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
  const fetchGraph = async () => {
    setIsLoading(true);
    setError(null);
    setImageUrl(null);
    setCsvUrl(null);

    try {
      const res = await fetch("/api/graph", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ address }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || "Failed to fetch graph.");
      }

      const zipBlob = await res.blob();
      const zipUrl = URL.createObjectURL(zipBlob);
      const a = document.createElement("a");
      a.href = zipUrl;
      a.download = `analysis_${address.slice(0, 6)}.zip`;
      document.body.appendChild(a);
      a.click();
      a.remove();

      const zip = await JSZip.loadAsync(zipBlob);
      const imageFile = zip.file("transaction_graph.png");
      const csvFile = zip.file("enriched_transactions.csv");

      if (!imageFile && !csvFile) {
        throw new Error("No valid files found inside the .zip archive.");
      }

      if (imageFile) {
        const imageBlob = await imageFile.async("blob");
        const imageUrl = URL.createObjectURL(imageBlob);
        setImageUrl(imageUrl);
      }

      if (csvFile) {
        const csvBlob = await csvFile.async("blob");
        const csvUrl = URL.createObjectURL(csvBlob);
        setCsvUrl(csvUrl);
      }

    } catch (err: any) {
      console.error("❌ Error processing graph:", err);
      setError(err.message || "Unknown error occurred");
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
        <p className="mt-4 text-slate-400">Generating transaction graph...</p>
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

  return (
    <div className="bg-slate-800/40 rounded-2xl p-6 flex flex-col items-center">
      <h3 className="text-xl font-bold tracking-wider text-cyan-400 mb-4">
        Transaction Graph & Report
      </h3>

      {imageUrl && (
        <img
          src={imageUrl}
          alt="Transaction Graph"
          className="rounded-lg max-w-full max-h-[400px] border border-slate-700"
        />
      )}

      {csvUrl && (
        <a
          href={csvUrl}
          download={`transactions_${address.slice(0, 6)}.csv`}
          className="mt-6 inline-flex items-center gap-2 px-4 py-2 bg-cyan-600 text-white rounded hover:bg-cyan-700 transition"
        >
          <FileDown className="w-5 h-5" />
          Download CSV File
        </a>
      )}
    </div>
  );
};
