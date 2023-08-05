from poppdf.pdf import image_from_path, xml_from_path, text_from_path, pdfinfo_from_path, image_info_from_path
from poppdf.common import parse_pages
import pytesseract
from poppdf.common import Rectangle
from poppdf.alto_xml import process_alto_xml
from math import isclose
from poppdf.common import update_object_dict_pos
from kdmt.geometry import rectangle_intersect
from math import isclose
from kdmt.strings import commonOverlapIndexOf
import cv2
from poppdf.pdf import xml_ocr_from_image

class PdfPage():
    def __init__(self, page):
        self.text_lines=sorted(page["texts"], key=lambda x: (x["bottom"], x["left"]))
        self.words=[]
        self.images=page["images"]
        self.width=page["width"]
        self.height=page["height"]
        self.number=page["number"]
        self.page_image=None
        self.text=None

    @property
    def bbox(self):
        if self.page_image is None:
            return {}

        return {"left":0, "top":0, "right":self.width,"bottom":self.height}

    @staticmethod
    def rescale_page(text_lines, width_ratio, height_ratio):

        for tl in text_lines:
            tl["top"]*=height_ratio
            tl["left"] *= width_ratio
            tl["right"] *= width_ratio
            tl["bottom"] *= height_ratio
            tl["height"]=tl["bottom"]-tl["top"]
            tl["width"]=tl["right"]-tl["left"]
            update_object_dict_pos(tl)
        return text_lines
    def rescale_page_to_image(self):
        return self.rescale_page(self.page_image.size[0], self.page_image.size[1])
class PdfDocument():
    def __init__(self, path, first_page=None, last_page=None, userpw=None, use_ocr=False, laguages="eng"):
        self.pdf_info = pdfinfo_from_path(path, userpw)

        self.pdf_pages=[]
        xml_data= xml_from_path(pdf_path=path, first_page=first_page, last_page=last_page)
        pages=parse_pages(xml_data)

        for p_num, p in pages.items():
            page=PdfPage(p)
            size=(p["width"], p["height"])
            page.page_image=image_from_path(pdf_path=path, first_page=p_num, last_page=p_num,size=size, grayscale=True)[0]

            page.text = text_from_path(path, first_page=p_num, last_page=p_num)
            ocr_text_lines=[]

            if use_ocr or page.text.strip()=="":
                page_image=image_from_path(pdf_path=path, first_page=p_num, last_page=p_num,dpi=300)[0]


                options = "--psm 3"
                alto_xml=pytesseract.image_to_alto_xml(page_image,config=options, lang=laguages)
                ocr_text_lines, page_text, confidence=process_alto_xml(alto_xml)
                for l in ocr_text_lines:
                    print(l["value"])
                ocr_text_lines=PdfPage.rescale_page(ocr_text_lines, page.page_image.size[0]/page_image.size[0],  page.page_image.size[1]/page_image.size[1])
            if page.text.strip()=="":
                page.text_lines=ocr_text_lines
                page.text=page_text
            elif use_ocr:
                text_lines_to_remove=[]
                for tl in page.text_lines:
                    print("text_line", tl["value"])
                    if (tl["value"]=="5 PLUS GRANDES POSITIONS"):
                        print("ha")
                    matches= self.__find_match(ocr_text_lines, tl)
                    if not matches:
                        print("to remove: ", tl["value"])
                        text_lines_to_remove.append(tl)
                    else:
                        print("not to remove: ", tl["value"])
                page.text_lines=[x for x in page.text_lines if x not in text_lines_to_remove]

            self.pdf_pages.append(page)

    def __find_match(self, sorted_list, item):

        i=0
        while i < len(sorted_list) and not isclose(sorted_list[i]["top"], item["top"], abs_tol=item["height"] / 10):
            i+=1


        return_set=[]
        if i<len(sorted_list):
            while i<len(sorted_list) and isclose(sorted_list[i]["top"], item["top"], abs_tol=item["height"]/10):
                return_set.append(sorted_list[i])
                i+=1
        return return_set



if __name__=="__main__":
    from poppdf.alto import String
    image=image_from_path("/Users/mohamedmentis/Dropbox/My Mac (MacBook-Pro.local)/Documents/Mentis/Development/Python/pdf2text/pdf3/FR_FFG_GlobalFlex_Sust_DisR.pdf", first_page=1, last_page=1)[0]
#    pdf=PdfDocument("/Users/mohamedmentis/Dropbox/My Mac (MacBook-Pro.local)/Documents/Mentis/Development/Python/pdf2text/pdf3/FR_FFG_GlobalFlex_Sust_DisR.pdf", first_page=2, last_page=2, use_ocr=True)
    lines=xml_ocr_from_image(image, size=(850, 1250))
    for tl in lines.extract_text_lines():
        print(' '.join(s.content for s in tl.strings if isinstance(s, String)))