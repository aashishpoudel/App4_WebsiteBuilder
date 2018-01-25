from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def root():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/pcb_project/')
def pcb_project():
    return render_template("pcb_project.html")

@app.route('/gui_automation_tool/')
def gui_automation_tool():
    return render_template("gui_automation_tool.html")

@app.route('/mirror_project/')
def mirror_project():
    return render_template("mirror_project.html")

@app.route('/mis_project/')
def mis_project():
    return render_template("mis_project.html")

@app.route('/home/')
def home():
    return render_template("home.html")

@app.route('/hidden/')
def hidden():
    return "Website in Heroku -- By Aashish Poudel"

@app.route('/financeplot/')
def financeplot():
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
    return render_template("financeplot.html",
    script1=script1,
    div1=div1,
    cdn_css=cdn_css,
    cdn_js=cdn_js)

@app.route('/QAM_Receiver/')
def QAM_Receiver():
    import math
    import random
    import pandas
    #from bokeh.charts import Scatter
    from bokeh.plotting import figure,output_file, show
    from bokeh.models import HoverTool
    from bokeh.embed import components
    from bokeh.resources import CDN

    def Qfunc(x):
        return (1/2)*(1-math.erf(x/math.sqrt(2)))

    bits = 2
    M = bits**2
    Tb = 1 #Bit Time
    Ts = bits*Tb #Symbol Time
    Nb = 32  # sample times in Tb
    Ns = bits*Nb # sample times in Ts
    T = Ts/Ns #Sample time
    LB = 4*Ns #Buffer Time
    LBN1 = LB - Ns + 1
    Es = 2 #Energy of signal waveform
    sqEs = math.sqrt(Es)

    SNRbdBt = [0.1*j for j in range(101)] #SNR(dB) in discrete points
    SNRbt = [10**(x/10) for x in SNRbdBt] #SNR(linear) in discrete points

    if bits == 1:     K = 1
    if bits > 1:    K = 2
    BER_actual = [(K/bits)*Qfunc(math.sqrt(bits*SNRbt_1)*math.sin(math.pi/M)) for SNRbt_1 in SNRbt]

    symbols = [[0,0],[0,1],[1,0],[1,1]]
    phases = [2*math.pi/M*i for i in range(M)]

    #verified wc and t
    wc = 8*math.pi/Ts
    t = [T*i for i in range(Ns)]
    wcT = wc * T
    nd = 0

    sw = [[0 for i in t] for j in range(M)]

    #sw verfied for all 4 rows
    for m in range(M):
        sw[m] = [math.sqrt(2*Es/Ts)*math.cos(wc*t1+phases[m]) for t1 in t]
    #su and suT verfied for all 4 rows
    su = [[0 for i in t] for j in range(2)]
    suT= [[0 for i in t] for j in range(2)]
    su[0]= [math.sqrt(2/Ts)*math.cos(wc*t1) for t1 in t]
    su[1]= [-1*math.sqrt(2/Ts)*math.sin(wc*t1) for t1 in t]
    suT[0]= [math.sqrt(2/Ts)*math.cos(wc*t1)*T for t1 in t]
    suT[1]= [-1*math.sqrt(2/Ts)*math.sin(wc*t1)*T for t1 in t]

    SNRdBs = range(1,11)
    BER_calc = [0 for i in SNRdBs]
    MaxIter= 1000
    NoOfSamples = 500;

    ycos_values = [0 for i in range(NoOfSamples)]
    ysin_values = [0 for i in range(NoOfSamples)]

    SNR_for_plot = 8

    for snrIdx in range(len(SNRdBs)):
        SNRbdB = SNRdBs[snrIdx]
        SNR = 10**(SNRbdB/10)
        NO=2*(Es/bits)/SNR
        sigma_square = NO/2
        sgmsT = math.sqrt(sigma_square/T)
        sws = [0 for i in range(LB)]
        yrcvdcos = [0 for i in range(LB)]
        yrcvdsin = [0 for i in range(LB)]
        totalBitError = 0
        for k in range(MaxIter):
            rand_num = random.random()
            randIdx_Tx = math.floor(rand_num*M)
            symbolsTx = symbols[randIdx_Tx]
            for n in range(Ns):
                sws.append(sw[randIdx_Tx][n])
                sws = sws[1:len(sws)]
                wct = wcT * (n-1)
                bp_noise = random.gauss(0,1)*math.cos(wct)-random.gauss(0,1)*math.sin(wct)
                rn = sws[-1] + sgmsT*bp_noise
                yrcvdcos.append(suT[0][n]*rn)
                yrcvdcos = yrcvdcos[1:len(yrcvdcos)]
                yrcvdsin.append(suT[1][n]*rn)
                yrcvdsin = yrcvdsin[1:len(yrcvdsin)]
            ycos_integrate = sum(yrcvdcos[LBN1:LB])
            ysin_integrate = sum(yrcvdsin[LBN1:LB])

            if snrIdx==SNR_for_plot and k<300:
                ycos_values[k] = ycos_integrate
                ysin_values[k] = ysin_integrate

            #For Detecting the M-ary signal
            theta = math.atan2(ysin_integrate,ycos_integrate)
            if theta<-math.pi/M:
                theta = theta + 2*math.pi
            arguments_dict = dict()
            for m in range(M):
                arguments_dict[m] = math.fabs(theta - phases[m])
            randIdx_Rx = min(arguments_dict, key=lambda k: arguments_dict[k])
            symbolsRx = symbols[randIdx_Rx]
            bit_error = [math.fabs(a1-b1) for a1,b1 in zip(symbolsTx,symbolsRx)]
            totalBitError = totalBitError + sum(bit_error)
            # Shortening For loop itself if totalBitError>100. So all calculations per SNR shortened
            if totalBitError > 100: break
        BER_calc[snrIdx] = totalBitError/((k)*bits)


    title = "Signal Constellation Diagram for Mod_Order = " + str(M) + " and SNR = " + str(SNR_for_plot)
    output_filename = "Signal_Constellation_for_PSK.html"
    p_constellation = figure(title=title,plot_width=700, plot_height=700)
    p_constellation.scatter(ycos_values, ysin_values, marker="x", line_color="#6666ee", fill_color="#ee6666", fill_alpha=0.5, size=12)
    p_constellation.xaxis.axis_label="I Channel"
    p_constellation.yaxis.axis_label="Q Channel"
    #output_file(output_filename)
    #show(p_constellation)

    title = "Bit Error Rate for Mod_Order = " + str(M)
    p_ber = figure(title=title,plot_width=700, plot_height=700)
    p_ber.line(SNRbdBt, BER_actual, line_width=2, legend="BER_actual")
    p_ber.circle(SNRdBs, BER_calc, fill_color="white", size=5, legend="BER_calculated")
    p_ber.xaxis.axis_label="SNR in dB"
    p_ber.yaxis.axis_label="Bit Error Rate (M = " + str(M) + ")"
    p_ber.legend.location = "top_right"
    p_ber.legend.click_policy="hide"
    output_filename = "Bit_Error_Probability.html"
    #output_file(output_filename)
    #show(p_ber)
    script1, div1 = components(p_constellation)
    script2, div2 = components(p_ber)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]
    return render_template("qam_receiver.html",
    script1=script1,
    div1=div1,
    script2=script2,
    div2=div2,
    cdn_css=cdn_css,
    cdn_js=cdn_js)

if __name__ == "__main__":
    app.run(debug=True)
