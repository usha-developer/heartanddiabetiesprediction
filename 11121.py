from flask import Flask,render_template,request,redirect
from sklearn.ensemble import RandomForestClassifier
import pickle

import sqlite3



app=Flask(__name__)

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/')
def home_1():
    return render_template('home.html')

@app.route('/register.html')
def reg_user():
    return render_template('register.html')

@app.route('/registerpage',methods=['POST'])
def saveregdetails():
    if request.method=='POST':
        uname=request.form['uname']
        uemail=request.form['uemail']
        upassword=request.form['upassword']
        upassword1=request.form['upassword1']
        if (upassword==upassword1):
            with sqlite3.connect('finalheartdb.db') as con:
                cur=con.cursor()
                cur.execute('insert into reguser(username,mailid,password) values(?,?,?)',(uname,uemail,upassword))
                con.commit()
                return render_template('loginpage.html')
        else:
            return render_template('register.html')
    return render_template('register.html')
            
        
@app.route('/loginpage.html')
def login_user():
    return render_template('loginpage.html')



@app.route('/loginpage',methods=['POST'])
def saveloginvalues():

    if request.method=='POST':
        
        uname1=request.form['uname1']
        upwd=request.form['upwd']
        with sqlite3.connect('finalheartdb.db') as con:
                cur=con.cursor()
                cur.execute('select * from reguser where username=?',(uname1,))
                row=cur.fetchone()
                n1=row[1]
                p1=row[3]
                if(n1==uname1 and p1==upwd):
                    return render_template('BMI.html')
                
    return render_template('loginpage.html') 

@app.route('/bmivalue',methods=['POST','GET'])
def bmi():
    if request.method=="POST":
        c1=float(request.form['30'])
        c2=int(request.form['31'])
        c3=round(c2 / (c1 * c1),2)
        c3=str(c3)
        #return c3
        return render_template('bmiresult.html',temp=c3)
    return render_template('BMI.html')


@app.route('/BMI.html')
def bmivalue():
    return render_template('BMI.html')



@app.route('/bmiresult.html')
def bmivalueresult():
    return render_template('bmiresult.html')



@app.route('/Diabetes.html',methods=['POST','GET'])
def diabetes():
    if request.method=="POST":
        model=pickle.load(open('diabetes.pickle','rb'))
        a1=int(request.form['1'])
        a2=int(request.form['2'])
        a3=int(request.form['3'])
        a4=int(request.form['4'])
        a5=int(request.form['5'])
        a6=int(request.form['6'])
        a7=int(request.form['7'])
        s=model.predict([[a1,a2,a3,a4,a5,a6,a7]])
        if s[0]==0:
            return render_template('Diabetes__Not_Predicetd.html')
        else:
            return render_template('Diabetes_Predicetd.html')
        #else:
            #return redirect('/predict_diabetes')
    return render_template('Diabetes.html')

@app.route('/Heart.html',methods=['POST','GET'])
def heart():

    return render_template('Heart.html')

@app.route('/heartresult',methods=['POST','GET'])
def heart1():
    if request.method=="POST":
        model=pickle.load(open('heart.pickle','rb'))
        dict1={'Female':1,'Male':0,'female':1,'male':0,'FEMALE':1,'MALE':0,'yes':1,'no':0,'YES':1,'NO':0,'YES':1,'No':0}
        b1=request.form['11']
        b1=dict1[b1]
        b2=int(request.form['21'])
        b3=request.form['31']
        b3=dict1[b3]
        b4=int(request.form['41'])
        b6=request.form['61']
        b6=dict1[b6]
        b7=request.form['71']
        b7=dict1[b7]
        b8=request.form['81']
        b8=dict1[b8]
        b9=int(request.form['91'])
        b10=int(request.form['10'])
        b11=int(request.form['011'])
        b12=int(request.form['12'])
        b13=int(request.form['13'])
        d=model.predict([[b1,b2,b3,b4,b6,b7,b8,b9,b10,b11,b12,b13]])
        if d[0]==0:
            return render_template('heart_disease_not.html')
        else:
            return render_template('heart_disease.html')
        #else:
            #return redirect('/predict_diabetes')

    return render_template('Diabetes.html')

@app.route('/Doctors.html')
def doctors():
    return render_template('Doctors.html')

if __name__ == "__main__":
    app.run(debug=True)
