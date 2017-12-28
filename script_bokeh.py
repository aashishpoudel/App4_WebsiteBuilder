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

@app.route('/plot/')
def plot():
    import pandas
    from bokeh.plotting import figure, output_file, show
    from pandas_datareader import data
    import datetime
    from bokeh.models import HoverTool
    from bokeh.embed import components
    from bokeh.resources import CDN

    hover = HoverTool(tooltips=[
        ("index", "$index"),
        ("(x,y)", "($x, $y)"),
        ("desc", "@desc"),
    ])

    startdate = datetime.datetime(1998,3,1)
    enddate = datetime.datetime(2017,3,1)
    ticker = "QCOM"
    df = data.DataReader(name=ticker,data_source="yahoo",start=startdate,end=enddate)

    def status(close, open):
        if close>open:
            Status="Increase"
        else:
            Status="Decrease"
        return Status

    df["Status"]=[status(c,o) for c,o in zip(df.Close,df.Open)]
    df["Middle"] = (df.Open+df.Close)/2
    df["Height"] = df.Close-df.Open

    print(df)
    title = ticker + " Chart (" + str(startdate)+" to "+str(enddate)+")"
    p = figure(x_axis_type="datetime",plot_height=500, plot_width=1000, title=title)
    #p.rect(df.index,df["Close"], width=0.2, height=5, size=2.0)
    hours_12 = 12*60*60*1000
    p.rect(df.index[df.Status=="Increase"], df.Middle[df.Status=="Increase"], width=hours_12, height=abs(df.Height[df.Status=="Increase"]), color="blue")
    p.rect(df.index[df.Status=="Decrease"], df.Middle[df.Status=="Decrease"], width=hours_12, height=abs(df.Height[df.Status=="Decrease"]), color="red")
    # p.segment(x1,y1,x2,y2)
    p.segment(df.index, df.High, df.index,df.Low, color="Black")
    # output_file("web_flask_finance_plot.html")
    # show(p)
    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]
    return render_template("plot.html",
    script1=script1,
    div1=div1,
    cdn_css=cdn_css,
    cdn_js=cdn_js)

if __name__ == "__main__":
    app.run(debug=True)
