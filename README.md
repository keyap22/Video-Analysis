## How to Run the App

### Step 1: Download Zip File
Download the project as a zip file.

### Step 2: Upload Student Data to DynamoDB
Navigate to the location where your student.json file is and use the following command to upload it to DynamoDB:

```bash
aws dynamodb batch-write-item --request-items file://student_data.json
```

make sure to add your dynamodb table name in the json file

### Step 3 : Create input and output s3 buckets

### Step 4 : Update details in handler.py and your_function_name.yml file

```Set your aws keys and secret key in the yml file and set the input and output bucket name in the handler file. 
Also, update the image-name in yml file with your_docker_account_name/your_function_name:latest
Update dynamodb table name in get_student_data() in handler file 
```

### Step 5 : Upload docker file to your docker hub and then deploy openfaas function

faas-cli build -f your_function_name.yml                                   
faas-cli push -f your_function_name.yml                       
faas-cli deploy -f your_function_name.yml --gateway http://127.0.0.1:31112

### Step 6 : Run workload generator 

```bash
python3 workload.py
```
