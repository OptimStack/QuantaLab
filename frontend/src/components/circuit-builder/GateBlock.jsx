import React from 'react';
import { useDraggable } from '@dnd-kit/core';

const GateBlock = ({ id, gate, color, isPaletteItem = false }) => {
  const { attributes, listeners, setNodeRef, transform } = useDraggable({
    id: id,
    data: { gate, color }
  });

  const style = transform ? {
    transform: `translate3d(${transform.x}px, ${transform.y}px, 0)`,
  } : undefined;

  return (
    <div 
      ref={setNodeRef} 
      style={style} 
      {...listeners} 
      {...attributes}
      className={`flex items-center justify-center w-10 h-10 rounded text-white font-bold text-sm cursor-grab active:cursor-grabbing shadow-sm
        ${color} ${isPaletteItem ? 'hover:scale-105 transition-transform' : 'absolute z-10'}`}
    >
      {gate}
    </div>
  );
};

export default GateBlock;
