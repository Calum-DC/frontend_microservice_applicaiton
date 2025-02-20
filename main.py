import os
from datetime import datetime
import boto3
from flask import Flask, render_template, request, jsonify, json, make_response
from dotenv import load_dotenv

app = Flask(__name__)


# sqs_client = boto3.client('sqs', region_name=os.getenv('AWS_REGION'))

# test fail
sqs_client = boto3.client('sqs', region_name="us-east-1", aws_access_key_id="AKIA....", aws_secret_access_key="secretkey....")


# Dictionary for SQS queue urls and associated priorities
queue_urls = {
    "1": os.getenv('SQS_QUEUE_P1'),
    "2": os.getenv('SQS_QUEUE_P2'),
    "3": os.getenv('SQS_QUEUE_P3')
}

@app.route("/")
def index():
    return render_template("index.html")

def priority_tag(priority):
    if priority == "1":
        return "Low"
    elif priority == "2":
        return "Medium"
    elif priority == "3":
        return "High"


@app.route("/submit_bug_report", methods=["POST"])
def submit_bug_report():

    # Extract the data from the bug report web form
    title = request.form["title"]
    description = request.form["description"]
    priority = request.form["priority"]
    timestamp = datetime.now().strftime("%d-%m-%y at %H:%M:%S")
    receipt_priority = priority_tag(priority)
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

    return render_template('receipt.html', title=title, description=description, priority=receipt_priority, timestamp=timestamp)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0')