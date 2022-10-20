from PIL import Image, ImageDraw, ImageFont
from random import sample

# general settings
width = 1920
height = 1080
num_pics = 10
font = ImageFont.truetype("Monaco.ttf", size = 17)

# grab random QA
with open('texts/QA.md') as f:
	contents = f.read()
	qa_texts = contents.split("---")


# generate picture
qa_indices = sample(range(len(qa_texts)), num_pics)
for i in range(num_pics):
	message = qa_texts[qa_indices[i]]
	img = Image.new('RGB', (width, height), color = 'black')

	imgDraw = ImageDraw.Draw(img)

	imgDraw.text((50, 100), message, font = font,  fill=(255, 255, 255))

	imgName = 'pic/'+ str(i) + '.png'
	img.save(imgName)
