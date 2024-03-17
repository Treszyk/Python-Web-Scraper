import jsonpickle
import io
import csv
import openpyxl
def convert_to_JSON(opinions:list):
    return jsonpickle.encode(opinions, unpicklable=False)

def convert_to_CSV(opinions:list):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "author", "recommended", "score", "verified", "review_date", "buy_date", "likes", "dislikes", "content", "plus", "minus"])

    for opinion in opinions:
        writer.writerow(opinion.serialize())

    output_val = output.getvalue()
    output.close()

    return output_val

def convert_to_XLSX(opinions:list):
    output = io.BytesIO()
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    
    sheet.append(["id", "author", "recommended", "score", "verified", "review_date", "buy_date", "likes", "dislikes", "content", "plus", "minus"])
    for opinion in opinions:
        sheet.append(opinion.serialize()) 

    workbook.save(output)   
    output_val = output.getvalue()
    output.close() 

    return output_val