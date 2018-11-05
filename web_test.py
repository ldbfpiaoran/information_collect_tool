from  flask import Flask
from flask import request
from flask import redirect
import requests
import os

app = Flask(__name__)

@app.route('/',methods=['GET','POST','HEAD'])
def home():
    if request.method == 'HEAD':
        return redirect('http://family.baidu.com')
    else:
        return redirect('http://family.baidu.com')

        



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)