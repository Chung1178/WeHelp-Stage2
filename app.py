from flask import *
import mysql.connector
import ast
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345678",
  database="taipei_day_trip"
)

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

# 旅遊景點API
@app.route("/api/attractions", methods=["GET"])
def get_attractions_info():
	page=request.args.get("page", 0)
	page=int(page)
	keyword=request.args.get("keyword", None)
	mycursor = mydb.cursor()
	try:
		if keyword != None:
			offset=page*12
			sql="SELECT * FROM sites WHERE category=%s OR name LIKE %s ORDER BY id LIMIT %s, 12"
			val=(keyword, "%"+keyword+"%", offset)
			mycursor.execute(sql, val)
			attractions_info=mycursor.fetchall()
			data=[
				{
				"id":id,
				"name":name,
				"category":category,
				"description":description,
				"address":address,
				"transport":transport,
				"mrt":mrt,
				"lat":float(lat),
				"lng":float(lng),
				"images":ast.literal_eval(images)
				}
				for id, name, category, description, address, transport, mrt, lat, lng, images in attractions_info
				]
			#處理nextPage
			sql="SELECT COUNT(id) FROM sites WHERE category=%s OR name LIKE %s"
			val=(keyword, "%"+keyword+"%")
			mycursor.execute(sql, val)
			total_attractions_num=mycursor.fetchone()
			total_attractions_num=total_attractions_num[0]
			total_pages=total_attractions_num/12
			if page+1 < total_pages:
				nextPage=page+1
				return jsonify({"data":data, "nextPage":nextPage})
			elif page+1 >= total_pages:
				nextPage=None
				return jsonify({"data":data, "nextPage":nextPage})
		elif keyword == None:
			offset=page*12
			sql="SELECT * FROM sites ORDER BY id LIMIT %s, 12"
			val=(offset,)
			mycursor.execute(sql, val)
			attractions_info=mycursor.fetchall()
			data=[
				{
				"id":id,
				"name":name,
				"category":category,
				"description":description,
				"address":address,
				"transport":transport,
				"mrt":mrt,
				"lat":float(lat),
				"lng":float(lng),
				"images":ast.literal_eval(images)
				}
				for id, name, category, description, address, transport, mrt, lat, lng, images in attractions_info
				]
			#處理nextPage
			sql="SELECT COUNT(id) FROM sites"
			mycursor.execute(sql)
			total_attractions_num=mycursor.fetchone()
			total_attractions_num=total_attractions_num[0]
			total_pages=total_attractions_num/12
			if page+1 < total_pages:
				nextPage=page+1
				return jsonify({"data":data, "nextPage":nextPage})
			elif page+1 >= total_pages:
				nextPage=None
				return jsonify({"data":data, "nextPage":nextPage})
	except Exception:
		err_json_message={"error": True, "message": "Server Error"}
		return jsonify(err_json_message)

# 報錯設定
@app.errorhandler(400)
def Bad_request(e):
    return jsonify({"error": True, "message": "Bad request"}), 400	

# 旅遊景點API
@app.route("/api/attraction/<attractionID>", methods=["GET"])
def get_attractions_byID(attractionID):
	mycursor = mydb.cursor()
	if str(attractionID).isdigit() is False:
		abort(400)
	try:
		if str(attractionID).isdigit() is True:
			sql="SELECT * FROM sites WHERE id=%s "
			val=(attractionID,)
			mycursor.execute(sql, val)
			attraction_info=mycursor.fetchone()
			if attraction_info is None:
				return jsonify({"data":None})
			else:
				id=attraction_info[0]
				name=attraction_info[1]
				category=attraction_info[2]
				description=attraction_info[3]
				address=attraction_info[4]
				transport=attraction_info[5]
				mrt=attraction_info[6]
				lat=float(attraction_info[7])
				lng=float(attraction_info[8])
				images=ast.literal_eval(attraction_info[9])
				data={"data":{
					"id":id,
					"name":name,
					"category":category,
					"description":description,
					"address":address,
					"transport":transport,
					"mrt":mrt,
					"lat":lat,
					"lng":lng,
					"images":images
					}}
				return jsonify(data)
	except Exception:
		err_json_message={"error": True, "message": "Server Error"}
		return jsonify(err_json_message)

# 旅遊景點分類API
@app.route("/api/categories", methods=["GET"])
def get_attractions_categories():
	mycursor = mydb.cursor()
	try:
		mycursor.execute("SELECT DISTINCT category FROM sites")
		categories=mycursor.fetchall()
		category_list=list(map(''.join, categories))
		return jsonify({"data":category_list})
	except Exception:
		err_json_message={"error": True, "message": "Server Error"}
		return jsonify(err_json_message)


app.run(port=3000)