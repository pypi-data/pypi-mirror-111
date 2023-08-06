#!/usr/bin/env python3.8

import json
import os
import sys

from .pyfinidash import InfinidashClient

run_command = os.system

def init():
    data_to_write = {
        "encryption": "AES_256"
    }
    
    cwd = os.getcwd()
    write_path = os.path.realpath(os.path.join(cwd, "aws-infinidash.json"))

    with open(write_path, "w") as config:
        config.write(json.dumps(data_to_write, indent=4))

def demo(key):
    client = InfinidashClient()

    client.encrypt(key).publish()

    print(client.encrypted_key)

    application = client.application("Hello")

    print(application.get_app_arn())
    print("")

    application.scale_to(10)

    rescaled_instances = application.get_rescaled_instances()

    for instance in rescaled_instances:
        print(instance.get_app_arn())

def main():
    mode = sys.argv[1]

    if mode == "init":
        init()
    elif mode == "demo":
        demo(sys.argv[2])

if __name__ == "__main__":
    main()
