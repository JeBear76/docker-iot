cp -r ~/certs ./iot-app/certs
cp -r ~/certs ./angular-bld/certs
docker compose up -d --build
docker exec -it iot-ollama ollama pull llama3
rm -rf ./iot-app/certs
rm -rf ./angular-bld/certs