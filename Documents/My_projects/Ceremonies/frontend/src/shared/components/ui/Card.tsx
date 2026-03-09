import { motion } from "framer-motion";
import { cn } from "../../../lib/utils";

interface CardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
  onClick?: () => void;
}

export function Card({ children, className, hover = true, onClick }: CardProps) {
  return (
    <motion.div
      whileHover={hover ? { y: -4 } : {}}
      className={cn(
        "bg-white rounded-2xl border border-border p-6 shadow-soft hover:shadow-medium transition-all duration-300",
        className
      )}
      onClick={onClick}
    >
      {children}
    </motion.div>
  );
}
