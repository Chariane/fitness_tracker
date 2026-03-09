import { cn } from "../../../lib/utils";

interface BadgeProps {
  children: React.ReactNode;
  variant?: "default" | "premium" | "verified" | "new";
  className?: string;
}

export function Badge({ children, variant = "default", className }: BadgeProps) {
  const variants = {
    default: "bg-surface border border-border text-text-secondary",
    premium: "bg-gradient-to-r from-primary-500 to-gold-500 text-white",
    verified: "bg-green-500 text-white",
    new: "bg-primary-500 text-white",
  };

  return (
    <span className={cn(
      "inline-flex items-center px-3 py-1 rounded-full text-xs font-medium",
      variants[variant],
      className
    )}>
      {children}
    </span>
  );
}
