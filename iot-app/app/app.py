# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import asyncio

from awscrt import mqtt, http
from awsiot import mqtt_connection_builder
import sys
import threading
import time
import json

# received_all_event = threading.Event()

# Callback when connection is accidentally lost.




if __name__ == '__main__':
    

    asyncio.run(webSocketMain())

    # # Disconnect
    # print("Disconnecting...")
    # disconnect_future = mqtt_connection.disconnect()
    # disconnect_future.result()
    # print("Disconnected!")
