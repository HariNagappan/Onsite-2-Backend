from flask import Blueprint, request

from db import GetConnection

auth_bp=Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def Login():
    conn=GetConnection()
    cursor = conn.cursor()
    data=request.get_json()
    username=data["username"]
    password = data["password"]
    print(username,password)
    cursor.execute("""SELECT username, password FROM users WHERE username = ?""", (username,))
    row=cursor.fetchone()
    if row is None:
        return {"success":False,"error_msg": "User does not exist"}
    if(row["password"] != password):
        return {"success": False,"error_msg":"Invalid Password"}
    return {"success": True,"error_msg":""}


@auth_bp.route("/signup", methods=["POST"])
def SignUp():
    conn=GetConnection()
    cursor = conn.cursor()
    data=request.get_json()
    username=data["username"]
    password = data["password"]
    cursor.execute("insert into users (username, password) values (?, ?)", (username, password))
    conn.commit()
    conn.close()
    return {"success": True,"error_msg":""}


