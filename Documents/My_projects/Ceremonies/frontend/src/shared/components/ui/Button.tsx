import { motion, type HTMLMotionProps } from "framer-motion";
import { cn } from "../../../lib/utils";

interface ButtonProps extends HTMLMotionProps<"button"> {
  variant?: "primary" | "secondary" | "outline" | "ghost";
  size?: "sm" | "md" | "lg";
  fullWidth?: boolean;
  children: React.ReactNode;
}

export function Button({ 
  variant = "primary", 
  size = "md", 
  fullWidth,
  children, 
  className,
  ...props 
}: ButtonProps) {
  const baseStyles = "inline-flex items-center justify-center font-medium rounded-xl transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-primary-500/50 disabled:opacity-50";
  
  const variants = {
    primary: "bg-gradient-to-r from-primary-500 to-gold-500 text-white hover:from-primary-600 hover:to-gold-600 shadow-lg shadow-primary-500/25 hover:shadow-xl hover:shadow-primary-500/35 hover:scale-[1.02] active:scale-[0.98]",
    secondary: "bg-white text-text-primary border border-border hover:bg-surface-alt hover:border-primary-200 hover:scale-[1.02] active:scale-[0.98]",
    outline: "border-2 border-primary-500/30 bg-transparent text-text-primary hover:bg-primary-50 hover:border-primary-500/50 hover:scale-[1.02] active:scale-[0.98]",
    ghost: "text-text-secondary hover:text-text-primary hover:bg-surface-alt",
  };
  
  const sizes = {
    sm: "text-sm px-4 py-2 gap-2",
    md: "text-base px-6 py-3 gap-2.5",
    lg: "text-lg px-8 py-4 gap-3",
  };
  
  return (
    <motion.button
      whileHover={{ scale: variant !== "ghost" ? 1.02 : 1 }}
      whileTap={{ scale: 0.98 }}
      className={cn(
        baseStyles, 
        variants[variant], 
        sizes[size],
        fullWidth && "w-full",
        className
      )}
      {...props}
    >
      {children}
    </motion.button>
  );
}
