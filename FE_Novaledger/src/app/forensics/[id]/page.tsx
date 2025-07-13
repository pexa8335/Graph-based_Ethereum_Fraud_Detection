import ForensicsClient from "@/components/forensics/ForensicsClient";

export default async function ForensicsPage({
  params,
}: {
  params: { id: string };
}) {
  return <ForensicsClient transactionId={params.id} />;
}
