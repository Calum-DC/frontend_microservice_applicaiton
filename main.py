import os

import boto3
from flask import Flask, render_template, request, jsonify, json
from dotenv import load_dotenv

app = Flask(__name__)


load_dotenv()
sqs_client = boto3.client('sqs', region_name=os.getenv('AWS_REGION'))

# Dictionary for SQS queue urls and associated priorities
queue_urls = {
    "1": os.getenv('SQS_QUEUE_P1'),
    "2": os.getenv('SQS_QUEUE_P2'),
    "3": os.getenv('SQS_QUEUE_P3'),
}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit_bug_report", methods=["POST"])
def submit_bug_report():

    # Extract the data from the bug report web form
    title = request.form["title"]
    description = request.form["description"]
    priority = request.form["priority"]

    # Check SQS queue and assign correct one
    queue_url = queue_urls.get(priority)
    if not queue_url:
        return jsonify({"error": "Invalid priority"}), 400

    # Create the message (dictionary then convert to json)
    message_body = {
        "title": title,
        "description": description
    }
    json_message_body = json.dumps(message_body)

    # Send message to the SQS queue
    sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=json_message_body)


if __name__ == "__main__":
    app.run(debug=True)