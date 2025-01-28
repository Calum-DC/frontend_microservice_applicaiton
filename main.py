import os
from flask  import Flask, render_template, redirect_url, jsonify


app = Flask(__name__)

#
# https://sqs.eu-north-1.amazonaws.com/535002885105/SQS_Queue_P1
# https://sqs.eu-north-1.amazonaws.com/535002885105/SQS_Queue_P2
# https://sqs.eu-north-1.amazonaws.com/535002885105/SQS_Queue_P3





@app.route("/")
def index():
    return render_template("index.html")




if __name__ == "__main__":
    app.run(debug=True)