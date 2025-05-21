import json
import boto3
from decimal import Decimal

rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FaceAnalysisResults')

def convert_floats(obj):
    if isinstance(obj, float):
        return Decimal(str(obj))
    elif isinstance(obj, list):
        return [convert_floats(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_floats(v) for k, v in obj.items()}
    else:
        return obj

def lambda_handler(event, context):
    # Extract bucket name and object key from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Analyze the image with Rekognition
    response = rekognition.detect_faces(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        Attributes=['ALL']
    )

    # Convert float values to Decimal for DynamoDB
    face_details = convert_floats(response['FaceDetails'])

    # Store face details in DynamoDB
    table.put_item(
        Item={
            'ImageName': key,
            'FaceAnalysisResults': face_details
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Face analysis complete and saved.')
    }