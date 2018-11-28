from flask import Flask, render_template

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

@app.route('/search/<tags>')
def search(tags):
    return render_template("search.html", tags = tags.split('+'))

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/teamMember')
def team():
    return render_template("teamMember.html")

if __name__ == "__main__":
    app.run()
