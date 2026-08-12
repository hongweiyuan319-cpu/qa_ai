import sqlite3 
from flask import Flask, jsonify, request
from flask_cors import CORS  # 允许前端跨域访问
from werkzeug.security import check_password_hash, generate_password_hash #引入哈希
from validate_data import validate_register_input
from validate_data import check_username_exists
import jwt
import datetime


#1. 开启跨域
app = Flask(__name__) #创建一个Flask网页服务器的实例，用__name__和该文件捆绑
CORS(app) #给刚刚创建的 app 跨域，此时这个后端变成了“允许来自任何网址、任何前端的跨域请求”的状态


#2. 初始化 SQLite 数据库（自动建表）
def init_db():
    conn = sqlite3.connect("database.db") #创建：在SQLite中，创建数据库和连接数据库是同一个动作，当写完这个代码，python就会在app.py所在的同级目录下生成database.db的文件
    cursor = conn.cursor()#之前的conn是连接数据库，现在的cursor是相当于申请增删改查操作权限
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT NOT NULL,
            password TEXT NOT NULL
            )
        """)#创建一个叫user的表，如果表已经存在，就不要重复创建(第一列叫ID，存整数，作为唯一主键，并且自动递增；第二列叫username，存文本，不能为空；第三列叫password，存文本，不能为空)

    conn.commit() #提交并保存
    conn.close() #关闭

#功能1: 存数据，当填入账号密码并且点击注册后，后端要把数据写入数据库
#功能2: 查数据，登录的时候，后端要进入数据库核对数据


#3. 注册接口(POST)
@app.route("/api/register",methods=["POST"]) #当客户端向服务器发送请求，访问/api/register路径时，会触发下面定义的函数来处理，只接受 POST 请求：
#客户端是发起请求的一方，服务器是响应请求的一方
def register():
    data = request.get_json() #从request里面拿到JSON数据
    if not data:
        return jsonify({"message": "请求内容不能为空，请传入JSON数据", "code": 400}), 400
    username = data.get("username")
    password = data.get("password")


    error_message, status_code = validate_register_input(username, password)
    if error_message:
        return jsonify({"message": error_message, "code": status_code}), status_code

    if check_username_exists(username):
        return jsonify({"message": "该用户名已被注册", "code": 400}), 400


    hashed_password = generate_password_hash(password)## 存入数据库的是 hashed_password，而不是明文 password

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:#尝试执行
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username,hashed_password),
        )#把新用户的 username 和 password 写入数据库的 users 表中
        conn.commit()
    except Exception as e:#捕获异常
        return(
            jsonify({"message": f"注册失败: {str(e)}", "code": 500}),500,
        )#如果写入失败（比如用户名已存在、数据库报错），则捕获错误，返回 500 错误状态码和失败原因
    finally:
        conn.close()

    return jsonify({"message": "注册成功", "code": 200}), 200 #这里只会在try完成之后执行，二expect发生不执行

# jsonify是Flask框架的一个工具函数，专门用来把Python的数据转换成JSON格式，并打包冲HTTP响应发送给客户端
# jsonify({...}), 200
    # jsonify({"message": "注册成功", "code": 200})：
        # 括号里是一个Python字典，包含了想告诉客户端的信息，jsonify 会把它转换成标准的 JSON 字符串（前后端数据交互的通用语言）
        # 内层200是给代码逻辑看的，代表代码的功能本身实现了
    # , 200：
        # 这是 HTTP 状态码。200 代表请求成功
        # 外层200给浏览器看，表示网络请求本身是通畅的

# SQLite
    # KEY表示列名，如 username、password
    # PRIMARY KEY: 数据的唯一身份证号。用来标识某一行数据绝不重复（比如每个用户的 ID），不能为空
    # AUTOINCREMENT: 让数据库自动编号。每插入一条新数据，这个数字自动加 1（比如 1、2、3...），不用手动输入


# 4. 登录接口(POST)
@app.route("/api/login",methods=["POST"])
def login():
    data = request.get_json() #把客户端发来的JSON格式数据读取后转换成Python字典，方便后续使用
    if not data:
        return jsonify({"message": "请求内容不能为空，请传入JSON数据", "code": 400}), 400
    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect("database.db")

    conn.row_factory = sqlite3.Row   # 让查询结果支持用列名取值

    
    cursor = conn.cursor()
    # 【关键修改】只根据 username 去数据库把这个人的信息全查出来
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
# SELECT * FROM users：从users里面查询并获取符合条件的所有数据
# WHERE username = ? AND password = ? ：查询条件是——用户名和密码必须同时与传入的变量（username, password）相匹配
# WHERE本身必须要求找到符合要求的必须是同一“行”
# ？赋值顺序按照出现顺序对应
# WHERE username = ? AND password = ? 中的username和password都是列名
    user = cursor.fetchone() #获取查询结果，查询结果可能有很多条，但是fetchone只看第一条
    conn.close()

# execute：在数据库内部生成了一个临时的“查询结果集”
# fetchone：从这个临时结果集里抓取第一条数据
# close（关闭连接）：这个临时结果集和操作通道一起被销毁，释放内存

    if user and check_password_hash(user["password"], password):
        access_token = generate_token(username)
    # user 的结构是：(id, username, password_hash)
        return jsonify({"message": "登录成功", "code": 200,"access_token" : access_token,}), 200
    else:
        return jsonify({"message":"登录失败", "code":400}),400


if __name__ == "__main__":#判断当前文件是不是被直接运行的。如果是，才执行下面的代码。
    init_db()
    print("后端服务器已启动，正在监听 http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)#正式启动 Web 服务器，监听本地的 5000 端口，等待前端发请求进来

#debug=True：开启调试模式。代码修改保存后，服务器会自动重启，不需要手动重启；如果代码报错，网页上会直接显示详细的错误信息，方便排查问题。
#port=5000：指定服务器运行的端口号。
    #意思是让后端程序在电脑的 5000 端口上监听请求
    #前端访问时也需要把请求发到这个端口。
    #5000是Flask的默认端口，类似于HTTP默认的80端口



# 5. JTW生成Token
# 新增服务器私钥
SECRET_KEY = "my_super_secret_key_123"
# HTTPS加密逻辑：
    # 默认加密：之前的临时密钥是一次性的，用完就销毁
    # 长期密钥：服务器用长期密钥配合算法加密计算生成 Token，然后Token本身有过期时间，在过期时间内，服务器不用存Token，只需要用本地的产期密钥用算法核算即可

def generate_token(username):
    """
    接收用户名，生成并返回一个 JWT 通行证字符串
    """
    payload = {
        "username": username,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2) # 2小时后过期
    }#这段代码在打包生成Token需要包含的核心数据
    # "username": username：在记录是谁登录的，方便服务器以后通过这个 Token 知道当前操作的用户是谁
    # "exp": ...：设置token的过期时间，过这个时间之后Token会自动失效，用户需要重登录

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


# 6. 检验Token
def verify_request_token():
    auth_header = request.headers.get("Authorization")#获取客户端（浏览器）发来的请求头中的认证信息
    # request.headers：获取这次请求的所有头部（Header）信息
    # .get("Authorization")：从中提取名为 "Authorization" 的字段。这个字段通常装着用户的“通行证”（Token），也就是前端发请求时用来证明自己身份的关键凭证。
    if not auth_header or not auth_header.startswith("Bearer "): #如果Token不存在或者Token格式不标准（Authorization的标准格式是：Bearer + Token）
        return None, "缺少有效通行证"

    token = auth_header.split(" ")[1]#以空格为界限，把字符串切开取第二个元素（Bearer + Token 中取 Token）
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])#用长期密钥（SECRET_KEY）去检查 Token 是否合法：
        return payload.get("username"), None # 成功：返回用户名和空错误
    except jwt.ExpiredSignatureError:
        return None, "通行证已过期"
    except jwt.InvalidTokenError:
        return None, "无效的通行证"


@app.route("/api/user/profile", methods=["GET"])
def get_user_profile():#检验开始
    current_user, error_msg = verify_request_token()
    if error_msg:
        return jsonify({"message": error_msg, "code": 401}), 401
    return jsonify(
      {"message": f"成功获取 {current_user} 的个人信息", "code": 200}
  ), 200