
#from metapub import PubMedFetcher 
#import f_before_metapub

import f_doi_to_pmid_http as f_dp

import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(filename='example.log', encoding='utf-8',format=FORMAT)
logger.setLevel(logging.DEBUG)
 


def meta_from_pmid(pmid_in):
    logger.debug("in meta_from_pmid")

    article=None

    fetch = PubMedFetcher()

    try:
        article=fetch.article_by_pmid(pmid_in)
    except Exception as e:
        print("pubmedfetcher error: ", repr(e))

        # print(article.keywords)
        # print(article.title)
        # print(article.journal, article.year, article.volume, article.issue)
        # print(article.authors)
        # print(article.citation)    
    return article





def meta_from_href(doi_in="",from_file=""):
    logger.debug("in functionn")
    parsed_data={}
    in_txt=""
    # Send an HTTP GET request
    if doi_in!="" and from_file=="":
        response = requests.get("https://pubmed.ncbi.nlm.nih.gov/?term=doi:"+doi_in)
        in_txt=response.text
        response_code=response.status_code 
    elif doi_in=="" and from_file!="":
        with open(from_file,"r") as in_html_file:
            in_txt=in_html_file.read()
            response_code=200 
    else:
        parsed_data=None
        logger.debug("no url and no file given to this func")
        return


    
    # Check if the request was successful
    if response_code == 200 :
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(in_txt, 'html.parser')
        #logger.debug(in_txt)
        
        # Find the meta tag with name="citation_pmid"
        parsed_data["pmid"] = str(soup.find('meta', attrs={'name': 'citation_pmid'})["content"]) 
        parsed_data["title"] = str(soup.find('meta', attrs={"name":"citation_title"})["content"])
        main_authors = str(soup.find('meta', attrs={"name":"citation_authors"})["content"])
        parsed_data["main_authors"]=main_authors
        parsed_data["main_author"]=main_authors.split(";")[0]

         
        parsed_data["journal"] = str(soup.find('meta', attrs={"name":"citation_publisher"})["content"])
        parsed_data["journal_longname"] = str(soup.find('meta', attrs={"name":"citation_journal_title"})["content"])
        #parsed_data["abstract"] = str(soup.find('div',class_=["abstract-content"],id="eng-abstract").find('p').string).replace('\n','').replace("  ",'')
        parsed_data["abstract"] = str(soup.find('div',class_=["abstract-content"],id="eng-abstract").get_text()).replace("\n","").replace("   ","")
        logger.debug(parsed_data["abstract"])
        parsed_data["volume"] = str(soup.find('meta', attrs={"name":"citation_volume"})["content"])
        parsed_data["issue"] = str(soup.find('meta', attrs={"name":"citation_issue"})["content"])
        parsed_data["date"] = str(soup.find('meta', attrs={"name":"citation_date"})["content"])

        parsed_data["pubmed_url"] = str(soup.find('meta', attrs={"name":"citation_abstract_html_url"})["content"])
        parsed_data["issn"] = str(soup.find('meta', attrs={"name":"citation_issn"})["content"])



    else:
        logger.debug("non 200 response"+str(response.status_code))
            
    ##<meta property="og:title" content="Updates in NMOSD and MOGAD Diagnosis and Treatment: A Tale of Two Central Nervous System Autoimmune Inflammatory Disorders - PubMed">
    

    return parsed_data



def meta_from_doi(in_doi):
    
    logger.debug("in_meta_from_doi")


    pmid_data=get_pmid_content(in_doi) 
##    this_metapub=meta_from_pmid(this_pmid[0])
    return pmid_data

def a_list_to_creators_dict(in_mp_a_list):
    logger.debug("in a_list_to_creators")
    artu_detour=[]
    for ii in in_mp_a_list:
        this_artu={'creatorType':'author','firstName':ii.fore_name,'lastName':ii.last_name}
        artu_detour.append(this_artu)
    return artu_detour

def author_str_to_cr_dict(in_str):
    in_str=in_str.replace("<span class=\"docsum-authors full-authors\">","")
    in_str=in_str.replace("</span>","")
    out_str=in_str.split(",")
    artu_detour=[]
    for ii in out_str:
        this_artu={'creatorType':'author','firstName':ii.split()[0],'lastName':ii.split()[-1]}
        artu_detour.append(this_artu)

    return this_artu



test=False

if test:
    print("runninf f_metapub in test mode, using local hrml file")
    print(meta_from_href("","/config/workspace/pdf_notes/demdem.html"))

    
"""    for child in all_soup.descendants:

        if child.name:
            print(child.name)
    pooper=all_soup.find('div',class_=["abstract-content"],id="eng-abstract").find('p').string
    print(pooper.find('p').string)

print(pooper)
    abstract_res = str(soup.find('div',id_=["eng-abstract"],class_=['abstract-content','selected']).string) """  