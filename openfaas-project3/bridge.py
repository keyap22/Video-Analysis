from flask import Flask, request, jsonify
import boto3
import requests
import json
import time

app = Flask(__name__)

# AWS S3 Configuration
s3_client = boto3.client('s3', aws_access_key_id='AKIAW3R2SDTY6VQKVEPE', aws_secret_access_key='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')
bucket_name = 'inputrequestbucket'

# OpenFaaS Function Configuration
openfaas_url = 'http://127.0.0.1:8080/function/openfaas-project3'

# A dictionary to keep track of processed files
processed_files = {}

@app.route('/sns', methods=['POST'])
def sns_listener():
    sns_message = json.loads(request.data)
    
    # Confirm SNS subscription
    if sns_message['Type'] == 'SubscriptionConfirmation':
        subscribe_url = sns_message['SubscribeURL']
        requests.get(subscribe_url)  # Confirm the subscription
        return jsonify(success=True)

    # Handle regular SNS notifications here (if necessary)
    # ...

    return jsonify(success=True)

def check_new_files():
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        for obj in response['Contents']:
            file_name = obj['Key']
            if file_name not in processed_files:
                # Prepare JSON payload
                payload = {
                    'event': {
                        'Records': [{'s3': {'bucket': {'name': bucket_name}, 'object': {'key': file_name}}}]
                    }
                }
                # Trigger OpenFaaS Function
                requests.post(openfaas_url, json=payload)
                processed_files[file_name] = True

@app.route('/check-s3')
def check_s3():
    check_new_files()
    return "Checked S3 for new files."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

    # Set up a simple scheduler to check the bucket periodically
    while True:
        check_new_files()
        time.sleep(60)  # Check every 60 seconds
