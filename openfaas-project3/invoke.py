import requests
import boto3
import json

def invoke():
    s3 = boto3.client("s3")
    input_bucket = "inputbucketproject3"
    openfaas_gateway_url = 'http://127.0.0.1:31112/'
    openfaas_function_name = 'openfaas-project3.openfaas-fn'

    response = s3.list_objects_v2(Bucket=input_bucket)
    key = response['Contents'][0]['Key']
    
    if 'Contents' in response:
        print("dhudjn")
        for obj in response['Contents']:
            video_key = obj['Key']
            print("processing file name: ", video_key)
            data = '{{"{}":"{}"}}'.format(video_key, video_key)

            response = requests.post(
            'http://127.0.0.1:31112/function/openfaas-project3.openfaas-fn',
            headers={'Content-Type': 'text/plain'},
            data=data,)

    print("response: ", response.text)

invoke()