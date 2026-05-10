"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BarChart3,
  Bell,
  Database,
  FileText,
  Globe,
  Newspaper,
  Radar,
  Settings,
  ShieldAlert,
  Ship,
  Satellite,
} from "lucide-react";

import { cn } from "@/lib/utils";

const items = [
  { href: "/dashboard", label: "Dashboard", icon: BarChart3 },
  { href: "/market", label: "Market", icon: Globe },
  { href: "/events", label: "Events", icon: Newspaper },
  { href: "/scenarios", label: "Scenarios", icon: Radar },
  { href: "/maritime", label: "Maritime", icon: Ship },
  { href: "/maritime-map", label: "Maritime Map", icon: Ship },
  { href: "/risk-center", label: "Risk Center", icon: ShieldAlert },
  { href: "/reports", label: "Reports", icon: FileText },
  { href: "/alerts", label: "Alerts", icon: Bell },
  { href: "/satellite", label: "Satellite", icon: Satellite },
  { href: "/fields", label: "Fields", icon: Database },
  { href: "/settings", label: "Settings", icon: Settings },
];

export function SidebarNav() {
  const pathname = usePathname();

  return (
    <aside className="grid-pattern sticky top-0 hidden h-screen w-64 border-r border-slate-800/70 bg-slate-950/60 p-5 lg:block">
      <Link href="/" className="mb-8 block">
        <div className="font-display text-xl font-semibold tracking-tight text-ink">Oil Intelligence AI</div>
        <div className="text-xs uppercase tracking-[0.18em] text-muted">Energy Risk Intelligence</div>
      </Link>
      <nav className="space-y-2">
        {items.map((item) => {
          const Icon = item.icon;
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition",
                active ? "bg-accent/20 text-accent" : "text-muted hover:bg-slate-800/70 hover:text-ink"
              )}
            >
              <Icon size={16} />
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
