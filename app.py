#!/usr/bin/python3
from flask import Flask
from flask import render_template, request
from flask import json,jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////./app.db'
db = SQLAlchemy(app)

class questions(db.Model):
    id = db.Column(db.Integer, primary_key = True, auto_increment = "True")
    ques = db.Column(db.String(500), nullable=False)
    cno = db.Column(db.Integer, nullable=False)
    op1 = db.Column(db.String(500), nullable=False)
    op2 = db.Column(db.String(500), nullable=False)
    op3 = db.Column(db.String(500), nullable=False)
    op4 = db.Column(db.String(500), nullable=False)
    def __init__(self,ques,cno,op1,op2,op3,op4):
        self.ques = ques
        self.cno = cno
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3
        self.op4 = op4

    
@app.route('/getques', methods=['GET'])
def getques():
    db.create_all()
    all_ques =  questions.query.all()
    a = []
    for i in all_ques:
        s = {
            'ques' : i.ques,
            'cno' : i.cno,
            'op1' : i.op1,
            'op2' : i.op2,
            'op3' : i.op3,
            'op4' : i.op4
        }
        a.append(s)
    b = json.dumps(a)
    return jsonify(b)

@app.route('/checkans', methods=['POST'])
def check():
    db.create_all()
    all_ques = questions.query(questions.cno)
    ans = []
    for i in range(len(all_ques)):
        ans.append(int(request.form['ans' + str(i)]))
    res = {}
    for i in range(len(all_ques)):
        if ans[i] == all_ques[i]:
            res[str(i)]  = True
        else:
            res[str(i)] = False
    a = json.dumps(res)
    return jsonify(a)


@app.route('/')
def intro():
    return render_template('Intro.html', name = None)

@app.route('/Introduction')
def intro2():
    return intro()

@app.route('/Theory')
def theory():
    return render_template('Theory.html')

@app.route('/Objective')
def objective():
    return render_template('Objective.html')

@app.route('/Experiment')
def experiment():
    return render_template('Experiment.html')

@app.route('/Procedure')
def procedure():
    return render_template('Procedure.html')

@app.route('/Quiz', methods=['POST','GET'])
def quiz():
    return render_template('Quizzes.html')

if __name__ == "__main__":
    app.run(debug=True)