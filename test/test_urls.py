import pytest
import requests

def test_home():
    r = requests.head('http://127.0.0.1:5000/')
    assert r.status_code == 200
    
def test_intro():
    r = requests.head('http://127.0.0.1:5000/Introduction')
    assert r.status_code == 200

def test_theory():
    r = requests.head('http://127.0.0.1:5000/Theory')
    assert r.status_code == 200

def test_obj():
    r = requests.head('http://127.0.0.1:5000/Objective')
    assert r.status_code == 200

def test_exp():
    r = requests.head('http://127.0.0.1:5000/Experiment')
    assert r.status_code == 200

def test_quiz():
    r = requests.head('http://127.0.0.1:5000/Quiz')
    assert r.status_code == 200

def test_proc():
    r = requests.head('http://127.0.0.1:5000/Procedure')
    assert r.status_code == 200

def test_rand():
    r = requests.head('http://127.0.0.1:5000/random_link')
    assert r.status_code == 404