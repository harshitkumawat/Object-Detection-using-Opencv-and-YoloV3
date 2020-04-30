from flask import Flask,render_template,request,redirect
import pymysql

app = Flask(__name__)
UPLOAD_FOLDER = './media'
app.config['MEDIA FOLDER'] = UPLOAD_FOLDER 


con = pymysql.connect('localhost','root','','object_detection')
cur = con.cursor()


@app.route('/feed',methods = ['POST','GET'])
def feed():
	if request.method=='GET':
		return render_template("showobjects.html",flag=1)

@app.route('/',methods = ['POST','GET'])
def login():
	if request.method=='GET':
		return render_template("index.html")
	elif request.method=='POST':
		if request.form['email']=="123@gmail.com":
			if request.form['password']=="12345":
				return redirect("/feed")
			else:
				return render_template("index.html",error="Invalid Password..")
		else:
			return render_template("index.html",error="Invalid email..")


@app.route('/showobjects',methods=['POST','GET'])
def showobjects():
	if request.method=='POST':
		date = request.form['date']
		time = request.form['time']
		object_ = request.form['choices-single-defaul']
		if object_ == "All":
			cur.execute("select * from objects_count where Date = %s and Time like %s",(date,time+'%'))
			data = cur.fetchall()
			if len(data)==0:
				return render_template("showobjects.html",flag=1,message = "Empty")
			return render_template("showobjects.html",flag=0,data=data,objects = "All")
		else:
			query = "select Date,Time,"+object_+",Frame from objects_count where Date = %s and Time like %s"
			cur.execute(query,(date,time+'%'))
			data = cur.fetchall()
			return render_template("showobjects.html",flag=0,data=data,objects = object_)
	else:
		return render_template("showobjects.html",flag=1,message = "Empty")		
	



if __name__ == '__main__':
    app.run()