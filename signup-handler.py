from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def foo():
    print("RECIEVED")
    # data = json.loads(request.data)
    # print(data)
    return "OK"

if __name__ == '__main__':
   app.run(host='0.0.0.0')