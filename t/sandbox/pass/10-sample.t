use SandboxTest {
  DESCRIPTION => <<~'EOF',
      Make sure the sample code passes.
      EOF
  EXPECTED_STDOUT => <<~'EOF'
      Hello, world!
      Image(size_x=640, size_y=480)
      166
      Ball has been plotted to y=3, x=2
      EOF
};

__DATA__
print("Hello, world!")

# Get a reference to the image above
image = get_ball_image()
print(image)

# Pixel [0, 0] has a red value of 166
print(image.at(x=0, y=0).r)

# Draw a cursor onto the image at position [2, 3]
plot_ball(x=2, y=3)
