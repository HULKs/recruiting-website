import vision

# Get a reference to the image above
image = vision.get_ball_image()

# Some test code ... you can replace/remove these lines
print("Hello, world!")
print(image)
print(f"Red value of pixel in the top left corner: {image.at(x=0, y=0).r}")

# Draw a circle onto the image at position [25, 35] with a radius of 20 in red 
vision.plot_ball_detection(image, x=25, y=35, radius=20, r=255, g=0, b=0)

# write image to file
vision.write_ball_image(image)
