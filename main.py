from flask import request, Response
import pandas as pd
from io import BytesIO
import base64

from app_1 import app


list_Lessons = []
list_Average = []

@app.route("/")
def Home():
    return app.send_static_file("Home page.html")

@app.route("/",methods=["POST"])
def read_Excel():
    body = request.get_json()
    Excel_data = pd.read_excel(BytesIO(base64.b64decode(body["Bytes"])))
    Average = 0
    for lesson in range(len(Excel_data["نمرات"].tolist())):
        Average += Excel_data["نمرات"].tolist()[lesson]
        list_Lessons.append((Excel_data["دروس"].tolist()[lesson],Excel_data["نمرات"].tolist()[lesson]))
    for scores in range(0,len(list_Lessons)-1):
        list_Average.append(((list_Lessons[scores][1]+list_Lessons[scores+1][1])/2,(list_Lessons[scores][0],list_Lessons[scores+1][0])))
    list_Average.insert(0,Average/len(list_Lessons))
    return {"page":"/total"}

@app.route("/total")
def result_page():
    return app.send_static_file("result page.html")

@app.route('/stream')
def stream():
    def eventStream():
        yield 'data: {}___{}___{}___{}\n\n'.format(list_Average[0],list_Lessons,max(list_Average[1:]),min(list_Average[1:]))
    return Response(eventStream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)