from flask import Flask

from auth_routes import auth_bp
from base_functions import CreateTableIfNotExist
from db import GetConnection
from weather_routes import weather_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(weather_bp)


if(__name__ == "__main__"):
    # conn=GetConnection()
    # cursor=conn.cursor()
    # cursor.execute("drop table if exists posted_user_map")
    # cursor.execute("drop table if exists usersubmitted")
    # cursor.execute("drop table if exists users")
    # cursor.execute("drop table if exists weather")
    # conn.commit()
    # conn.close()
    CreateTableIfNotExist()
    app.run(host="0.0.0.0",debug=True,port=5000)
