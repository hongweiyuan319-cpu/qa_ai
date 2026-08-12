/*
auth.js：专门存放"用户认证"相关的接口函数（register / login / getProfile）
每一个接口都封装成一个函数，页面调用时直接传参，不用关心请求细节。
*/

import request from '../utils/request';

// ── 注册接口 ──
// 对应后端：POST /api/register（创建账号）
// 参数：username 账号、password 密码（由页面传入）
// 返回：request.post(...) 返回 Promise，页面用 .then/.catch 处理结果
export function register(username, password) {
  return request.post('/api/register', {
    username,  // 简写，等价于 username: username
    password
  });
}

// -- 登录接口 --
export function login(username,password){
    return request.post('/api/login',{
        username,
        password
    });
}

// -- 获取当前用户信息接口 --
// 对应后端：GET /api/user/profile（带 token 查用户）
// 特点：GET 请求，不需要传数据（token 由 request.js 的请求拦截器自动带上）
export function getProfile() {
  return request.get('/api/user/profile');
}
