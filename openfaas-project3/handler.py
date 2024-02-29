from boto3 import client
import boto3
import numpy as np
import os
import pickle
import face_recognition
import json
import csv

input_bucket = "inputbucketproject3"
output_bucket = "outputbucketproj2"

def get_student_data(name):
    print("in get student data")
    dynamo = boto3.client('dynamodb', region_name="us-east-1")
    data = dynamo.get_item(TableName='project2', Key={'name': {'S': name}})
    return data["Item"]
    
def put_student_data(video_name, name, major, year):
    print("in put student data")
    with open('/tmp/student.csv', 'w+') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow([name, major, year])
    csv_file.close()
    s3 = boto3.client('s3', region_name="us-east-1")
    with open('/tmp/student.csv', 'rb') as data:
        s3.upload_fileobj(data, output_bucket, video_name+'.csv')
    data.close()
    os.remove('/tmp/student.csv')

def open_encoding():
	file = open("function/encoding", "rb")
	data = pickle.load(file)
	file.close()
	return data

def recog(image_path, input_video):
    face_encodings = np.array(list(open_encoding().values()), dtype=object)
    inputImage = face_recognition.load_image_file(image_path)

    try:
        inputFaceEncoding = face_recognition.face_encodings(inputImage)[0]
    except IndexError:
        print("No face was detected fro the given database")
        quit()
        
    known_faces = np.array(list(open_encoding().values())[1])

    results = face_recognition.compare_faces(known_faces, inputFaceEncoding)
    
    index = np.where(results)[0][0]
    name = list(open_encoding().values())[0][index]
    student = get_student_data(name)
    studentName = student["name"]["S"]
    studentMajor = student["major"]["S"]
    studentYear = student["year"]["S"]
    print("student name: ", studentName)
    print("student major: ", studentMajor)
    put_student_data(input_video, studentName, studentMajor, studentYear)

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    print("invoked print")
    print("req: ", req)
    parsed_request = json.loads(req)
    video_key = next(k for k in parsed_request.keys())
    s3 = boto3.client("s3")
    
    local_video_path = f'/tmp/{video_key}'

    # Download the video file from S3
    s3.download_file(input_bucket, video_key, local_video_path)
    
    path = "/tmp/"
    os.system("ffmpeg -i " + str("/tmp/") + video_key + " -r 1 " + str(path) + "image-%3d.jpeg")
    recog("/tmp/image-001.jpeg", video_key.split(".")[0])

    return {"operation done"}
