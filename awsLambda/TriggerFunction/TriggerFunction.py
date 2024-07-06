import boto3

def lambda_handler(event, context):
    # Create an SNS client
    sns_client = boto3.client('sns')
    
    # Define the payload
    payload = [
        {
            'filename': 'file1.txt',
            'count': 10
        },
        {
            'filename': 'file2.txt',
            'count': 5
        },
        {
            'filename': 'file3.txt',
            'count': 3
        }
    ]

    # Publish the payload to the IoT Core topic
    iot_client = boto3.client('iot-data')
    iot_client.publish(
        topic='docker-iot-thing-topic',
        payload=str(payload)
    )