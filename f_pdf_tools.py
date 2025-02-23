import re
import pymupdf,fitz
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import logging


logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(filename='example.log', encoding='utf-8',format=FORMAT)
logger.setLevel(logging.DEBUG)
 



def get_dict(pdf_file,page_no=0):
    page = pdf_file.load_page(page_no)
    page_content = page.get_text('dict',sort=True)
   
    return page_content
def find_doi(pagein:pymupdf.Page):
    doi_doi=None
    intex=pagein.get_text().split()
    logger.debug(pagein.number)
 


   
    for l_no,this_line in enumerate(intex):

#        print(l_no, this_line)


         this_line_lower=str(this_line).lower()
         #print(this_line_lower,str(this_line))
         if "doi:" in this_line_lower:
            doi_doi=this_line.replace("doi:","")
            #print("doi on line: "+str(l_no)+" doi line: "+this_line_lower)
         elif "https://doi.org/" in this_line:
            doi_doi=this_line.replace("https://doi.org/","")
            """ 
            print("doi on line: "+str(l_no)+" doi line: "+this_line_lower,doi_doi)
            else:
                         print("\nno doi on page/line: "+str(pagein.number)+this_line_lower+"\n------\n") """
             

        # .replace-("doi:","").strip()
    if doi_doi==None:
        doi_doi=re_pagefind_doi(pagein)
        
    return doi_doi

def datetime_stockholm():

    # Get the current time in UTC
    now = datetime.now(ZoneInfo("UTC"))

    # Convert to CET (Central European Time)
    cet_time = now.astimezone(ZoneInfo("Europe/Berlin"))

    # Format it as YYYY-MM-DD HH:MM:SS
    formatted_date_time = cet_time.strftime("%Y-%m-%d %H:%M:%S")

    return str(formatted_date_time)

def get_text(pdf_file,page_no=0):
    page = pdf_file.load_page(page_no)
    page_content = page.get_text('text',sort=True)
   
    return 

def readpdf(in_filename):
    out_pdf=pymupdf.open(in_filename)
    return out_pdf
    

def generic_items(dict_or_list):
    if type(dict_or_list) is dict:
        return dict_or_list.items()
    if type(dict_or_list) is list:
        return enumerate(dict_or_list)
def get_keys(dictionary):
    result = []
    # goodstuff=[]
     

    for key, value in generic_items(dictionary):
        if type(value) is dict or type(value) is list:
            new_keys = get_keys(value)
            result.append(key)
            for innerkey in new_keys:
                # result.append(f'../{innerkey}')
                # result.append(f'.')
                result.append(f'{key}/{innerkey}')
        elif value=='':
            result.append(f'_emptyvalue_{key}:{value}')
        else:
            result.append(f'_value_{key}:{value}')

    return result

def get_keys_with_values(keys_values_list,return_only_non_blank=True):
    aa_list=get_keys(keys_values_list)
    results=[]
    for aa in aa_list:
        if type(aa)==str:
            if "_value_" in aa.lower():

                res=aa.replace("_value_","")
                results.append(res)
            if "_emptyvalue_" in aa.lower() and return_only_non_blank==False:
                res=aa.replace("_emptyvalue_","")
                results.append(res)
    return results


def re_extract_doi(in_string):

    #re_keep_fo_pa=re.compile(r'(Published online|http[s]{,1}://dx\.doi\.org)\s+(?P<part1>10.\d{4,})(?P<part2>(/[\w\.]+)+)')
    jls_extract_var = r'(Published online|http[s]{,1}:\/{2}dx\.doi\.org|doi:)(\s|\/)(?P<part1>(10\.\d{4,})((\/[\w\.\-]+)+))'
    re_keep_fo_pa=re.compile(jls_extract_var)
    resulta=re_keep_fo_pa.search(in_string)
    if resulta:
        resultado=(resulta.group('part1'))
    else:
        resultado='Empty'
    return resultado


def re_pagefind_doi(page_in):
    page_no=page_in.number
    this_pdf_meta=page_in.get_textpage().extractBLOCKS()
    found_it=False

    for no,i in enumerate(this_pdf_meta):
        if i[-1]==0:
            this_text=i[-3]
            current=re_extract_doi(this_text)
            if current!="Empty":
                return current
    return None

def re_af_get_func(annotation):
    this_re=re.compile(r"(?P<f_name>#_title|#_author|#_date|#_dhl|#_thl)\((?P<args>[\w\s_-]*)\)")
    try:
        return this_re.findall(annotation)
    except:
        return False    

def annot_func_course(in_args,highlight):
    if in_args=="hl" or in_args=="":
        return highlight
        
    else:
        return in_args

def annot_func_date(in_args,highlight):
    if in_args=="hl" or in_args=="":
        return highlight
        
    else:
        return in_args
    
def annot_func_author(in_args,highlight):
    if in_args=="hl" or in_args=="":
        return highlight
        
    else:
        return in_args

def annot_func_title(in_args,highlight):
    if in_args=="hl" or in_args=="":
        return highlight
        
    else:
        return in_args


def meta_from_annot(page_in):
    page_no=page_in.number
    found_it=False
    this_author=None
    this_title=None
    this_date=None
    this_course=None

    for this_annot in page_in.annots():
        logger.debug("annot type "+str(this_annot.type[0]))
        if this_annot.type[0] == 8:  # Highlight

            highlight,annotation=get_annot_func_hl(this_annot,page_in)
            logger.debug("highlight results: "+str(annotation)+" "+ str(highlight))
            resulta=re_af_get_func(annotation)
            logger.debug("resulta length: "+str(len(resulta)))
            if len(resulta)>0:
                for ixikaxi in range(len(resulta)):
                    this_resultss=(resulta.pop())
                    logger.debug("# / results: "+str(ixikaxi)+str(this_resultss))
                    if this_resultss[0]=="#_title" or this_resultss[0]=="#_th":
                        logger.debug("calling #_title")
                        this_title=annot_func_title(this_resultss[1],highlight)
                        logger.debug("title is: "+this_title)
                    if this_resultss[0]=="#_author" or this_resultss[0]=="#_ah":
                        logger.debug("calling #_author")
                        this_author=annot_func_author(this_resultss[1],highlight)
                        logger.debug("author is: "+this_author)
                    if this_resultss[0]=="#_date" or this_resultss[0]=="#_dh":
                        logger.debug("calling #_date")
                        this_date=annot_func_date(this_resultss[1],highlight)
                        logger.debug("date is: "+this_date)
                    if this_resultss[0]=="#_course" or this_resultss[0]=="#_ch":
                        logger.debug("calling #_course")
                        this_date=annot_func_course(this_resultss[1],highlight)
                        logger.debug("course is: "+this_course)
    out_meta={}
    out_meta["main_author"]=this_author
    out_meta["date"]=this_date
    out_meta["title"]=this_title
    out_meta["course"]=this_course




                    
  
    return out_meta

def get_annot_func_hl(annot, page):
    rect = annot.rect
    if int(rect.y0-20)>0:
        left=int(rect.y0-20)
    else:
        left=0
    if int(rect.y1+20)<page.rect.y1:
        right=int(rect.y1+20)
    expand_rect=fitz.Rect(0,left,page.rect.x1,right)

    words = page.get_text("words")
    highlighted_words = [w for w in words if fitz.Rect(w[:4]).intersects(rect)]
    annot_text = " ".join(w[4] for w in highlighted_words)
    note_text = annot.info["content"] if "content" in annot.info else "No note"
    note_text= note_text.replace("\n", " ") #ta bort cr cl
    note_text= note_text.replace("\r", " ") #ta bort cr cl
    return annot_text, note_text


test=False

if test==True:
   resultsss=re_af_get_func("#_title(hl) #_author(kalarakis) #_date()") 
   print(len(resultsss))
   print(resultsss.pop())
   print(resultsss.pop())