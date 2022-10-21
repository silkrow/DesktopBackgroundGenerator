from PIL import Image, ImageDraw, ImageFont
from random import sample

# general settings
width = 1920
height = 1080
num_pics = 10
qa_x = 100
qa_y = 50
voc_x = 1100
voc_y = 50
greet1_x = 1300
greet1_y = 1000

qa_font = ImageFont.truetype("Optima.ttc", size = 24)
voc_font = ImageFont.truetype("Optima.ttc", size = 20)
greet1_font = ImageFont.truetype("Bradley Hand Bold.ttf", size = 30)

# grab random QA
with open('texts/QA.md') as f:
	contents = f.read()
	qa_texts = contents.split("---")

# grab random vocabulary
with open('texts/voc.md') as f:
	contents = f.read()
	voc_texts = contents.split("---")

# Greeting message
greet1 = "Please please get things done EARLY!"

# generate picture
qa_indices = sample(range(len(qa_texts)), num_pics)
voc_indices = sample(range(len(voc_texts)), len(voc_texts))
for i in range(num_pics):
	qa_texts[qa_indices[i]]
	img = Image.new('RGB', (width, height), color = (238,232,170))

	imgDraw = ImageDraw.Draw(img)

	imgDraw.text((qa_x, qa_y), qa_texts[qa_indices[i]], font = qa_font,  fill=(0, 0, 0))
	imgDraw.text((voc_x, voc_y), voc_texts[voc_indices[1]], font = voc_font,  fill=(0, 0, 0))
	imgDraw.text((greet1_x, greet1_y), greet1, font = greet1_font,  fill=(0, 0, 0))
	imgName = 'pic/'+ str(i) + '.png'
	img.save(imgName)
