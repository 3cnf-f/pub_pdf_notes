import json
import nbformat as nbf
import f_js_md_data_n_tools as f_d

#json_to_ipynb.py

# see example_ipynb.txt
# create function that can be run directly from pdf2_pdf_t_json
# or from one of the json files 
#      it exports pdf annot as blocks of ipynb that can be edited
#       also it could be used to display and edit results from searches 
# that run over more than one article or more than one reading of the same article

# (also always keep exporting as json)

def save_notebook(in_notebook,in_writepath):
    nbf.write(in_notebook,in_writepath)
def dic_copy_keysinlist(in_dic,in_list):
    out_dic={}
    for aa in in_list:
        try:
            if in_dic[aa]:
                out_dic[aa]=in_dic[aa]
            else:
                out_dic[aa]="N/A"
        except:
            out_dic[aa]="N/A"
    return out_dic

def any_ink_cell(in_json):
    this_source_Q=[
        "annot_uuid4",
        "page_no",
        "img_filename",
        "highlighted_text", 
        "annotation_text",
        "rect", 
        "file_uuid4",
        "entry_type",
        "DOI",
        "title",
        "document_type",
        "course",
        "main_author",
        "date"
    ]
    
    
    
    e_sd=dic_copy_keysinlist(in_json,this_source_Q)
    
    

    this_meta_dic=in_json
    out_cell=nbf.v4.new_markdown_cell(source=["p:("+str(e_sd["page_no"])+")\n",
    "!["+str(e_sd["img_filename"])+"]("+str(e_sd["img_filename"])+")\n",
    "#### "+str(e_sd["annotation_text"])+"\n",
    
    
    
    
    
    
    ],metadata=e_sd)
    return out_cell

def rectangle_cell(in_json):
    this_source_Q=[
        "annot_uuid4",
        "page_no",
        "img_filename",
        "highlighted_text", 
        "annotation_text",
        "rect", 
        "file_uuid4",
        "entry_type",
        "DOI",
        "title",
        "document_type",
        "course",
        "main_author",
        "date"
    ]
    
    
    
    e_sd=dic_copy_keysinlist(in_json,this_source_Q)
    
    

    this_meta_dic=in_json
    out_cell=nbf.v4.new_markdown_cell(source=["p:("+str(e_sd["page_no"])+")\n",
    "!["+str(e_sd["img_filename"])+"]("+str(e_sd["img_filename"])+")\n",
    "#### "+str(e_sd["annotation_text"])+"\n",
    
    
    
    
    
    
    ],metadata=e_sd)
    return out_cell
def highlight_cell(in_json):
    this_source_Q=[
        "annot_uuid4",
        "page_no",
        "img_filename",
        "highlighted_text", 
        "annotation_text",
        "rect", 
        "entry_type",
        "DOI",
        "file_uuid4",
        "title",
        "course",
        "document_type",
        "main_author",
        "date"
    ]
    
    
    
    e_sd=dic_copy_keysinlist(in_json,this_source_Q)
    
    

    this_meta_dic=in_json
    out_cell=nbf.v4.new_markdown_cell(source=["p:("+str(e_sd["page_no"])+")\n",
    "!["+str(e_sd["img_filename"])+"]("+str(e_sd["img_filename"])+")\n",
    "#### "+str(e_sd["annotation_text"])+"\n",
    
    
    
    
    
    
    ],metadata=e_sd)
    return out_cell
 

def header_cell(in_json):
    this_source_Q=[""
    "date",
    "DOI",                       
    "title",                                                                      
    "main_author",                                      
    "journal",                
    "abstract",                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    "pubmed_url",
    "file_uuid4",
    "filename",
    "file_datetime_stockholm",
    "pmid",
    "main_authors",
    "journal",
    "abstract",
    "volume",
    "issue",
    "issn",
    "course",
    "document_type"
    ]
    
    
    
    e_sd=dic_copy_keysinlist(in_json,this_source_Q)
    if e_sd["document_type"]=="journal_article":
        out_cell=nbf.v4.new_markdown_cell(source=["## "+str(e_sd["title"])+"\n",
        
        '#### '+str(e_sd["main_author"])+'  -   '+str(e_sd["journal"])+'  -   '+str(e_sd["date"])+'\n', 
        '[DOI: '+str(e_sd["DOI"])+']('+str(e_sd["pubmed_url"])+')\n',
        '##### Abstract: \n',
        str(e_sd["abstract"])+'\n',
        
        
        
        
        
        ],metadata=e_sd)
    if e_sd["document_type"]=="handout":
        out_cell=nbf.v4.new_markdown_cell(source=["## "+str(e_sd["title"])+"\n","#### Document type: "+str(e_sd["document_type"])+"\n","#### Course: "+str(e_sd["course"])+"\n",
        
        '#### '+str(e_sd["main_author"])+'  -   '+str(e_sd["date"])+'\n', 
        
        
        
        
        
        ],metadata=e_sd)
    
    
    

    this_meta_dic=in_json
    return out_cell
 


def make_notebook_fromjson(in_json):
    nb_this=nbf.v4.new_notebook()
    
    
    #create header_cell for this cell
    this_header_cell=header_cell(in_json)
    nb_this.cells.append(this_header_cell)

    #create meta for this cell
    #this_meta=json_to_meta(in_json)

    #create md for this cell
    #this_md=json_to_md(in_json)
    
    for xx in in_json.keys():
        if xx[:7]=="ANNOT#-":
            print(xx[7:]+"  <Annotation is processing...")
            if in_json[xx]["entry_type"]=="highlight":
                nb_this.cells.append(highlight_cell(in_json[xx]))
            if in_json[xx]["entry_type"]=="rectangle":
                nb_this.cells.append(rectangle_cell(in_json[xx]))
            if in_json[xx]["entry_type"]=="non_blue_ink" or in_json[xx]["entry_type"]=="blue_ink":
                nb_this.cells.append(any_ink_cell(in_json[xx]))

        else:
            print(xx+" <is not an annotation\n")
    

    return nb_this

def l_j_mk_n_sv_ipynb(in_jsname,in_ipyname):
    print(in_jsname)

    with open(in_jsname,"r") as testjson_file:
        test_json=json.load(testjson_file)
    test_notebook=make_notebook_fromjson(test_json)
    save_notebook(test_notebook,in_ipyname)

test=False

testjsonpath="/config/workspace/pdf_notes/dem2/dem2.json"
out_testpath="/config/workspace/pdf_notes/dem2/dem2.ipynb"

if test==True:
    #test_json=f_d.load_json_for_conversion(testjsonpath)
    print("tst")
    with open(testjsonpath,"r") as testjson_file:
        test_json=json.load(testjson_file)
    test_notebook=make_notebook_fromjson(test_json)
    save_notebook(test_notebook,out_testpath)