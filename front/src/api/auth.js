/*
auth.js：专门存放"用户认证"相关的接口函数（register / login / getProfile）
每一个接口都封装成一个函数，页面调用时直接传参，不用关心请求细节。
*/

import request from '../utils/request';

// ── 注册接口 ──
// 函数形式：把"获取输入框数据"和"发送请求"分开。
// username, password：由调用方（页面）传进来的账号和密码。
// 返回：request.post(...) 返回的是一个 Promise（请求的"承诺"），
//       谁调用谁用 .then/.catch 处理成功或失败。
export function register(username, password) {
  return request.post('/api/register', {
    username,  // 简写，等价于 username: username
    password
  });
}

// ── 调用方式（这段写在页面里，不是写在这个文件里）──
// register(inputUsername, inputPassword)
//   .then(res => {
//     // res：代表服务器回传的整个响应对象（里面包含了状态码、响应头、后端返回的数据等一大堆东西）
//     // res.data：这是 Axios 的固定写法，专门用来获取后端真正返回的数据核心。
//     //            对应你后端代码里 jsonify({"message": "注册成功", "code": 200}) 传过来的那个字典
//     console.log("注册成功：", res.data);
//     alert("注册成功！");
//   })
//   .catch(err => {
//     // err.response：代表服务器虽然作出了回应，但返回的是错误状态码（如 400、500）时的响应对象
//     // err.response.data.message：专门用来获取后端返回的具体错误原因（比如"该用户名已被注册"）
//     console.log("注册失败：", err.response.data);
//     alert("注册失败：" + err.response.data.message);
//   });
