from flask import Flask, render_template
from flask import request
import music

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template("welcome.html")

@app.route('/welcome')
def welcome2():
    return render_template("welcome.html")

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/foo', methods=['POST'])
def foo():
    names = request.form.get('names')
    output1 = music.get_songs(names)
    return render_template('search.html', output = output1)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/teamMember')
def team():
    return render_template("teamMember.html")

if __name__ == "__main__":
    app.run()
