import os
from django.conf import settings

MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'media')
MEDIA_URL = 'media/'
IMAGE_TAIL = ('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')
DEFAULT_AVATAR = "default.png"
AVATARS_URL = settings.MEDIA_URL + "avatars/"
