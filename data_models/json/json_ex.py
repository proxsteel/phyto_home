#!/usr/bin/env python3
import json

with open("dev_facts.json") as F:
    data = F.read()
    j_dict = json.loads(data)
    print ("The type of data is: ", type(j_dict))
#    print (j_dict)

    for k, v in j_dict.items():
        print("Key {ky}: Value {val} --- Type {t}".format(ky=k, val=v, t=type(v)))
