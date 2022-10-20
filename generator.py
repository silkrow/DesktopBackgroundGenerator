from PIL import Image, ImageDraw, ImageFont

# general settings
width = 512
height = 512
font = ImageFont.truetype("Monaco.ttf", size = 20)

# grab random QA
qa_text = ""
i = 0
with open('QA.md') as f:
	contents = f.readlines()
	for line in contents:
		qa_text = qa_text + line
		i = i + 1
		if i == 20:
			break


# generate picture
message = qa_text
img = Image.new('RGB', (width, height), color = 'blue')

imgDraw = ImageDraw.Draw(img)

imgDraw.text((10, 10), message, font = font,  fill=(255, 255, 0))

img.save('pic/1.png')
