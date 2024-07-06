# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import asyncio
import websockets
from awscrt import mqtt, http
from awsiot import mqtt_connection_builder
import sys
import threading
import time
import json


connected = list()
# received_all_event = threading.Event()

# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))


# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(on_resubscribe_complete)


def on_resubscribe_complete(resubscribe_future):
    resubscribe_results = resubscribe_future.result()
    print("Resubscribe results: {}".format(resubscribe_results))

    for topic, qos in resubscribe_results['topics']:
        if qos is None:
            sys.exit("Server rejected resubscribe to topic: {}".format(topic))


# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    reply = "Received message from topic '{}': {}".format(topic, payload)
    print(reply)    
    print(f'Connected: {len(connected)}')
    for conn in connected:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            asyncio.run(conn.send(reply))
        else:
            loop.run_until_complete(conn.send(reply))
        
    #received_all_event.set()

# Callback when the connection successfully connects
def on_connection_success(connection, callback_data):
    assert isinstance(callback_data, mqtt.OnConnectionSuccessData)
    print("Connection Successful with return code: {} session present: {}".format(callback_data.return_code, callback_data.session_present))

# Callback when a connection attempt fails
def on_connection_failure(connection, callback_data):
    assert isinstance(callback_data, mqtt.OnConnectionFailureData)
    print("Connection failed with error code: {}".format(callback_data.error))

# Callback when a connection has been disconnected or shutdown successfully
def on_connection_closed(connection, callback_data):
    print("Connection closed")

def send_message(mqtt_connection, message_topic, message_string):
    message = "{}".format(message_string)
    print("Publishing message to topic '{}': {}".format(message_topic, message))
    mqtt_connection.publish(
        topic=message_topic,
        payload=message,
        qos=mqtt.QoS.AT_LEAST_ONCE)

# create handler for each connection
async def handler(websocket, path):
    if websocket not in connected:
        connected.append(websocket)
    while True:
        try:
            data = await websocket.recv()
        except websockets.ConnectionClosedOK:
            print ("Connection closed")
        reply = f"Data recieved as:  {data}!"
        print(reply)
        for conn in connected:
            await conn.send(reply)

async def webSocketMain():
    async with websockets.serve(handler, "0.0.0.0", 8000):
        await asyncio.Future()

if __name__ == '__main__':
    # Create a MQTT connection from the command line data
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint='axpxhkmf6px2p-ats.iot.eu-west-1.amazonaws.com',
        port=None,
        cert_filepath='./certs/docker-iot-thing.pem.crt',
        pri_key_filepath='./certs/docker-iot-thing-private.pem.key',
        ca_filepath='./certs/Amazon-root-CA-1.pem',
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id='docket-iot-thing-1',
        clean_session=False,
        keep_alive_secs=30,
        http_proxy_options=None,
        on_connection_success=on_connection_success,
        on_connection_failure=on_connection_failure,
        on_connection_closed=on_connection_closed)


    print(f"Connecting to 'axpxhkmf6px2p-ats.iot.eu-west-1.amazonaws.com' with client ID 'docket-iot-thing-1'...")
    
    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    message_count = 10
    message_topic = 'docker-iot-thing-topic'

    # Subscribe
    print("Subscribing to topic '{}'...".format(message_topic))
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=message_topic,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)

    subscribe_result = subscribe_future.result()
    print("Subscribed with {}".format(str(subscribe_result['qos'])))

    asyncio.run(webSocketMain())

    # # Disconnect
    # print("Disconnecting...")
    # disconnect_future = mqtt_connection.disconnect()
    # disconnect_future.result()
    # print("Disconnected!")