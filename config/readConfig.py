from os import environ

from dotenv import load_dotenv



def getClientID():
    load_dotenv()
    return environ["Client_ID"]
def getClientSecret():
    load_dotenv()
    return environ["Client_Secret"]
def getTargetChannel():
    load_dotenv()
    return environ["Target_Channel"]
def getTargetFile():
    load_dotenv()
    return environ["Target_File"]
