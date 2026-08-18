/* 这个文档专门用于处理token：
登录成功 ──→ ① 存储：localStorage.setItem('token', ...)
               │
刷新页面 ──→ ② 读取：初始化时从 localStorage 读，恢复登录态
               │
发请求   ──→ ③ 使用：request.js 拦截器自动带上
               │
退出/过期─→ ④ 销毁：localStorage.removeItem('token')
*/

//1. createContext() ：造一个共享容器，**建公告栏**
import { createContext, useState, useContext } from 'react';
const AuthContext = createContext(null);   // 造一个空盒子，默认空（null）
//createContext(null) = 引入后，造一个空的共享盒子，null 是它的默认空内容。盒子本身不干活，等 Provider 放数据、useContext 取数据

//2. AuthProvider ：管数据、提供登录/登出方法，**管理员**
export function AuthProvider({ children }){
    // 先放“登录状态”：user = 当前登录态
    const [user, setUser] = useState(//声明一个状态 user，括号里是它的初始值
        () => localStorage.getItem('token')//一个函数，专门负责去取初始值
    );

//3. 登录方法
    const login = (token) => {
        localStorage.setItem('token',token); //① 抄进笔记本（刷新不丢）
        setUser(token)// ② 点亮已登录灯（页面立刻变）
    };

    const logout = () => {
        localStorage.removeItem('token');//① 撕掉笔记本上的 token
        setUser(null);// ② 关掉"已登录"灯 → 页面立刻变未登录
    }

// Provider 组件负责把数据传递给子组件
    return(
        <AuthContext.Provider value = {{ user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}
//5. useAuth() ：**看板工具**——任何页面一行代码就能拿到公告栏内容
// eslint-disable-next-line react-refresh/only-export-components
export function useAuth() {
    return useContext(AuthContext); // 去公告栏看一眼，把贴的 value 整个拿回来
}