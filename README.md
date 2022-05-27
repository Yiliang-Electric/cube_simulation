# cube_simulation
cube_simulation:

calibratiom.py:
If you're the first time running this code, u need to run calibration.py first for calibration config file creation with camera recently.
And if u change camera, u need run it again.

cube_main.py:
step 1:
Setting the object's quadrilateral corners with "set_original_quadrilateral(corner)".
Corner's order:
corners = [lefttop,leftbottom,rightbottom,righttop]
step 2:
Calling function "show(image,corner)", it will return drawing cube with image data.
