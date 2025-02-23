import json
import f_pdf_tools as f_p
import re
import f_js_md_data_n_tools as d
import logging






#### OBS ÄNDRAT JSON FORMAT!!


logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(filename='example.log', encoding='utf-8',format=FORMAT)
logger.setLevel(logging.DEBUG)

def add_foldall():
    out_string=""
    out_string+=d.cr()+"{[Outline: Fold All]}    {[Outline: Unfold All]}"
    return out_string

def add_journal(in_data):
    out_string=""
    logger.debug("")
    out_string+=d.heading_3(in_data,"journal")+d.cr(2) 
    return out_string

def add_main_authors_date(in_data):
    out_string=""
    logger.debug("")

    out_string+=d.heading_3(in_data,"main_author")+"   -   "                                                                       
    out_string+=d.just_text(in_data,"date")                                                                      
    return out_string

def add_title(in_data):
    out_string=""
    logger.debug("title")
    out_string+=d.heading_3(in_data,"title")                                                                       
    return out_string


def parse_header(in_data):
    logger.debug("enter parse")
    out_string=""
    #out_string+=d.just_text("### header_data")
    out_string+=d.start_code_block                   
    out_string+=d.line_dump(in_data,"title")                                                                       
    out_string+=d.line_dump(in_data,"journal")                                                                                          
    out_string+=d.line_dump(in_data,"main_authors")                                       
    out_string+=d.line_dump(in_data,"abstract")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    out_string+=d.line_dump(in_data,"pubmed_url")                                             
    out_string+=d.line_dump(in_data,"date")                                             
    out_string+=d.line_dump(in_data,"volume")      
    out_string+=d.line_dump(in_data,"issue")     
    out_string+=d.line_dump(in_data,"DOI")
    out_string+=d.line_dump(in_data,"pmid")            
    out_string+=d.line_dump(in_data,"file_uuid4")
    out_string+=d.line_dump(in_data,"file_datetime_stockholm")
    out_string+=d.line_dump(in_data,"filename")                                                          
    out_string+=d.line_dump(in_data,"issn")             


    out_string+=d.cr()+d.end_code_block+d.cr(2)
    #out_string+=d.end_details()
    print(out_string)
    return out_string
    

def load_json_for_conversion(in_filename):
    with open(in_filename,"r",encoding='utf-8') as infile:
        indata=json.load(infile)
    return indata

def block_annot(block_list):
    logger.debug(block_list)
    out_blocks=""   
    aa=block_list             
    if aa["entry_type"]==("blue_ink"): 
 
        out_blocks+=("### Handwriting p:"+str(aa["page_no"]))
        print(d.cr(2)+aa["annotation_text"])

        try:
            is_a_thing=aa["img_filename"] 
            if is_a_thing!="":
                d.h4_plain("img > >")
                out_blocks+=d.dump_image_same_folder(is_a_thing)
        except:
            print(aa["annot_uuid4"]+": no img filename")
            logger.debug("no image in annot: "+aa["annot_uuid4"])
        try:
            is_a_thing=aa["highlighted_text"] 
            if is_a_thing!="":
                d.h4_plain("hlt > >")
                out_blocks+=(""+is_a_thing+"\n")
        except:
            print(aa["annot_uuid4"]+": no img highlighted text")
            logger.debug("no highlight in annot: "+aa["annot_uuid4"])
        try:
            is_a_thing=aa["annotation_text"] 
            if is_a_thing!="":
                d.h4_plain("ant > >")
                out_blocks+=("\n"+is_a_thing+"\n")
                #out_blocks+=("* "+is_a_thing+"\n\n")
        except:
            print(aa["annot_uuid4"]+": no img annotated text")
            logger.debug("no annotation in annot: "+aa["annot_uuid4"])
        #out_blocks+=d.end_details()+d.cr(1)
    if aa["entry_type"]==("non_blue_ink") or aa["entry_type"]==("rectangle"):
        out_blocks+= ("### Pen annotation p:"+str(aa["page_no"]))

        try:
            is_a_thing=aa["img_filename"] 
            if is_a_thing!="":
                d.h4_plain("img > >")
                out_blocks+=d.dump_image_same_folder(is_a_thing)
                #out_blocks+=d.dump_image(is_a_thing)
        except:
            print(aa["annot_uuid4"]+": no img filename")
            logger.debug("no image in annot: "+aa["annot_uuid4"])
        try:
            is_a_thing=aa["highlighted_text"] 
            if is_a_thing!="":
                d.h4_plain("hlt > >")
                out_blocks+=("\n"+is_a_thing+"\n")
                #out_blocks+=("* "+is_a_thing+"\n\n")
        except:
            print(aa["annot_uuid4"]+": no img highlighted text")
            logger.debug("no highlight in annot: "+aa["annot_uuid4"])
        try:
            is_a_thing=aa["annotation_text"] 
            if is_a_thing!="":
                d.h4_plain("ant > >")
                out_blocks+=("\n"+is_a_thing+"\n") 
                #out_blocks+=("* "+is_a_thing+"\n\n")
        except:
            print(aa["annot_uuid4"]+": no img annotated text")
            logger.debug("no annotation in annot: "+aa["annot_uuid4"])
        #out_blocks+=d.end_details()+d.cr(1)
    if aa["entry_type"]==("highlight"):
        out_blocks+=("### highlight p:"+str(aa["page_no"]))

        try:
            is_a_thing=aa["img_filename"] 
            if is_a_thing!="":
                d.h4_plain("img > >")
                out_blocks+=d.dump_image_same_folder(is_a_thing)
        except:
            print(aa["annot_uuid4"]+": no img filename")
            logger.debug("no image in annot: "+aa["annot_uuid4"])
        try:
            is_a_thing=aa["highlighted_text"] 
            if is_a_thing!="":
                d.h4_plain("hlt > >")
                out_blocks+=("\n "+is_a_thing+"\n")
                #out_blocks+=("* "+is_a_thing+"\n\n")
        except:
            print(aa["annot_uuid4"]+": no img highlighted text")
            logger.debug("no highlight in annot: "+aa["annot_uuid4"])
        try:
            is_a_thing=aa["annotation_text"] 
            if is_a_thing!="":
                d.h4_plain("ant > >")
                out_blocks+=("\n* "+is_a_thing+"\n")
                #out_blocks+=("* "+is_a_thing+"\n\n")
        except:
            print(aa["annot_uuid4"]+": no img annotated text")
            logger.debug("no annotation in annot: "+aa["annot_uuid4"])
        #out_blocks+=d.end_details()+d.cr(1)
     
    return out_blocks



def dump_all_data(infile_json_data):
    for i,this_block in enumerate(infile_json_data):
        print("\n\n\n-----------------\n"+str(i)+"\n-----------------\n"+str(this_block))

def convert_json_to_MD(in_filname,out_filname,att_base_url=""):
    '''
    set att_base_url to "local=folder" if it is to be set as in the same silverbullet.md base 
    folder as in ![[folder/img_filename.png]] or leave the default att_base_folder="" for files in same folder
    or.. supply a url as in http://h.23.we.cc/static/


    '''
    outfile_list=[]
    outfile_dict={}
    ## outfile is a list of the md blocks that will be written 
    if att_base_url!="":
        att_base_url.append("/")
    infile_json_data=load_json_for_conversion(att_base_url+in_filname)

    with open(out_filname,"w",encoding="utf-8") as outfile:
        outfile.write(add_title(infile_json_data))
        outfile.write(add_main_authors_date(infile_json_data))
        outfile.write(add_journal(infile_json_data))
        outfile.write(add_foldall())
        

        outfile.write(parse_header(infile_json_data))
        for this_part in infile_json_data["blocks"]:
            outfile.write(block_annot(this_part))    

 
 #not finished

testrun=False

if testrun:
    tst_outfile="/config/workspace/pdf_notes/out_test.md"
    tst_infile="devast_metabol_newborb/devast_metabol_newborb.json"
    convert_json_to_MD(tst_infile,tst_outfile)

    
