#!/bin/bash

echo "Configuring AWS account..."
echo "Please enter your AWS account number: "
read ACCOUNT_NUMBER
sed -i 's/<YOUR_ACCOUNT>/$ACCOUNT_NUMBER/g' ./publish-lambda.sh
sed -i 's/<YOUR_ACCOUNT>/$ACCOUNT_NUMBER/g' ./deployment-policies/lambda-deployment-policy.json
echo "AWS account number updated in scripts."
echo "Good to Go!"