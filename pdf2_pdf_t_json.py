



import fitz  # PyMuPDF
import os
import uuid,json
import f_pdf_tools as f_p
import f_metapub as f_mp
import f_blue_ink as f_bi
import logging

#tar en pdf och exporterar som json, övriga uppgifter sköts av andra program eller moduler annotation av highlight, square och ink typ.
#För ink och square så sparas en kopia på drive och en kopia laddas upp till hashim.se via sftp
# Define the functions for SFTP and annotation processing (as previously discussed)
# ...

 
logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(filename='example.log', encoding='utf-8', format=FORMAT)
logger.setLevel(logging.DEBUG)
 
def rect_to_tuple(rec_in):
    return str(rec_in)

# Process highlight annotations
def extract_highlight(annot, page,img_folder, img_counter,in_pdf_path):
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
      # Set a higher DPI (e.g., 144 for double the default resolution)
    zoom_x = 4.0  # Horizontal zoom
    zoom_y = 4.0  # Vertical zoom
    mat = fitz.Matrix(zoom_x, zoom_y)  # Transformation matr
    pix = page.get_pixmap(matrix=mat, clip=expand_rect)
    img_name = f"{os.path.basename(in_pdf_path).split('.')[0]}-img{img_counter}.png"
    img_path = os.path.join(img_folder, img_name)
    if toggle_save_img:
        pix.save(img_path)
    if toggle_print==True:
        print(annot_text)
    return  img_name,annot_text, note_text

def process_square(annot, page, img_folder, img_counter,in_pdf_path):
    rect = annot.rect
    words = page.get_text("words")
    highlighted_words = [w for w in words if fitz.Rect(w[:4]).intersects(rect)]
    annot_text = " ".join(w[4] for w in highlighted_words)
     # Set a higher DPI (e.g., 144 for double the default resolution)
    zoom_x = 4.0  # Horizontal zoom
    zoom_y = 4.0  # Vertical zoom
    mat = fitz.Matrix(zoom_x, zoom_y)  # Transformation matr
    pix = page.get_pixmap(matrix=mat, clip=rect)
    img_name = f"{os.path.basename(in_pdf_path).split('.')[0]}-img{img_counter}.png"
    img_path = os.path.join(img_folder, img_name)
    if toggle_save_img:
        pix.save(img_path)

  
    # Extract annotation popup text
    popup_text = annot.info["content"] if "content" in annot.info else "No note"
    popup_text= popup_text.replace("\n", " ") #ta bort cr cl
    popup_text= popup_text.replace("\r", " ") #ta bort cr cl
    if toggle_print==True:
        print(annot_text)
    #print(popup_text)
    return img_name, popup_text, annot_text  # Return image name, popup text, and highlighted words

def process_ink(annot, page, img_folder, img_counter,in_pdf_path):
    rect = annot.rect
    words = page.get_text("words")
    highlighted_words = [w for w in words if fitz.Rect(w[:4]).intersects(rect)]
    annot_text = " ".join(w[4] for w in highlighted_words)
     # Set a higher DPI (e.g., 144 for double the default resolution)
    zoom_x = 4.0  # Horizontal zoom
    zoom_y = 4.0  # Vertical zoom
    mat = fitz.Matrix(zoom_x, zoom_y)  # Transformation matr
    pix = page.get_pixmap(matrix=mat, clip=rect)
    img_name = f"{os.path.basename(in_pdf_path).split('.')[0]}-img{img_counter}.png"
    img_path = os.path.join(img_folder, img_name)
    if toggle_save_img:
        pix.save(img_path)
 

    # Extract annotation popup text
    popup_text = annot.info["content"] if "content" in annot.info else "No note"
    popup_text= popup_text.replace("\n", " ") #ta bort cr cl
    popup_text= popup_text.replace("\r", " ") #ta bort cr cl
    if toggle_print==True:
        print(annot_text)
    #print(popup_text)
    return img_name, popup_text,annot_text  # Return image name and popup text




# Process the PDF and extract annotations
def process_pdf_annotations(pdf_path, img_folder):
    doc = fitz.open(pdf_path)
    annotations_parent_dict={}
    annotations_data = []
    img_counter = 1
    this_meta=None
    this_doi=f_p.find_doi(doc[0])
    if this_doi!=None:
        print("Doi on page 0: "+str(this_doi))
        this_meta=f_mp.meta_from_href(this_doi,"") #remember to this_doi,"" 
    else:
        this_meta=f_p.meta_from_annot(doc[0])
    this_file_uuid4=str(uuid.uuid4())

    file_datetime_stockholm=f_p.datetime_stockholm()



    annotations_parent_dict.update({"file_uuid4":this_file_uuid4,"filename":pdf_path,"file_datetime_stockholm":file_datetime_stockholm})

    if this_meta and this_doi!=None:
        annotations_parent_dict.update({"document_type":"journal_article",
            "pmid":str(this_meta["pmid"]),
            "DOI":this_doi,
            "title":str(this_meta["title"]),
            "main_authors":str(this_meta["main_authors"]),
            "main_author":str(this_meta["main_author"]),

            "journal":str(this_meta["journal"]),
            "abstract":str(this_meta["abstract"]),
            "volume":str(this_meta["volume"]),
            "issue":str(this_meta["issue"]),

            "pubmed_url":str(this_meta["pubmed_url"]),
            "issn":str(this_meta["issn"]),
            "date":str(this_meta["date"]),
            "course":"N/A",
            })

    if this_meta and this_doi==None:
        #assume handour
        annotations_parent_dict.update({"document_type":"handout",
            "title":str(this_meta["title"]),
            "main_author":str(this_meta["main_author"]),
            "course":str(this_meta["course"]),
            "pmid":"N/A",
            "DOI":"N/A",
            "main_authors":"N/A",

            "journal":"N/A",
            "abstract":"N/A",
            "volume":"N/A",
            "issue":"N/A",

            "pubmed_url":"N/A",
            "issn":"N/A",

            "date":str(this_meta["date"]) })
    
            
       ## ,        "pages":this_meta.pages,"issue":this_meta.issue,"volume":this_meta.volume,"doi":this_meta.doi,"pmid":this_meta.pmid,"publication":this_meta.journal,"title":this_meta.title,"abstract":this_meta.abstract,"year":this_meta.year})
 

    for p_no,page in enumerate(doc):


        for annot in page.annots():
            this_annot={}

            if annot.type[0] == 8:  # Highlight

                this_annot["entry_type"]="highlight"
                this_annot["annot_uuid4"]=str(uuid.uuid4())
                this_annot["page_no"]=p_no
                this_annot["img_filename"],this_annot["highlighted_text"],  this_annot["annotation_text"] = extract_highlight(annot, page,img_folder, img_counter,pdf_path)
                this_annot["rect"]=rect_to_tuple(annot.rect)
                this_annot["file_uuid4"]=this_file_uuid4          
                this_annot["main_author"]=this_meta["main_author"]
                this_annot["date"]=this_meta["date"]
                this_annot["title"]=this_meta["title"]
                this_annot["course"]=annotations_parent_dict["course"]



                annotations_parent_dict.update({"ANNOT#-"+str(img_counter):this_annot})
                img_counter += 1
 
            elif annot.type[0] == 4:  # Square
                this_annot["entry_type"]="rectangle"
                this_annot["annot_uuid4"]=str(uuid.uuid4())
                this_annot["page_no"]=p_no
                this_annot["img_filename"], this_annot["annotation_text"], this_annot["highlighted_text"]   =  process_square(annot, page, img_folder, img_counter,pdf_path)
                this_annot["rect"]=rect_to_tuple(annot.rect)
                this_annot["DOI"]=this_doi      

                this_annot["file_uuid4"]=this_file_uuid4                
                this_annot["main_author"]=this_meta["main_author"]
                this_annot["date"]=this_meta["date"]
                this_annot["title"]=this_meta["title"]
                this_annot["course"]=annotations_parent_dict["course"]
                annotations_parent_dict.update({"ANNOT#-"+str(img_counter):this_annot})
                
                img_counter += 1
            elif annot.type[0]== 15: # ink
                if f_bi.checkbluey(annot): 
                    this_annot["entry_type"]="blue_ink"
                else:
                    this_annot["entry_type"]="non_blue_ink"

                this_annot["annot_uuid4"]=str(uuid.uuid4())
                this_annot["page_no"]=p_no
                this_annot["img_filename"], this_annot["annotation_text"], this_annot["highlighted_text"] = process_ink(annot, page, img_folder, img_counter,pdf_path)
                this_annot["rect"]=rect_to_tuple(annot.rect)
                this_annot["DOI"]=this_doi      

                this_annot["file_uuid4"]=this_file_uuid4                
                this_annot["main_author"]=this_meta["main_author"]
                this_annot["date"]=this_meta["date"]
                this_annot["title"]=this_meta["title"]
                this_annot["course"]=annotations_parent_dict["course"]
                annotations_parent_dict.update({"ANNOT#-"+str(img_counter):this_annot})


                img_counter += 1
            annotations_parent_dict.update(this_annot)


    doc.close()
    #annotations_parent_dict.update({"i":{"a":"bla","ooo":"laa"}})
    return annotations_parent_dict
toggle_print=True
toggle_save_img=True