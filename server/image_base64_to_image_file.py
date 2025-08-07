from binascii import a2b_base64
import urllib.request
from datetime import datetime
from werkzeug.utils import secure_filename

def image_base64_to_image_file(base64, extension):

    print('\n\nImage Base64 received:\n',str(base64),'\n\n')
    print('Image extension:',str(extension),'\n\n')

    # construct image file name
    image_filename = str(datetime.now()).replace('-', '')
    image_filename = image_filename.replace(':', '')
    image_filename = image_filename.replace('.', '')
    image_filename = image_filename.replace(' ', '-')
    image_filename = secure_filename(image_filename + '.' + extension)

    # get image binary data
    image_binary_data = a2b_base64(base64)

    # read response and save image file
    with open(image_filename, 'wb') as f:
        f.write(image_binary_data)
        f.close()

    return image_filename