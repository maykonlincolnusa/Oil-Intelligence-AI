import * as React from "react";

import { cn } from "@/lib/utils";

export function Select({ className, ...props }: React.SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <select
      className={cn(
        "h-10 w-full rounded-lg border border-slate-700 bg-slate-900/70 px-3 text-sm text-ink outline-none ring-accent focus:ring-2",
        className
      )}
      {...props}
    />
  );
}
