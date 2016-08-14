from flask import Flask, abort, redirect, url_for, \
    render_template

app = Flask(__name__)

@app.route('/')
def report():
    return render_template('report.html')