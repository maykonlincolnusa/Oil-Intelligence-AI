import { Badge } from "@/components/ui/badge";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";

export function MetricCard({
  label,
  value,
  tone = "default",
  description,
}: {
  label: string;
  value: string | number;
  tone?: "default" | "success" | "danger" | "accent";
  description?: string;
}) {
  return (
    <Card className="animate-fade-up">
      <div className="mb-4 flex items-center justify-between">
        <CardDescription>{label}</CardDescription>
        <Badge variant={tone}>{tone.toUpperCase()}</Badge>
      </div>
      <CardTitle className="text-3xl font-semibold">{value}</CardTitle>
      {description ? <CardDescription className="mt-2">{description}</CardDescription> : null}
    </Card>
  );
}
