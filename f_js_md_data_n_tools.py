import json
conv_tab_file_header=[
    {"to_list":"uuid4","from_list":"uuid4"},
    {"to_list":"DOI","from_list":"DOI"},
    {"to_list":"orig_full_pdf_path","from_list":"filename"},
    {"to_list":"datetime_stockholm","from_list":"datetime_stockholm"}
    ]

start_code_block="\n```pdf_data\n" 
end_code_block="\n```\n" 
def cr(nos=1):
    stringout=""
    for i in range(nos):
        stringout+=("\n") 
    return stringout

def line_dump(indic,key):
    outstr=""
    outstr+=cr()+str(key)+": "+indic[key]
    return outstr

def just_text(indic,key):
    outstr=""
    outstr+=indic[key]
    return outstr

def heading_3(indic,key):
    outstr=""
    outstr+=cr()+"### "+indic[key]
    return outstr

def heading_2(indic,key):
    outstr=""
    outstr+=cr()+"## "+indic[key]
    return outstr

def h3_plain(in_string):
    outstr=""
    outstr+="\n### "+in_string
    return outstr




def details_summary(in_summary):
    outstr=""
    outstr+=cr()+"<details><summary>"+in_summary+"</summary>"+cr()
    return outstr


    
def end_details():
    outstr=""
    outstr+=cr()+"</details>\n"
    return outstr

def dump_image_same_folder(in_path,width="",height=""):
    is_x=""
    is_pipe=""
    if width!="" or height!="":
        is_pipe="|"
    if height!="":
        is_x="x"
    outstr=""
    outstr+=cr()+"![img]("+in_path+is_pipe+width+is_x+height+")"+cr(1)
    return outstr

def load_json_for_conversion(in_filename):
    with open(in_filename,"r",encoding='utf-8') as infile:
        indata=json.load(infile)
    return indata
