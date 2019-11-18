import wget
import apikeys as apik
import requests as req
from flask import Flask, jsonify
from flask import request
from flask import make_response
from flask_httpauth import HTTPBasicAuth
import json
import time
import hashlib
import time
from zeroconf import ServiceBrowser, Zeroconf


auth = HTTPBasicAuth()
file=''
LEDOK=False

class MyListener(object):
    def remove_service(self,zeroconf,type,name):
        print("Service %s removed" %(name,))
        global LEDOK
        LEDOK=False
    def add_service(self,zeroconf,type,name):
        info = zeroconf.get_service_info(type,name)
        print(name,info)
        global LEDOK
        LEDOK=True
        
app = Flask(__name__)

@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'secret'
    return none

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error':'Unathorized access'}),401)


@app.route('/Canvas', methods=['GET'])
@auth.login_required
def get_canvas():
    file = request.args.get('file','')
    if(file==''):
        return "request must include file name"
    else:
        name = str(file)
        r= req.get("https://vt.instructure.com/api/v1/courses/92615/files?search_term="+file+"&access_token="+apik.CANVAS_API_KEY)
        binary = r.content
        output= json.loads(binary.decode())
        wget.download(output[0]['url'])
        return "File is in current folder"
        #return str(output[0]['url'])

@app.route('/Marvel', methods=['GET'])
@auth.login_required
def get_marvel():
    story = request.args.get('story','')
    if(story==''):
        return "request must include story number"
    else:    
        name1=str(story)
        ts=str(time.time())
        message=ts+apik.private+apik.public
        h=hashlib.md5(message.encode())
        url = "http://gateway.marvel.com/v1/public/stories/"+name1+"?apikey="+apik.public+"&hash="+h.hexdigest()+"&ts="+ts
        response = req.get(url)
        with open ('Marvelstory.txt', 'w') as out:
            json.dump(response.json(), out)
        return "Saved file as Marvelstory.txt"

@app.route('/LED', methods=['GET'])
@auth.login_required
def get_color():
    if(LEDOK):
        com = request.args.get('command','')
        if(com==''):
            return "bad request"
        else:
            comarr = com.split('-')
            if(len(comarr)==3):
                status = comarr[0]
                color=comarr[1]
                intensity=comarr[2]
                url="http://pumpkin-pi.local:8081/LED?status="+status+"&color="+color+"&intensity="+intensity
                r= req.get(url)
                return "Sending"
            
            else:
                return "bad request"
    else:
        return "Haven't found LED Pi"
        
    


if __name__=='__main__':
    zeroconf = Zeroconf()
    listener = MyListener()
    browser = ServiceBrowser(zeroconf,"_http._tcp.local.",listener)
    app.run(debug=True, port="8081", host='0.0.0.0')
