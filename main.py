from flask import Flask, session
from datetime import timedelta
from view.userAPI import userAPI
from view.postAPI import postAPI
from view.portAPI import portAPI
from view.commentAPI import commentAPI
from view.mypageAPI import mypageAPI
import json

app = Flask(__name__)
app.register_blueprint(userAPI)
app.register_blueprint(postAPI)
app.register_blueprint(portAPI)
app.register_blueprint(commentAPI)
app.register_blueprint(mypageAPI)

with open("secret_key.json")as Json:
	app.secret_key = json.loads(Json.read())["secret"]

#세션만료
@app.before_request
def make_session_permanent():
	session.permanent = True
	app.permanent_session_lifetime = timedelta(minutes= 60) #시간 설정

if __name__ == "__main__":
	app.run(host = '0.0.0.0', port = 5000, debug = True)
