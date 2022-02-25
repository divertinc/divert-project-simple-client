#!/usr/bin/env python
# Copyright (c) 2022 Divert, Inc.
import json
import logging
import os

import requests
import pathlib

logging.basicConfig(level=logging.INFO,
                    filename="client.log",
                    format="%(levelname).1s [%(module)s.%(funcName)s]  %(message)s")


def main():
    client = DvSClient()
    client.invoke()


class DvSClient:
    
    DEFAULT_CONFIG = {
        "config_version": None,
        "client_id": "UNCONFIGURED",
        "server_address": "http://127.0.0.1:8000",
        "message": "animal-color",
    }
    
    def __init__(self):
        self.config = self.DEFAULT_CONFIG
        config_file = pathlib.Path(os.getenv("CONFIG_FILE") or "./config.json")
        if config_file.exists():
            config_input = json.loads(config_file.read_text())
            self.config.update(config_input)
        else:
            logging.warning(f"No config file found at {config_file.absolute().as_posix()}")
        
    def invoke(self):
        request_url = self.config["server_address"]
        request_content = {
            "client_id": self.config["client_id"],
            "message": self.config["message"],
        }
        
        logging.info(f"Calling {request_url} with content {request_content}")
        r = requests.post(url=request_url, json=request_content)
        logging.info(f"{r.status_code} {r.json()}")
    

if __name__ == '__main__':
    main()
