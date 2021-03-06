#!/usr/bin/python3
from flask import Flask
from flask import render_template, request
from flask import json, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./app.db'
db = SQLAlchemy(app)


class questions(db.Model):
    """The database model for storing questions"""
    id = db.Column(db.Integer, primary_key=True, auto_increment="True")
    ques = db.Column(db.String(500), nullable=False)
    cno = db.Column(db.Integer, nullable=False)
    op1 = db.Column(db.String(500), nullable=False)
    op2 = db.Column(db.String(500), nullable=False)
    op3 = db.Column(db.String(500), nullable=False)
    op4 = db.Column(db.String(500), nullable=False)

    def __init__(self, ques, cno, op1, op2, op3, op4):
        self.ques = ques
        self.cno = cno
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3
        self.op4 = op4


class imgs(db.Model):
    """The database model for storing image links"""
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(500), nullable=False)

    def __init__(self, name, link):
        self.name = name
        self.link = link


@app.route('/getques', methods=['GET'])
def getques():
    """
        Parameters : None
        Returns : All the questions stored in the database as a JSON Object
    """
    db.create_all()
    all_ques = questions.query.all()
    a = []
    for i in all_ques:
        s = {
            'ques': i.ques,
            'cno': i.cno,
            'op1': i.op1,
            'op2': i.op2,
            'op3': i.op3,
            'op4': i.op4
        }
        a.append(s)
    b = json.dumps(a)
    return jsonify(b)


@app.route('/checkans', methods=['GET', 'POST'])
def check():
    """
        Parameters : Gets the Users input of the MCQ's
        Returns : The questions, the corresponding correct answers, and the result of the quiz per question as a python dictionary for Jinja templating
    """
    db.create_all()
    all_ques = questions.query.all()
    ans = []
    for i in range(len(all_ques)):
        ans.append(int(request.form['ans' + str(i)]))
    res = {}
    for i in range(len(all_ques)):
        if ans[i] == all_ques[i].cno:
            res[all_ques[i].ques] = [True]
        else:
            res[all_ques[i].ques] = [False]
    for i in range(len(all_ques)):
        if all_ques[i].cno == 1:
            res[all_ques[i].ques].append(all_ques[i].op1)
        elif all_ques[i].cno == 2:
            res[all_ques[i].ques].append(all_ques[i].op2)
        elif all_ques[i].cno == 1:
            res[all_ques[i].ques].append(all_ques[i].op3)
        else:
            res[all_ques[i].ques].append(all_ques[i].op4)
    return render_template('Results.html', res=res)


@app.route('/addques', methods=['POST'])
def addques():
    """
        Parameters : Gets the inputs for adding a question to the database
        Returns : The final added question as a JSON Object
    """
    ques = request.form['ques']
    cno = int(request.form['cno'])
    op1 = request.form['op1']
    op2 = request.form['op2']
    op3 = request.form['op3']
    op4 = request.form['op4']
    db.create_all()
    new_ques = questions(ques, cno, op1, op2, op3, op4)
    db.session.add(new_ques)
    db.session.commit()
    b = {
        'ques': new_ques.ques,
        'cno': new_ques.cno,
        'op1': new_ques.op1,
        'op2': new_ques.op2,
        'op3': new_ques.op3,
        'op4': new_ques.op4
    }
    b = json.dumps(b)
    # status = type(new_ques) == questions
    return jsonify(b)


@app.route('/getimg', methods=['GET'])
def getimg():
    """
        Parameters : None
        Returns : All the image links stored in the database as a JSON Object
    """
    img = imgs.query.all()
    a = []
    for i in img:
        s = {
            'name': i.name,
            'link': i.link
        }
        a.append(s)
    a = json.dumps(a)
    return jsonify(a)


@app.route('/addimg', methods=['POST'])
def addimg():
    """
        Parameters : The image links for adding into the database
        Returns : The added image link as a JSON Object
    """
    name = request.form['name']
    link = request.form['link']
    db.create_all()
    new_img = imgs(name, link)
    db.session.add(new_img)
    db.session.commit()
    b = {
        'name': new_img.name,
        'link': new_img.link
    }
    return jsonify(b)

# Just an utility route to delete some particular entry from the database
@app.route('/del')
def delete():
    """
        Parameters : The question to be deleted
        Returns : The status code of deletion
    """
    db.create_all()
    req = questions.query.filter_by(
        ques="Estitmate the number of distinct terms in a text document: <br> Given k=10^1.64,b=0.49 and n=1000020{tokens}").first()
    db.session.delete(req)
    db.session.commit()
    a = {'stat': True}
    a = json.dumps(a)
    return jsonify(a)


@app.route('/')
def intro():
    """Renders the Introduction page"""
    return render_template('Intro.html', name=None)


@app.route('/Introduction')
def intro2():
    """Renders the Introduction page"""
    return intro()


@app.route('/Theory')
def theory():
    """Renders the Theory page"""
    return render_template('Theory.html')


@app.route('/Objective')
def objective():
    """Renders the Objective page"""
    return render_template('Objective.html')


@app.route('/Experiment')
def experiment():
    """Renders the Experiment page"""
    return render_template('Experiment.html')


@app.route('/Procedure')
def procedure():
    """Renders the Procedure page"""
    return render_template('Procedure.html')


@app.route('/Quiz', methods=['POST', 'GET'])
def quiz():
    """Renders the Quiz page"""
    return render_template('Quizzes.html')


if __name__ == "__main__":
    app.run(debug=True)
