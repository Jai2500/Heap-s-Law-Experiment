#!/usr/bin/python3
from flask import Flask
import json
import jsonify
from flask_sqlalchemy import SQLAlchemy
import pytest


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
db = SQLAlchemy(app)


class questions(db.Model):
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
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(500), nullable=False)

    def __init__(self, name, link):
        self.name = name
        self.link = link


def getques():
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
    # b = json.dumps(a)
    return a


def check(answer):
    db.create_all()
    all_ques = questions.query.all()
    ans = []
    for i in answer:
        ans.append(int(i))
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

    return res[all_ques[0].ques][0]


def addques(quest, cnos, ops):
    ques = quest
    cno = int(cnos)
    op1 = ops[0]
    op2 = ops[1]
    op3 = ops[2]
    op4 = ops[3]
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
    # b = json.dumps(b)
    # status = type(new_ques) == questions
    return b


def getimg():
    img = imgs.query.all()
    a = []
    for i in img:
        s = {
            'name': i.name,
            'link': i.link
        }
        a.append(s)
    # a = json.dumps(a)
    return a


def addimg(iname, ilink):
    name = iname
    link = ilink
    db.create_all()
    new_img = imgs(name, link)
    db.session.add(new_img)
    db.session.commit()
    b = {
        'name': new_img.name,
        'link': new_img.link
    }
    return b


# The below function is just an utility function that the developer has to program at his side
def delete():
    db.create_all()
    req = questions.query.filter_by(
        ques="Estitmate the number of distinct terms in a text document: <br> Given k=10^1.64,b=0.49 and n=1000020{tokens}").first()
    db.session.delete(req)
    db.session.commit()
    a = {'stat': True}
    a = json.dumps(a)
    return jsonify(a)


b = {}


def test_addques():
    global b
    quest = "This is a question"
    cnos = 1
    ops = ['op1', 'op2', 'op3', 'op4']
    a = addques(quest, cnos, ops)
    b = {
        'ques': quest,
        'cno': cnos,
        'op1': ops[0],
        'op2': ops[1],
        'op3': ops[2],
        'op4': ops[3]
    }
    # b = json.dumps(b)
    assert(a == b)


def test_nothing():
    global b
    quest = "This is a question"
    cnos = 1
    ops = ['op1', 'op2', 'op3', 'op4']
    a = addques(quest, cnos, ops)
    c = {
        'ques': quest,
        'cno': cnos,
        'op1': ops[0],
        'op2': ops[1],
        'op3': ops[2],
        'op4': ops[3]
    }
    assert(c == b)


def test_getques():
    global b
    c = [b]
    a = getques()
    for i in range(len(c)):
        assert(c[i] == a[i])


# def test_check():
#     answer = [1]
#     a = check(answer)
#     assert(a == True)

def test_addimg():
    global b
    iname = 'abc'
    ilink = 'def'
    a = addimg(iname, ilink)
    b = {
        'name': iname,
        'link': ilink
    }
    assert(a == b)


def test_getimg():
    global b
    c = [b]
    a = getimg()
    for i in range(len(c)):
        assert(c[i] == a[i])

# test_check()
