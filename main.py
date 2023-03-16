import os
import openai
import datetime as dt
from twilio.rest import Client
from dotenv import load_dotenv
from flask import Flask, request, jsonify

from decouple import config as config_decouple
from config import config

def create_app(enviroment):
    app = Flask(__name__)

    app.config.from_object(enviroment)

    return app

enviroment = config['development']
if config_decouple('PRODUCTION', default=False):
    enviroment = config['production']

app = create_app(enviroment)

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
client = Client(account_sid, auth_token)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"status": 200, "message": "Hello World"})

@app.route('/test', methods=['POST'])
def test():
    data = request.get_json()
    return jsonify({"data": data, "status": 200, "Datetime": dt.datetime.now().strftime("%Y-%b-%d %H:%M:%S")})

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    # response = openai.Completion.create(
    #     model="text-davinci-003",
    #     prompt=data['q'],
    #     temperature=0.7,
    #     max_tokens=256,
    #     top_p=1,
    #     frequency_penalty=0,
    #     presence_penalty=0
    # )
    # res_string = response.choices[0].text.strip()
    # print(res_string)
    msg = client.messages.create(
        from_ = 'whatsapp:+14155238886',
        to = "whatsapp:+5491135646079",
        # body=res_string,
        body = "Hola, soy un bot de prueba",
    )
    print("SID:",msg.sid)
    return jsonify({"status": 200})


if __name__ == '__main__':
    app.run(debug=True)