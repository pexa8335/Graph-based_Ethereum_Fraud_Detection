"use client";

import React, { useRef, useEffect } from 'react'; 
import { useGLTF, useAnimations } from '@react-three/drei';
import { useFrame } from '@react-three/fiber'; 
import * as THREE from 'three';

interface RobotModelsProps {
  position?: [number, number, number];
  scale?: number | [number, number, number];
}

const RobotModels: React.FC<RobotModelsProps> = (props) => {
  const group = useRef<THREE.Group>(null); 
  const { scene, animations } = useGLTF('/robot_playground/scene.gltf'); 
  const { actions, mixer } = useAnimations(animations, group);
  useEffect(() => {
    if (animations && animations.length > 0) {
      const firstAction = actions[animations[0].name];
      if (firstAction) {
        console.log(`Playing animation: ${animations[0].name}`);
        firstAction.reset().fadeIn(0.5).play(); 
      }
    }
    return () => {
    };
  }, [actions, animations, mixer]); 
  useFrame((state, delta) => {
    mixer.update(delta);
  });
  return <primitive ref={group} object={scene.clone()} {...props} />;
};

export default RobotModels;