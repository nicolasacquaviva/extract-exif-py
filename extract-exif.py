import exifread
import os.path
import sys

def exif_to_string(exif_data):
    string = ''

    for key, value in exif_data.items():
        string += str(key) + ': ' + str(value) + '\n'

    return string

def exit_with_error(e):
    print('Usage: extract-exif "directory or file"')
    sys.exit(1)

def get_exif_from_image(file_path):
    try:
        # Open image file for reading (must be in binary mode)
        file = open(file_path, 'rb')
        return exifread.process_file(file)
    except Exception as e:
        print('Error get_exif_from_image', e)

def is_image(file_name):
    extensions = ['jpg', 'jpeg', 'png', 'tiff']

    if file_name.split('.')[1] in extensions:
        return True
    else:
        return False

def write_exif_to_file(target_file):
    file_exif = exif_to_string(get_exif_from_image(target_file))
    write_file(str(file_exif), target_file + '__exif__.txt')

def write_file(data, file_name):
    try:
        file = open(file_name, 'a')

        file.write(data)
        file.close()
    except Exception as e:
        print('Error write_file', e)

def main():
    if len(sys.argv) < 2:
        exit_with_error()

    target = sys.argv[1]

    if os.path.isfile(target):
        write_exif_to_file(target)
    elif os.path.isdir(target):
        for file_name in os.listdir(target):
            if (is_image(file_name)):
                write_exif_to_file(target + file_name)
    else:
        exit_with_error()

main()
