import boto3
import datetime

def lambda_handler(event, context):
    # Create an AWS IoT client
    iot_client = boto3.client('iot-data')
    
    # Get the current date and time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Publish the current date and time to the IoT topic
    iot_client.publish(
        topic='docker-iot-thing-topic',
        qos=1,
        payload=current_time
    )
    
    return {
        'statusCode': 200,
        'body': 'Published current date and time to IoT topic'
    }