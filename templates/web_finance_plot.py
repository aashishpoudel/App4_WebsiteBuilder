import pandas
from bokeh.plotting import figure, output_file, show
from pandas_datareader import data
import datetime
from bokeh.models import HoverTool
from bokeh.resources import CDN

hover = HoverTool(tooltips=[
    ("index", "$index"),
    ("(x,y)", "($x, $y)"),
    ("desc", "@desc"),
])

start = datetime.datetime(1998,3,1)
end = datetime.datetime(2017,3,1)
df = data.DataReader(name='QCOM',data_source="yahoo",start=start,end=end)

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

p = figure(x_axis_type="datetime",plot_height=500, plot_width=1500, title="CandleStick Chart")
#p.rect(df.index,df["Close"], width=0.2, height=5, size=2.0)
hours_12 = 12*60*60*1000
p.rect(df.index[df.Status=="Increase"], df.Middle[df.Status=="Increase"], width=hours_12, height=abs(df.Height[df.Status=="Increase"]), color="blue")
p.rect(df.index[df.Status=="Decrease"], df.Middle[df.Status=="Decrease"], width=hours_12, height=abs(df.Height[df.Status=="Decrease"]), color="red")
# p.segment(x1,y1,x2,y2)
p.segment(df.index, df.High, df.index,df.Low, color="Black")
output_file("web_finance_plot.html")
show(p)
