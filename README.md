#AWS Face Analysis Pipeline

This project uses AWS services to automatically detect faces in images uploaded to S3 and saves the results to DynamoDB.

# Background
I wanted to familiarize myself with AWS services and wanted to learn how AWS services could work together to solve a real-world problem. Face detection is used in things like ID verification and security - so I thought it'd be a good challenge to build a small version of that on AWS.

# Understanding 

The idea is that an image is uploaded to S3 which triggers Lambda to use Rekognition to analyze it and then the results are saved in dynamoDB.

# Implementation
How I built it:
- S3 Bucket: Stores the uploaded images
- Lambda Function: Runs when a new image is added
- Rekognition: Does the face detection
- DynamoDB: Stores all the results (Face attributes)
- IAM Role: Gives Lambda permission to use Rekognition, S3, and DynamoDB

Tech Stack:
- AWS Lambda
- Amazon Rekognition
- Amazon S3
- Amazon DynamoDB
- Python & Boto3

# Lessons Learned

This project taught me a lot about how AWS services really work together, especially when it comes to permissions and how different services communicate. I ran into several issues that I had to troubleshoot, and each one helped me understand the bigger picture.

When I first set this up, I thought that giving my lambda function permission to access S3 was all I needed. Since Lambda had the correct IAM role with S3 and Rekognition permissions, I assumed everything would run smoothly. What I did not realize was that Amazon Rekognition is a completly separate AWS service. Even though my lambda function was triggering it, Rekognition was still trying to access the image in S3 by itself. This meant Rekognition also needed permission to read the image, which Lambda's IAM role could not provide on its own. The fix was to update my S3 bucket policy and specifically allow the Rekognition service to read files in the bucket. Once I added a policy that gave rekognition permissions to access the bucket, the function finally worked.

Another issue i ran into was with floats in DynamoDB. DynamoDB refused to let me store the results of the face analysis. I kept getting an error that said float types were not supported. This happened because Rekognition returns things like bounding box dimensions and confidence scores as regular floats, and DynamoDb requires them to be in the decimal format instead. I had to write a helper function that went through the entire response and converted all float values into Decimal objects using Python's decimal module. After I did that, I was able to store the results in DynamoDB table without any problems.

# Deliverables

At the end of the Project, I had a working pipeline that:
 - Reacts to new image uploads
 - Detects faces automatically
 - Stores all results in a DynamoDB table
 
This was my first time connecting multiple AWS services into a complete working system, and it really helped me understand how cloud services can respond to events and trigger other actions automatically. Building something that reacts to real-time changes, like an image upload, showed me how powerful event-driven architecture can be and gave me a much clearer idea of how modern serverless applications are designed.