#!/bin/bash

CURRENT_DIR=$(pwd)

# Delete the policy if it exists
aws iam delete-role-policy \
    --profile iot-backend-deployment-user \
    --no-cli-pager \
    --role-name LambdaIotTriggerFunctionRole \
    --policy-name LambdaIotTriggerFunctionPolicy
    
# Delete the IAM role if it exists
aws iam delete-role \
    --profile iot-backend-deployment-user \
    --no-cli-pager \
    --role-name LambdaIotTriggerFunctionRole

# Create an IAM role if it doesn't exist
aws iam create-role \
    --profile iot-backend-deployment-user \
    --no-cli-pager \
    --role-name LambdaIotTriggerFunctionRole \
    --assume-role-policy-document file://awsLambda/policies/lambda-trust-policy.json


# Attach the policy to the role
aws iam put-role-policy \
    --profile iot-backend-deployment-user \
    --no-cli-pager \
    --role-name LambdaIotTriggerFunctionRole \
    --policy-name LambdaIotTriggerFunctionPolicy \
    --policy-document file://awsLambda/policies/lambdaRole.json

# Create an SNS topic called iotTrigger
aws sns create-topic \
    --profile iot-backend-deployment-user \
    --no-cli-pager \
    --name iotTrigger

# Create a package folder in the TriggerFunction folder
mkdir -p ./awsLambda/TriggerFunction/package

# Install boto3 using pip into the package folder
pip install boto3 -t ./awsLambda/TriggerFunction/package

cd ./awsLambda/TriggerFunction/
# Zip the contents of the TriggerFunction folder
zip -q -r ../function.zip .  && echo "Zip success" || echo "Zip failure"

cd $CURRENT_DIR

# Remove the existing function if it exists
aws lambda delete-function \
    --profile iot-backend-deployment-user \
    --no-cli-pager \
    --function-name IotTriggerFunction \
    --region eu-west-1

# Upload the function to AWS (replace <function_name> and <bucket_name> with your own values)
aws lambda create-function \
    --profile iot-backend-deployment-user \
    --no-cli-pager \
    --function-name IotTriggerFunction \
    --runtime python3.12 \
    --role arn:aws:iam::208600120751:role/LambdaIotTriggerFunctionRole \
    --handler TriggerFunction.lambda_handler \
    --zip-file fileb://awsLambda/function.zip \
    --region eu-west-1 \
    --timeout 30 \
    --memory-size 128 \
    --publish

# Remove the package folder
rm -rf ./awsLambda/TriggerFunction/package
rm -f ./awsLambda/function.zip
