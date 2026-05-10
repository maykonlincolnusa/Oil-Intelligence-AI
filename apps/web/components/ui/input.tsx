import * as React from "react";

import { cn } from "@/lib/utils";

export function Input({ className, ...props }: React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      className={cn(
        "h-10 w-full rounded-lg border border-slate-700 bg-slate-900/70 px-3 text-sm text-ink outline-none ring-accent placeholder:text-muted focus:ring-2",
        className
      )}
      {...props}
    />
  );
}
