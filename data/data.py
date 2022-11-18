import json
import mysql.connector
import re


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="taipei_day_trip"
)

with open("taipei-attractions.json", mode="r", encoding="utf-8") as file:
    data=json.load(file) 

attractions_info=data["result"]["results"]
for info in attractions_info:
    name=info["name"]
    category=info["CAT"]
    description=info["description"]
    address=info["address"]
    transport=info["direction"]
    mrt=info["MRT"]
    lat=info["latitude"]
    lng=info["longitude"]
    #圖片處理
    files=info["file"]
    file_split_url=files.split("https")
    images=[]
    for url in file_split_url:
        if "jpg" in url:
            images.append("https"+url)
        elif "JPG" in url:
            images.append("https"+url)
        elif "png" in url:
            images.append("https"+url)
        elif "PNG" in url:
            images.append("https"+url)
    images=str(images) #轉為字串
    mycursor = mydb.cursor()
    sql='INSERT INTO sites (name, category, description, address, transport, mrt, lat, lng, images) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    val=(name, category, description, address, transport, mrt, lat, lng, images)
    mycursor.execute(sql, val)
    mydb.commit()

