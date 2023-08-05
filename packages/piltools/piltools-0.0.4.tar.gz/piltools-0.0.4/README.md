# PILTools
## Python Imaging Library Tools

Pillow is "[the friendly PIL fork by Alex Clark and Contributors](https://pillow.readthedocs.io/en/stable/)".

This tool suite is meant to augment the existing Python Imaging Library with the following tools:
- Recrop: A dynamic image resizer. Given a target (width, height) dimension, resize the image, then crop with respect to a focus area.
- (More tools to come)

# Install
```sh
pip install piltools
```

# Example A(spect) R(atio) Resize
```
from PIL import Image
from piltools.transform import ar_resize

im = Image.open("./cosmos.jpg")

# Double image in size
ar_resize(im, 2).show()
```

# Example ReCrop
```
from PIL import Image
from piltools.transform import recrop

im = Image.open("./cosmos.jpg")

# Create an ad Banner using top center portion of image
recrop(im, (468, 60), v_align="top", h_align="center").show()
```
