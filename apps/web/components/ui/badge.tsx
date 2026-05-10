import * as React from "react";

import { cn } from "@/lib/utils";

const variants = {
  default: "bg-panelSoft text-ink",
  success: "bg-success/20 text-success",
  danger: "bg-danger/20 text-danger",
  accent: "bg-accent/20 text-accent",
};

export function Badge({
  className,
  variant = "default",
  ...props
}: React.HTMLAttributes<HTMLSpanElement> & { variant?: keyof typeof variants }) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-md px-2 py-1 text-xs font-medium tracking-wide",
        variants[variant],
        className
      )}
      {...props}
    />
  );
}
