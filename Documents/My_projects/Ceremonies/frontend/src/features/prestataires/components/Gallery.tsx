import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronLeftIcon, ChevronRightIcon, XMarkIcon } from "@heroicons/react/24/outline";

interface GalleryProps {
  images: string[];
  className?: string;
}

export function Gallery({ images, className = "" }: GalleryProps) {
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);

  const openLightbox = (index: number) => setSelectedIndex(index);
  const closeLightbox = () => setSelectedIndex(null);
  const nextImage = () => setSelectedIndex((prev) => (prev !== null ? (prev + 1) % images.length : null));
  const prevImage = () => setSelectedIndex((prev) => (prev !== null ? (prev - 1 + images.length) % images.length : null));

  if (images.length === 0) {
    return (
      <div className={`bg-gray-200 rounded-2xl h-64 flex items-center justify-center text-text-secondary ${className}`}>
        Aucune image
      </div>
    );
  }

  return (
    <>
      <div className={`grid grid-cols-2 md:grid-cols-4 gap-4 ${className}`}>
        {images.map((src, index) => (
          <motion.div
            key={index}
            whileHover={{ scale: 1.02 }}
            className="relative aspect-square rounded-xl overflow-hidden cursor-pointer"
            onClick={() => openLightbox(index)}
          >
            <img src={src} alt={`Gallery ${index + 1}`} className="w-full h-full object-cover" />
          </motion.div>
        ))}
      </div>

      {/* Lightbox */}
      <AnimatePresence>
        {selectedIndex !== null && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/90 z-50"
              onClick={closeLightbox}
            />
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="fixed inset-0 z-50 flex items-center justify-center p-4"
            >
              <button
                onClick={closeLightbox}
                className="absolute top-4 right-4 text-white/70 hover:text-white p-2"
              >
                <XMarkIcon className="w-8 h-8" />
              </button>
              <button
                onClick={prevImage}
                className="absolute left-4 text-white/70 hover:text-white p-2"
              >
                <ChevronLeftIcon className="w-8 h-8" />
              </button>
              <button
                onClick={nextImage}
                className="absolute right-4 text-white/70 hover:text-white p-2"
              >
                <ChevronRightIcon className="w-8 h-8" />
              </button>
              <img
                src={images[selectedIndex]}
                alt={`Gallery ${selectedIndex + 1}`}
                className="max-h-full max-w-full object-contain"
              />
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}