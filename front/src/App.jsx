/*
App.jsx —— 路由地图
作用：访问哪个网址，显示哪个页面
  /login    → 登录页
  /register → 注册页
  /         → 首页
*/
import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Home from './pages/Home';

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/" element={<Home />} />
      {/* 其他任何路径 → 都跳回首页 */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
