/*
pages/Register.jsx —— 注册页
流程：填账号密码 → 调后端注册接口 → 成功提示 → 跳到登录页去登录
*/
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { register } from '../api/auth';
import './auth.css';

function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();                          // 阻止表单默认刷新
    setError('');
    try {
      await register(username, password);        // 1. 调后端注册接口（成功则后端已把用户写入数据库）
      alert('注册成功！请登录');                   // 2. 简单提示成功
      navigate('/login');                        // 3. 跳到登录页去登录
    } catch (err) {
      setError(err.response?.data?.message || '注册失败，请重试');
    }
  };

  return (
    <div className="auth-page">
      <div className="brand">
        <span className="brand-logo">Q</span>
        <span className="brand-name">QA AI Agent</span>
      </div>
      <h2>注册</h2>
      <p className="subtitle">创建你的账户</p>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="用户名"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="密码（至少 6 位）"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">注册</button>
      </form>
      <p className="switch">已有账号？<Link to="/login">去登录</Link></p>
    </div>
  );
}

export default Register;
