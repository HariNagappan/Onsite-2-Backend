from flask import Blueprint, request, jsonify

from base_functions import NumberOfDays
from db import GetConnection

weather_bp=Blueprint("weather",__name__)

@weather_bp.route("/weather/today")
def GetTodayWeather():
    city=request.args.get("city")
    conn=GetConnection()
    cursor=conn.cursor()
    cursor.execute("select * from weather where city=?",(city,))
    all_cities=cursor.fetchall()
    conn.close()
    for row in all_cities:
        print(NumberOfDays(row["created_at"]))
    return list(dict(row) for row in filter(lambda row: NumberOfDays(row["created_at"])<1, all_cities))

@weather_bp.route("/weather",methods=["POST"])
def PostWeatherData():
    data= request.get_json()
    city=data["city"]
    pincode=data["pincode"]
    temperature=data["temperature"]
    humidity=data["humidity"]
    username=data["username"]
    conn=GetConnection()
    cursor=conn.cursor()
    cursor.execute("select user_id from users where username=?",(username,))
    user_id=cursor.fetchone()["user_id"]
    cursor.execute("select weather.created_at from weather join posted_user_map on weather.post_id=posted_user_map.post_id where user_id=? and city=?",(user_id,city))
    submitlst=cursor.fetchall()
    for row in submitlst:
        if(NumberOfDays(row["created_at"])<1):
            return {"success": False,"error_msg":"Max entries limit reached for current city"}
    cursor.execute("insert into weather(city,pincode,temperature,humidity) values(?,?,?,?)",(city,pincode,temperature,humidity))
    cursor.execute("select post_id from weather order by post_id DESC ")
    cur_post_id=cursor.fetchone()["post_id"]
    cursor.execute("insert into posted_user_map(post_id,user_id) values(?,?)",(cur_post_id,user_id))

    conn.commit()
    conn.close()
    return {"success": True,"error_msg":""}

@weather_bp.route("/weather/history",methods=["GET"])
def GetWeatherHistory():
    conn=GetConnection()
    cursor=conn.cursor()
    city=request.args.get("city")
    days=int(request.args.get("days"))
    cursor.execute("select * from weather where city=?",(city,))
    all_cities_weather=cursor.fetchall()
    all_cities_weather=filter(lambda row: NumberOfDays(row["created_at"])<=days, all_cities_weather)
    return list(dict(row) for row in all_cities_weather)

@weather_bp.route("/weather/<int:post_id>",methods=["DELETE"])
def DeleteWeather(post_id):
    conn=GetConnection()
    cursor=conn.cursor()
    cursor.execute("delete from posted_user_map where post_id=?", (post_id,))
    cursor.execute("delete from weather where post_id=?",(post_id,))
    conn.commit()
    conn.close()
    return {"success": True,"error_msg":""}

@weather_bp.route("/userposts",methods=["GET"])
def GetUserPosts():
    conn=GetConnection()
    cursor=conn.cursor()
    username=request.args.get("username")
    cursor.execute("select user_id from users where username=?", (username,))
    user_id=cursor.fetchone()["user_id"]
    cursor.execute("select post_id from posted_user_map where user_id=?",(user_id,))
    all_post_ids=cursor.fetchall()
    lst=[]
    for row in all_post_ids:
        cursor.execute("select * from weather where post_id=?",(row["post_id"],))
        fetchone=cursor.fetchone()
        lst.append(dict(fetchone))
    return lst