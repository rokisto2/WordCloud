import os
import shutil
import threading

import pymysql
import json

from matplotlib.pyplot import step


def generatedJson(id, name, power, Sattelites):
    my_list = {"image": f"ipfs://IPFSPUT/{id}.png", f"name": f"{name}", "attributes": [
        {
            "trait_type": "Sattelites",
            "value": f"{Sattelites}"
        },
        {
            "trait_type": "Power",
            "value": f"{power}"
        }
    ]}
    with open(f'/mnt/HC_Volume_22862748/Json2/{id}.json', 'w') as outfile:
        json.dump(my_list, outfile,indent=4)
