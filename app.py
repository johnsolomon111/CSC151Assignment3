from flask import Flask, render_template, request, url_for, redirect
import mysql.connector
from mysql.connector import errorcode
from forms import forms, Course, SearchForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfgh'

mydb = mysql.connector.connect(user='root',password='jonsol109811',host="127.0.0.1",database='studentdb')

mycursor = mydb.cursor(dictionary=True)

@app.route('/', methods=['POST','GET'])
def index():
	searchForm = SearchForm()
	mycursor.execute("SELECT * FROM student JOIN course ON student.course_code=course.course_code")
	data = mycursor.fetchall()
	return render_template('index.html', data=data, title='Assignment3', searchForm=searchForm)

@app.route('/add',methods=['POST','GET'])
def add():
	form = forms(request.form)
	if request.method == 'POST':
		idnumber = request.form['idnumber']
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		gender = request.form['gender']
		year = request.form['year']
		code = request.form['code']
		val = (idnumber,firstname,lastname,gender,code,year)
		sql = "INSERT INTO student (id,firstname,lastname,gender,course_code,year) VALUES (%s,%s, %s, %s, %s, %s)"
		mycursor.execute(sql, val)
		mydb.commit()
		return redirect(url_for('index'))
	return render_template('addform.html',form=form , title='Add')

@app.route('/delete/<id>', methods=['POST', 'GET'])
def delete(id):
	sql = "DELETE FROM student WHERE id='"+id+"'"
	# val = (id)
	mycursor.execute(sql)
	mydb.commit()
		
	return redirect(url_for('index'))

@app.route('/update/<id>', methods=['POST', 'GET'])
def update(id):
	sql1 = "SELECT * FROM student WHERE id= '"+id+"'"
	mycursor.execute(sql1)
	data = mycursor.fetchone()
	print data

	form = forms(request.form)
	if request.method == 'POST':
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		gender = request.form['gender']
		code = request.form['code']
		year = request.form['year']
		val = (firstname,lastname,gender,code,year)
		sql = "UPDATE student SET firstname=%s,lastname=%s,gender=%s,course_code=%s,year=%s WHERE id='"+id+"'"
		mycursor.execute(sql, val)
		mydb.commit()
		return redirect(url_for('index'))
 
	return render_template('update.html', form=form, data=data)

# *************COURSES*****************************************************************

@app.route('/course', methods=['POST','GET'])
def course():
	searchForm = SearchForm()
	mycursor.execute("SELECT * FROM course")
	data = mycursor.fetchall()
	mydb.commit()
	return render_template('courselist.html',title='Course List', data=data, searchForm=searchForm)

@app.route('/addcourse', methods=['GET', 'POST'])
def addcourse():
	form = Course(request.form)
	if request.method == 'POST':
		course = request.form['course']
		code = request.form['code']
		val = (course,code)
		sql = "INSERT INTO course (course_name,course_code) VALUES (%s, %s)"
		mycursor.execute(sql, val)
		mydb.commit()
		return redirect('course')

	return render_template('addcourse.html', form=form, title='Add Course')

@app.route('/deletecourse/<id>', methods=['POST', 'GET'])
def deletecourse(id):
	sql = "DELETE FROM course WHERE course_code= '"+id+"'"
	sql1 = "DELETE FROM student WHERE course_code= '"+id+"'"
	mycursor.execute(sql1)
	mycursor.execute(sql)
	mydb.commit()
		
	return redirect(url_for('course'))
# @app.route('/updatecourse/<id>', methods=['POST', 'GET'])
# def updatecourse(id):
# 	sql1 = "SELECT course_name,course_code FROM course WHERE course_code='"+id+"'"
# 	mycursor.execute(sql1)
# 	data = mycursor.fetchone()
# 	sql2 = "SELECT * FROM student WHERE course_code = '"+id+"'"	
# 	data2 = mycursor.fetchall()

# 	form = Course(request.form)
# 	if request.method == 'POST':
# 		course = request.form['course']
# 		code = request.form['code']
# 		val = (course,code)
# 		sql = "UPDATE course SET course_name=%s,course_code=%s WHERE course_code='"+id+"'"
# 		sql3 = "UPDATE student SET course_code=%s WHERE course_code= '"+id+"'"
# 		mycursor.execute(sql, val)
# 		mydb.commit()
# 		mycursor.execute(sql3,code)
# 		mydb.commit()
# 		return redirect(url_for('course'))
 
# 	return render_template('updatecourse.html', form=form, data=data)

@app.route('/search', methods=['POST', 'GET'])
def search():
	searchForm = SearchForm()
	if request.method == 'POST' and searchForm.validate_on_submit():
		student = request.form['student']
		sql = '''SELECT * FROM student JOIN course ON student.course_code=course.course_code WHERE firstname LIKE "%'''+student+'''%" or lastname LIKE "%'''+student+'''%"'''
		mycursor.execute(sql)
		result = mycursor.fetchall()
		return render_template('searchresults.html',title='Search Results', searchForm=searchForm, result=result)
	return render_template('index.html', searchForm=searchForm)

@app.route('/searchcourse', methods=['POST', 'GET'])
def searchcourse():
	searchForm = SearchForm()
	if request.method == 'POST' and searchForm.validate_on_submit():
		course = request.form['course']
		sql = '''SELECT * FROM course WHERE course_name LIKE "%'''+course+'''%" or course_code LIKE "%'''+course+'''%"'''
		mycursor.execute(sql)
		result = mycursor.fetchall()
		print result
		return render_template('courseresults.html',title='Course Results', searchForm=searchForm, result=result)
	return render_template('courselist.html', searchForm=searchForm)

if __name__ == '__main__':
	app.run(debug=True)
