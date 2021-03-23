from PIL import Image
import sys
from pathlib import Path

image = "raspberry_24x30.jpg"
im_name = Path(image).stem

# Load image
im = Image.open(image)

width, height = im.size
# If image width not divisible by 8, correct it
adj_width = width + width % 8

if adj_width == width:
    print("Image size: {}x{}".format(adj_width, height))
else:
    print("Adjusted image width")
    print("Adjusted image size: {}x{}".format(adj_width, height))
    print("Original image size: {}x{}".format(width, height))

# Create buffer for pixel data
buf = bytearray(height*adj_width//8)
i = 0
for byte in range(len(buf)):
    for bit in range(7, -1, -1):
        if i % adj_width < width:
            px =  im.getpixel((i % adj_width, i // adj_width))
            if px[0] < 128 or px[1] < 128 or px[2] < 128:
                buf[byte] |= 1 << bit
        i += 1

# Save data to file
print("Saving data to file: {}".format(im_name + ".py"))
with open(im_name + ".py", "w") as f:
    f.write("name = '{}'\nwidth = {}\nheight = {}\nformat = '{}'\nimg = {}"
            .format(im_name, adj_width, height, "MONO_HLSB", buf))

print("Done!")
