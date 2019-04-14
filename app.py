#!/usr/bin/python3
from flask import Flask
from flask import render_template, request
from flask import json,jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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