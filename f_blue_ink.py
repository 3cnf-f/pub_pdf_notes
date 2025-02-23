import fitz

import logging

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(filename='example.log', encoding='utf-8',format=FORMAT)
logger.setLevel(logging.DEBUG)
 
def checkbluey(in_annot):
    if in_annot.colors["stroke"]:
            if in_annot.colors["stroke"]==[0.0,0.0,1.0]:
                return True
            else:
                return False
    else:
        return False
     