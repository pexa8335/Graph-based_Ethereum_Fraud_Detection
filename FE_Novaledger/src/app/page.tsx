// src/app/page.tsx
"use client"; // Needs "use client" for client-side interactivity and Canvas

import React, { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment, Html } from '@react-three/drei';
import RobotModels from '@/components/ui/RobotModels';
import Link from 'next/link'; // Import Link for navigation

export default function HomePage() {
  return (
    // This div serves as the main content area, filling the space next to the Sidebar
    // It will contain both the 3D background and the overlaid welcome content.
    <div className="relative flex flex-grow flex-col items-center justify-center p-8 text-center min-h-screen">
      {/* 
        3D Canvas as a background layer (z-0)
        It attempts to render. On machines with WebGL issues, it will be blank,
        but the overlay content will still be visible.
        On capable machines (like your lead's RTX 2060), the 3D model will appear beautifully.
      */}
      <div className="absolute inset-0 z-0">
        <Canvas
          camera={{ position: [0, 0, 5], fov: 75 }}
          className="w-full h-full" // Tailwind classes for full width/height
          // Keep 'legacy' prop to attempt WebGL1 fallback for wider compatibility (though might not help HD 3000)
          legacy
        >
          <Suspense fallback={
            <Html center className="bg-transparent"> {/* bg-transparent to not block the view */}
              <div className="text-white text-xl">Loading 3D model...</div>
            </Html>
          }>
            <ambientLight intensity={0.5} />
            <directionalLight position={[2, 5, 2]} intensity={1} />
            {/* You can experiment with different presets for Environment */}
            <Environment preset="night" /> 
            <RobotModels position={[0, -1, 0]} scale={2} />
            <OrbitControls />
          </Suspense>
        </Canvas>
      </div>

      {/* 
        Overlay content (Welcome message and button)
        This layer is positioned relatively and given a higher z-index (z-10)
        to appear on top of the 3D Canvas.
        It also ensures text and button are centered and readable.
      */}
      <div className="relative z-10 flex flex-col items-center justify-center p-8
                      bg-gradient-to-br from-[#1a1a2e]/80 to-[#2a2a3e]/80 
                      rounded-lg shadow-2xl backdrop-blur-sm max-w-4xl mx-auto">
        
        <h1 className="text-5xl md:text-6xl font-extrabold mb-4 tracking-wide text-white drop-shadow-lg"
            style={{ textShadow: '0px 0px 15px rgba(0, 255, 255, 0.4)' }} // Custom glow effect
        >
          Welcome to NovaLedger!
        </h1>
        
        <p className="text-lg md:text-xl leading-relaxed max-w-3xl mb-10 text-gray-300">
          Your intelligent financial analysis platform. Discover powerful tools to track, analyze, and make informed decisions about your financial data, powered by advanced technology.
        </p>
        
        <Link href="/analyze" passHref>
          <button className="px-10 py-4 text-xl font-bold uppercase tracking-wider
                             bg-[#00ffcc] text-[#1a1a2e] rounded-xl shadow-lg
                             hover:bg-[#00e6b8] hover:translate-y-[-4px] hover:shadow-2xl
                             transition-all duration-300 ease-in-out
                             focus:outline-none focus:ring-4 focus:ring-[#00ffcc] focus:ring-opacity-50">
            Get Started
          </button>
        </Link>
      </div>
    </div>
  );
}