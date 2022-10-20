from PIL import Image, ImageDraw, ImageFont
from random import sample

# general settings
width = 1920
height = 1080
num_pics = 10
qa_x = 100
qa_y = 100
voc_x = 800
voc_y = 100
qa_font = ImageFont.truetype("Monaco.ttf", size = 15)
voc_font = ImageFont.truetype("Monaco.ttf", size = 15)

# grab random QA
with open('texts/QA.md') as f:
	contents = f.read()
	qa_texts = contents.split("---")

# grab random vocabulary
with open('texts/voc.md') as f:
	contents = f.read()


# generate picture
qa_indices = sample(range(len(qa_texts)), num_pics)
voc_message = contents
for i in range(num_pics):
	qa_texts[qa_indices[i]]
	img = Image.new('RGB', (width, height), color = 'black')

	imgDraw = ImageDraw.Draw(img)

	imgDraw.text((qa_x, qa_y), qa_texts[qa_indices[i]], font = qa_font,  fill=(255, 255, 255))
	imgDraw.text((voc_x, voc_y), voc_message, font = voc_font,  fill=(255, 255, 255))

	imgName = 'pic/'+ str(i) + '.png'
	img.save(imgName)
