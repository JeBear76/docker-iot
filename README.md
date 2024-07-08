# Docker IoT Thing

[EC2 IoT Tutorial Used](https://docs.aws.amazon.com/iot/latest/developerguide/creating-a-virtual-thing.html)
[Docker Networking](https://www.tutorialworks.com/container-networking/)

## Setup IoT Thing
### Basic Thing Setup

```
mkdir ./iot-app/certs

curl -o ./iot-app/certs/Amazon-root-CA-1.pem https://www.amazontrust.com/repository/AmazonRootCA1.pem 

aws iot create-keys-and-certificate \
    --set-as-active \
    --certificate-pem-outfile "./iot-app/certs/device.pem.crt" \
    --public-key-outfile "./iot-app/certs/public.pem.key" \
    --private-key-outfile "./iot-app/certs/private.pem.key"

aws iot attach-thing-principal \
    --thing-name "MyIotThing" \
    --principal "certificateArn"

aws iot create-policy \
    --policy-name "MyIotThingPolicy" \
    --policy-document "file://./docker-iot-device-config/policy.json"
```

## Docker setup
```
docker network create tulip-net
```

## Angular Setup