#!/bin/bash

curl -o ~/certs/Amazon-root-CA-1.pem https://www.amazontrust.com/repository/AmazonRootCA1.pem 

CERTIFICATE_ARN=$(aws iot create-keys-and-certificate \
    --profile iot-user \
    --no-cli-pager \
    --region eu-west-1 \
    --set-as-active \
    --certificate-pem-outfile "~/certs/docker-iot-thing.pem.crt" \
    --public-key-outfile "~/certs/docker-iot-thing-public.pem.key" \
    --private-key-outfile "~/certs/docker-iot-thing-private.pem.key" \
    --query certificateArn | tr -d '"')

aws iot create-thing \
    --profile iot-user \
    --no-cli-pager \
    --region eu-west-1 \
    --thing-name "docker-iot-thing"

aws iot attach-thing-principal \
    --profile iot-user \
    --no-cli-pager \
    --region eu-west-1 \
    --thing-name "docker-iot-thing" \
    --principal $CERTIFICATE_ARN

aws iot create-policy \
    --profile iot-user \
    --no-cli-pager \
    --region eu-west-1 \
    --policy-name "docker-iot-thing-policy" \
    --policy-document "file://./docker-iot-device-config/policy.json"

aws iot attach-policy \
    --profile iot-user \
    --no-cli-pager \
    --region eu-west-1 \
    --policy-name "docker-iot-thing-policy" \
    --target $CERTIFICATE_ARN