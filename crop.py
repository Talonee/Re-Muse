from PIL import Image 

# Opens a image in RGB mode 
im = Image.open("covers/mylove.jpg") 
width, height = im.size 
print(width)
# Setting the points for cropped image 
left = (1280 - 720) / 2
top = 0
right = 1280 - left
bottom = 720

# # Cropped image of above dimension 
# # (It will not change orginal image) 
im1 = im.crop((left, top, right, bottom)) 

# # Shows the image in image viewer 
# im1.show() 
im1.save("covers/crop.jpg")