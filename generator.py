from PIL import Image, ImageDraw, ImageFont
from random import randint

# general settings
width = 1920
height = 1080
font = ImageFont.truetype("Monaco.ttf", size = 20)

# grab random QA
with open('QA.md') as f:
	contents = f.read()
	qa_texts = contents.split("---")

qa_index = randint(0, len(qa_texts) - 1)

# generate picture
message = qa_texts[qa_index]
img = Image.new('RGB', (width, height), color = 'blue')

imgDraw = ImageDraw.Draw(img)

imgDraw.text((10, 10), message, font = font,  fill=(255, 255, 0))

img.save('pic/1.png')
