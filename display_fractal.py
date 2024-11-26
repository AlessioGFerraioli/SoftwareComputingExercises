from PIL import Image as imreader
from plumbum.cli.image import Image as imdisplay
im = imreader.open("fractal_wrongness.jpg")
# does not work with jupyter
imdisplay().show_pil(im)