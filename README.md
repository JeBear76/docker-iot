# Docker IoT Thing

[EC2 IoT Tutorial Used](https://docs.aws.amazon.com/iot/latest/developerguide/creating-a-virtual-thing.html)
[Docker Networking](https://www.tutorialworks.com/container-networking/)

## Setup IoT Thing
### Basic Thing Setup

```
mkdir ~/certs
```

## Docker setup
```
docker network create tulip-net
```

## Angular Setup

```
openssl req -x509 -newkey rsa:4096 -keyout ~/cerst/static-key.pem -out ~/certs/static-cert.pem -sha256 -days 3650 -nodes -subj "/C=ZA/ST=Western Cape/L=Cape Town/O=RobotMaker/OU=R&D/CN=Jebear76"
```