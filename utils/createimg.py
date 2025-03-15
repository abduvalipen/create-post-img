from PIL import Image, ImageDraw, ImageFont
import os
import requests
from io import BytesIO
from data import config
from loader import db



def download_image_from_telegram(file_id, bot_token):
    url = f'https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}'
    response = requests.get(url)
    print(response.json())
    file_path = response.json()['result']['file_path']
    
    image_url = f'https://api.telegram.org/file/bot{bot_token}/{file_path}'
    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))
    return image


def createshablon_funk(Id, jobs, holat, kompany, salarys,chat_id):
    company = db.select_company(user_id=chat_id)
    if company:
        fileid = company[6]
    else:
        for i in db.select_all_templatetest():
            fileid = i[0]


    bot_token=config.BOT_TOKEN
    file_id = fileid

    image = download_image_from_telegram(file_id, bot_token)
    draw = ImageDraw.Draw(image)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
 # image.save(f"{chat_id}.png")
    # image.show()
    # IMAGE_FOLDER = os.path.join(BASE_DIR, "imgs", "1111.png") 
    # image = Image.open(IMAGE_FOLDER) 
    # draw = ImageDraw.Draw(image)

    FONT_PATH = os.path.join(BASE_DIR , "Roboto.ttf")


    font = ImageFont.truetype(str(FONT_PATH), size=50)
    if len(str(Id)) == 1:
        id = "#" + str(Id)  
        position = (280, 250)
        color = "black" 
        draw.text(position, id, fill=color, font=font)
    elif len(str(Id)) == 2:
        id = "#" + str(Id)  
        position = (260, 250)    
        color = "black" 
        draw.text(position, id, fill=color, font=font)
    elif len(str(Id)) == 3:
        id = "#" + str(Id)  
        position = (240, 250)    
        color = "black" 
        draw.text(position, id, fill=color, font=font)
    elif len(str(Id)) == 4:
        id = "#" + str(Id)  
        position = (230, 250)    
        color = "black" 
        draw.text(position, id, fill=color, font=font)
    elif len(str(Id)) == 5:
        font = ImageFont.truetype(str(FONT_PATH), size=40)
        id = "#" + str(Id)  
        position = (230, 255)    
        color = "black" 
        draw.text(position, id, fill=color, font=font)
    else:
        font = ImageFont.truetype(str(FONT_PATH), size=40)
        id = "#" + str(Id)[:5]  
        position = (230, 255)    
        color = "black" 
        draw.text(position, id, fill=color, font=font)


    font = ImageFont.truetype(str(FONT_PATH), size=60)  
    job = str(jobs) 
    position = (430, 250)    
    color = "white" 
    draw.text(position, job, fill=color, font=font)



    font = ImageFont.truetype(str(FONT_PATH), size=60)  
    oflayn_or_onlayn = str(holat)
    position = (410, 480)
    color = "white"
    draw.text(position, oflayn_or_onlayn, fill=color, font=font)



    font = ImageFont.truetype(str(FONT_PATH), size=60)  
    kompany_name = str(kompany)
    position = (410, 620)
    color = "white"
    draw.text(position, kompany_name, fill=color, font=font)


    font = ImageFont.truetype(str(FONT_PATH), size=60)  
    salary = str(salarys)
    position = (410, 760)
    color = "white"
    draw.text(position, salary, fill=color, font=font)

    IMG_DIR = os.path.join(BASE_DIR, "testresultimg")

    image_path = os.path.join(IMG_DIR, f"{chat_id}.png")
    image.save(image_path)

   

    return image_path
