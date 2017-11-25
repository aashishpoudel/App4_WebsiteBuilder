from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def root():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/hidden/')
def hidden():
    return "Website in Heroku -- By Aashish Poudel"

@app.route('/page1/')
def page1():
    return render_template("page1.html")

@app.route('/page2/')
def page2():
    return render_template("page2.html")

@app.route('/home/')
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
