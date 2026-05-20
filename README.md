# Proposed workflow
* PDF -> flat per file metafile (md, flat json or similar. Each annotation carries the unique id of the pdf)
* The flat metafile is versioned
* 1-2 databases can be aggregated, one for the pdfs and one for the annotations
* PDF -> also creates folder (with the pdf unique name) with jpg from box annotations and metafiles
* pdf unique name contains info on pdf and first date of reading, making it unique and human readable
  * ex: smith_NMOSD_2015_260520/
  * ex: smith_NMOSD_2015_260520/Smith_NMOSD_2015_260520.pdf


# pdf_notes
* [ ] alternative to doi if pdf from book
* [ ] backup, zip inkl pdf ipynb and all? github? linux backup tool with versioning per file? 
* [ ] annot func #_ins(hl) or #_ihl copys/inserts the highlight in the annotation or maybe create function that works with notebook
* [ ] function to use internal jupy md ipy md converions and move md and images proposedto sb and re index tb
* [ ] function to write to zotero.. perhaps as backup




New branch just in case
