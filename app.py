from flask import Flask, jsonify, request, send_file

from src.base import api_ask

app = Flask(__name__)

@app.route("/ask", methods=['POST'])
def hello_world():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        body = request.json
        
        answer, audio = api_ask(**body)
        if audio:
            return jsonify(isError= False,
                        message= "Success",
                        statusCode= 200,
                        data= answer,
                        audioFile=send_file(audio)), 200
        else:
            return jsonify(isError= False,
                        message= "Success",
                        statusCode= 200,
                        data= answer), 200

    else:
        return jsonify(isError= True,
                    message= "Content-Type not supported",
                    statusCode= 400), 400
    
