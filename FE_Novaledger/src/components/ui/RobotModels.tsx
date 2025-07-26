
"use client"; // Đây là Client Component

import React, { useRef } from 'react';
import { useGLTF } from '@react-three/drei';
import * as THREE from 'three'; // Import Three.js để dùng các kiểu dữ liệu nếu cần

// Cập nhật interface RobotModelsProps để bao gồm các thuộc tính
interface RobotModelsProps {
  position?: [number, number, number]; // Thêm thuộc tính position, là một tuple 3 số
  scale?: number | [number, number, number]; // Thêm thuộc tính scale, có thể là 1 số hoặc tuple 3 số
  // Bạn có thể thêm các props khác của Three.js Object3D vào đây nếu cần,
  // ví dụ như rotation?: [number, number, number];
}

// Component này sẽ tải và hiển thị mô hình robot
const RobotModels: React.FC<RobotModelsProps> = (props) => {
  // Đường dẫn đến tệp GLTF của bạn.
  // Đảm bảo tệp này nằm trong thư mục 'public'
  const { scene } = useGLTF('/robot_playground/scene.gltf');

  // useGLTF trả về một đối tượng chứa scene, materials và animations.
  // Chúng ta sẽ trực tiếp sử dụng scene.
  // clone() để tránh các vấn đề nếu bạn muốn render nhiều instance của model
  return <primitive object={scene.clone()} {...props} />;
};

export default RobotModels;