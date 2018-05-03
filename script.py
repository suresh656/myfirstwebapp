from flask import Flask, render_template, jsonify, request
#from werkzeug.wrappers import Request, Response

app =Flask(__name__)

#@Request.application
#def application(request):
#    return Response('Hello World!')
#
#
@app.route('/plot/')
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, output_file, show
    from bokeh.embed import components
    from bokeh.resources import CDN

    start=datetime.datetime(2016,10,1)
    end=datetime.datetime(2017,3,10)

    df=data.DataReader(name="GOOG",data_source="google",start=start,end=end)

    df_bull=df[df.Close>=df.Open]
    df_bear=df[df.Open>df.Close]

    p=figure(x_axis_type='datetime', height=300, width=1000,title='Candlestick Chart',sizing_mode='scale_width')
    #p.grid.grid_line_alpha=0.5
#hi
    hours_12=12*60*60*1000

    p.segment(df.index, df.High, df.index, df.Low, color='black')
    p.rect(x=df_bull.index,y=((df_bull.Open+df_bull.Close)/2),
           width=hours_12,height=abs(df_bull.Close-df_bull.Open),color='#CCFFFF',line_color='black')

    p.rect(x=df_bear.index,y=((df_bear.Open+df_bear.Close)/2),
           width=hours_12,height=abs(df_bear.Open-df_bear.Close),color='#FF3333',line_color='black')

    script1,div1=components(p)
    cdn_js=CDN.js_files[0]
    cdn_css=CDN.css_files[0]
    return render_template("plot.html",
    script1=script1, div1=div1,cdn_css=cdn_css,cdn_js=cdn_js)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/get/',methods=["GET"])
def geti():
    resp = {"username": "kkk"}
    return jsonify(resp)

@app.route('/ost/',methods=["POST"])
def posti():
    responseId = request.json["responseId"]
    #session = request.json["session"]
    #querytext = request.json["querytext"]
    #mobilenumber = request.json["mobilenumber"]
    respo = {"fulfillmentText": "This is the response","fulfillmentMessages": [],"source": "example.com","payload": {},"outputContexts": [ ],"followupEventInput": {}}
    return jsonify(respo)

@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/policy/')
def policy():
    return render_template("policy.html")

if __name__ == "__main__":
    app.run(debug=True)
    #from werkzeug.serving import run_simple
    #run_simple('localhost', 4000, application)
