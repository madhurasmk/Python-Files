from markitdown import MarkItDown
md1 = MarkItDown()
htmlResult = md1.convert("Good Articles.html")
print(htmlResult.text_content)
pdfResult = md1.convert(".pdf")
print(pdfResult.text_content)

docxResult = md1.convert("Generative AI Foundations.docx")
print(docxResult.text_content)
excelResult = md1.convert(".xlsx")
print(excelResult.text_content)
# Result = md1.convert("Good Articles.html")
# print(pdfResult.text_content)
