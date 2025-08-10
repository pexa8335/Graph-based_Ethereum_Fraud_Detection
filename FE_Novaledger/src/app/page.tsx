"use client"; 

import React, { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment, Html } from '@react-three/drei';
import RobotModels from '@/components/ui/RobotModels';
import Link from 'next/link';

export default function HomePage() {
  return (

    <div className="relative flex flex-grow flex-col items-center justify-center p-8 text-center min-h-screen">
      <div className="absolute inset-0 z-0">
        <Canvas
          camera={{ position: [0, 0, 5], fov: 75 }}
          className="w-full h-full" 
          legacy
        >
          <Suspense fallback={
            <Html center className="bg-transparent"> 
              <div className="text-white text-xl">Loading 3D model...</div>
            </Html>
          }>
            <ambientLight intensity={0.5} />
            <directionalLight position={[2, 5, 2]} intensity={1} />
            <Environment preset="night" /> 
            <RobotModels position={[0, -1, 0]} scale={2} />
            <OrbitControls />
          </Suspense>
        </Canvas>
      </div>
      <div className="relative z-10 flex flex-col items-center justify-center p-8
                      bg-gradient-to-br from-[#1a1a2e]/5 to-[#2a2a3e]/5
                      rounded-lg shadow-2xl backdrop-blur-2xl max-w-4xl mx-auto mt-60">
        <h1 className="text-5xl md:text-6xl font-extrabold mb-4 tracking-wide text-white drop-shadow-lg"
            style={{ textShadow: '0px 0px 15px rgba(0, 255, 255, 0.4)' }}
        >
          Welcome to Aegis Intelligence
        </h1>
        <Link href="/fraud" passHref>
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