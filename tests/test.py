import fitz

doc = fitz.open("zona impianti.pdf")

for page in doc:
    rect = fitz.EMPTY_RECT()  # start with the standard empty rectangle
    print(page.mediabox)
    print(page.get_pixmap())
    for item in page.get_bboxlog():
        rect |= item[1]  # join this bbox into the result
    # rect now wraps all page content
    print(rect)