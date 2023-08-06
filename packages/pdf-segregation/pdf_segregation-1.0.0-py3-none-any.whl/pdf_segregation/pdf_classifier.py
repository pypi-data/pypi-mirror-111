## Load libraries
#
import PyPDF2

## Digital and Non digital classifier
#     
def digital_nondigital_classifier(files):
    pdf_reader = PyPDF2.PdfFileReader(str(files), 'rb')
    total_pages = pdf_reader.getNumPages()
    curr_page = 0
    d_flag_count = 0
    non_d_flag_count = 0
    for curr_page in range(0, total_pages):
        page_data = pdf_reader.getPage(curr_page)
        if '/Font' in page_data['/Resources']:     
            d_flag_count = d_flag_count + 1
        else:
            non_d_flag_count = non_d_flag_count + 1
    
    if(d_flag_count > 0 and non_d_flag_count == 0):
        return "Digital"
    elif(non_d_flag_count > 0 and d_flag_count == 0):
        return "Non-Digital"
    else:
        return "Mixed"