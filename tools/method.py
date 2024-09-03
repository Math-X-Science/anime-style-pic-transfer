from PIL import Image
import io
import os
import json
import base64
import random
import requests


def encode_pil_to_base64(image):
    with io.BytesIO() as output_bytes:
        image.save(output_bytes,format="png")
        byte_data = output_bytes.getvalue()
    return base64.b64encode(byte_data).decode("utf-8")

def sumbmit_post(url:str,data:dict):
    return requests.post(url,data=json.dumps(data))

def save_encoded_image(b64_image:str,output_path:str):
    with open(output_path,"wb") as image_file:
        image_file.write(base64.b64decode(b64_image))
    image_file.close()

def joinLoraList(loraName01,weight01,loraName02,weight02,loraName03,weight03):
    if loraName01 =="":
        loraPart01 =""
    else:
        loraPart01 = "<lora:%s:%2.1f"%(loraName01,weight01)

    if loraName02 =="":
        loraPart02 =""
    else:
        loraPart02 = "<lora:%s:%2.1f"%(loraName02,weight02)

    if loraName03 =="":
        loraPart03 =""
    else:
        loraPart03 = "<lora:%s:%2.1f"%(loraName03,weight03)
    
    loaralist = loraPart01 + loraPart02 + loraPart03
    print(loaralist)
    return loaralist
    
#if __name__ ==  "__main__":
