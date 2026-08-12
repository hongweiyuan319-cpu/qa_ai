import sqlite3


def validate_register_input(username,password):

    # 校验用户名是否为空
    if not username:
        return "用户名不能为空", 400

    # 校验密码是否为空
    if not password:
        return "密码不能为空", 400

    # 校验密码长度是否小于 6 位
    if len(password) < 6:
        return "密码长度不能少于 6 位", 400

    return None, 200


def check_username_exists(username):
    conn = sqlite3.connect("database.db")
    cursor=conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username = ?",(username,)
    )#cursor.execute() 的语法规定：传进去的查询参数必须是一个“容器”（比如元组 Tuple 或列表 List），而不能直接裸写一个变量。
    user = cursor.fetchone()
    conn.close()

    if user is None:
        return False
    else:
        return True