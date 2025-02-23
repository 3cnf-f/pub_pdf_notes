import logging
import pdf2_pdf_t_json as f_pj
import f_json_md as f_jm 
import f_json_ipynb as f_ji
from sys import argv  
import os
from os import makedirs as o_makedirs
from os import path as o_p
from shutil import copy as s_copy
from shutil import make_archive as s_ma

import json



 
logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(filename='example.log', encoding='utf-8', format=FORMAT)
logger.setLevel(logging.DEBUG)
 




def pdf_json_ipynb(pdf_file_path):


    
    folder_name = f"{os.path.basename(pdf_file_path).split('.')[0]}"

    if not o_p.exists(folder_name):
        o_makedirs(folder_name)

    local_img_folder = folder_name  # Local directory path
    print(folder_name)
    # Process the PDF
    #(os.listdir('/p01'))
    ipynb_name = f"{os.path.basename(pdf_file_path).split('.')[0]}.ipynb"
    ipynb_name = local_img_folder+"/"+ipynb_name
    md_name = f"{os.path.basename(pdf_file_path).split('.')[0]}.md"
    md_name = local_img_folder+"/"+md_name

    data = f_pj.process_pdf_annotations(pdf_file_path, local_img_folder)

    json_filename= folder_name+"/"+folder_name+".json"
    print(data)
    print(json_filename)

    with open(json_filename,"w") as ff:
        json.dump(data,ff,indent=4)

    #f_jm.convert_json_to_MD(json_filename,md_name,)
    f_ji.l_j_mk_n_sv_ipynb(json_filename,ipynb_name)




    s_copy(pdf_file_path,folder_name+"/"+folder_name+".pdf")
    s_ma(folder_name,"zip",folder_name+"/")

    print(folder_name,pdf_file_path,md_name)

if __name__ == '__main__':
    arg_pdf_file_path = argv[1]   # runs on arg instead of hard set
    pdf_json_ipynb(arg_pdf_file_path)


test=False
if test:
    tst_pdf_file_path="/config/workspace/pdf_notes/r01.pdf"
    pdf_json_ipynb(tst_pdf_file_path)
