from flask import Flask, session
from datetime import timedelta
from view.userAPI import userAPI
import json

app = Flask(__name__)
app.register_blueprint(userAPI)

with open("secret_key.json")as Json:
	app.secret_key = json.loads(Json.read())["secret"]

#세션만료
@app.before_request
def make_session_permanent():
	session.permanent = True
	app.permanent_session_lifetime = timedelta(minutes= 60) #시간 설정

if __name__ == "__main__":
	app.run(host = '0.0.0.0', port = 5000, debug = True)
