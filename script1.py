from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "My website goes here. Homepage"

@app.route('/about/')
def about():
    return "This is my About Page"

@app.route('/page1/')
def page1():
    return render_template("page1.html")

@app.route('/page2/')
def page2():
    return render_template("page2.html")

@app.route('/home/')
def navigation():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
