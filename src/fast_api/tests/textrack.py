import boto3
import io
import json
from PIL import Image, ImageDraw

def draw_bounding_box(key, val, width, height, draw):
    if "Geometry" in key:
        box = val["BoundingBox"]
        left = width * box['Left']
        top = height * box['Top']
        draw.rectangle([left, top, left + (width * box['Width']), top + (height * box['Height'])],
                       outline='black')

def print_labels_and_values(field):
    # Verificar si hay un valor detectado (ValueDetection)
    if "ValueDetection" in field:
        print("Field Type: {}".format(field.get("Type")["Text"]))
        print("Detected Value: {}".format(field.get("ValueDetection")["Text"]))
    else:
        print("No values returned")

def process_expense_analysis(s3_connection, client, bucket, document):
    s3_object = s3_connection.Object(bucket, document)
    s3_response = s3_object.get()
    stream = io.BytesIO(s3_response['Body'].read())
    image = Image.open(stream)

    response = client.analyze_expense(
        Document={'S3Object': {'Bucket': bucket, 'Name': document}})

    width, height = image.size
    draw = ImageDraw.Draw(image)

    output_data = {
        "SummaryFields": [],
        "LineItemsGroup": {
            "productos": []
        }
    }

    for expense_doc in response["ExpenseDocuments"]:
        # Procesar SummaryFields
        for summary_field in expense_doc["SummaryFields"]:
            if "ValueDetection" in summary_field:
                output_data["SummaryFields"].append({
                    "Field": summary_field["Type"]["Text"],
                    "label": "Unknown",
                    "value": summary_field["ValueDetection"]["Text"]
                })

        # Procesar LineItems
        for line_item_group in expense_doc["LineItemGroups"]:
            for line_item in line_item_group["LineItems"]:
                item_name = ""
                item_price = ""

                for expense_field in line_item["LineItemExpenseFields"]:
                    field_type = expense_field["Type"]["Text"]
                    if field_type == "ITEM":
                        item_name = expense_field["ValueDetection"]["Text"].split()[0].capitalize()
                    elif field_type == "PRICE":
                        item_price = expense_field["ValueDetection"]["Text"].replace("-", "")

                if item_name and item_price:
                    output_data["LineItemsGroup"]["productos"].append({
                        "Items": item_name,
                        "valor": item_price
                    })

        # Para dibujar los bounding boxes (opcional)
        for line_item_group in expense_doc["LineItemGroups"]:
            for line_item in line_item_group["LineItems"]:
                for expense_field in line_item["LineItemExpenseFields"]:
                    for key, val in expense_field["ValueDetection"].items():
                        if "Geometry" in key:
                            draw_bounding_box(key, val, width, height, draw)

        for summary_field in expense_doc["SummaryFields"]:
            if "LabelDetection" in summary_field:
                for key, val in summary_field["LabelDetection"].items():
                    draw_bounding_box(key, val, width, height, draw)

    # Mostrar el JSON de salida formateado
    print(json.dumps(output_data, indent=4))

    # Mostrar la imagen (opcional)
    image.show()
    #generates the image to verify the correct analysis
    image.save("ouyput_image.png") # 

def main():
    session = boto3.Session(profile_name='default')
    s3_connection = session.resource('s3')
    client = session.client('textract', region_name='us-east-1')
    bucket = 's3customlabels'
    document = 'rgg1_the_home_depot.jpeg'
    process_expense_analysis(s3_connection, client, bucket, document)

if __name__ == "__main__":
    main()
