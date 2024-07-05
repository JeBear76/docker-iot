# Docker IoT Thing

(EC2 IoT Tutorial Used)[https://docs.aws.amazon.com/iot/latest/developerguide/creating-a-virtual-thing.html]
(Django-Angular Tutorial used)[https://devarea.com/building-a-web-app-with-angular-django-and-django-rest/]
## Setup IoT Thing
### Basic Thing Setup

```
mkdir ~/certs

curl -o ~/certs/Amazon-root-CA-1.pem https://www.amazontrust.com/repository/AmazonRootCA1.pem 

aws iot create-keys-and-certificate \
    --set-as-active \
    --certificate-pem-outfile "~/certs/device.pem.crt" \
    --public-key-outfile "~/certs/public.pem.key" \
    --private-key-outfile "~/certs/private.pem.key"

aws iot attach-thing-principal \
    --thing-name "MyIotThing" \
    --principal "certificateArn"

aws iot create-policy \
    --policy-name "MyIotThingPolicy" \
    --policy-document "file://./config/policy.json"
```
## Django setup


## Angular Setup