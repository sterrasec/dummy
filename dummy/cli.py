#!/usr/bin/env python3
# coding: UTF-8

import argparse
import binascii
import colorama
import io
import os
import platform

from colorama import Fore
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import B5

system = platform.system()

def make_csv(file_path, byte_size):
    header = 'Number\n'
    worksheet_function1 = '=3+5\n'
    number = '6\n'
    worksheet_function2 = '=SUM(A2:A3)\n' # 14
    template_length = len(header + worksheet_function1 + number + worksheet_function2)
    with open(file_path, 'w') as f:
        # Write the template
        f.write(header)
        f.write(worksheet_function1)
        f.write(number)
        f.write(worksheet_function2)

        if (byte_size == None) or (template_length > byte_size):
            return True

        for i in range(template_length, byte_size, 2):
            f.write('0\n')
    return True

def make_jpeg(file_path, text):
    image = Image.new('RGB', (729, 516), (255, 255, 255)) # B5, White
    draw = ImageDraw.Draw(image)
    # Pillow's builtin font has a static size, so I used Arial
    # https://github.com/python-pillow/Pillow/issues/2695

    if system == 'Windows':
        font_path = 'C:/Windows/Fonts/arial.ttf'
    else:
        font_path = 'Arial.ttf'
    arial = ImageFont.truetype(font_path, 30)
    draw.text((10, 10), text, fill=(0, 0, 0), font=arial) # Black
    image.save(file_path, format='jpeg')
    return True

def make_png(file_path, text, byte_size):
    image = Image.new('RGB', (729, 516), (255, 255, 255)) # B5, White
    draw = ImageDraw.Draw(image)
    # Pillow's builtin font has a static size, so I used Arial
    # https://github.com/python-pillow/Pillow/issues/2695

    system = platform.system()
    if system == 'Windows':
        font_path = 'C:/Windows/Fonts/arial.ttf'
    else:
        font_path = 'Arial.ttf'
    arial = ImageFont.truetype(font_path, 30)
    draw.text((10, 10), text, fill=(0, 0, 0), font=arial) # Black
    output = io.BytesIO()
    image.save(output, format='png')
    png_data = output.getvalue()

    if (byte_size == None) or (len(png_data) > byte_size):
        with open(file_path, 'wb') as f:
            f.write(png_data)
        return True

    # IEND chunk is the last chunk of a PNG file
    iend_type_index = png_data.find(b'IEND')
    if iend_type_index == -1:
        print(Fore.RED + 'Error: IEND chunk not found.')
        return False

    # The first 4 bytes of the IEND chunk are data length
    # IEND chunk type (4 bytes) follows IEND chunk data length (4 bytes)
    iend_chunk_index = iend_type_index - 4

    # 12 = 4 (chunk length) + 4 (chunk type) + 4 (chunk CRC)
    extra_chunk_length = byte_size - len(png_data) - 12
    # private chunk type 
    extra_chunk_type = b'eXtr'
    extra_chunk_data = b'\x00' * extra_chunk_length
    extra_chunk_crc = binascii.crc32(extra_chunk_type + extra_chunk_data)
    extra_chunk = extra_chunk_length.to_bytes(4, byteorder='big')
    extra_chunk += (extra_chunk_type + extra_chunk_data)
    extra_chunk += extra_chunk_crc.to_bytes(4, byteorder='big')

    added_png_data = png_data[:iend_chunk_index] + extra_chunk + png_data[iend_chunk_index:]
    with open(file_path, 'wb') as f:
        f.write(added_png_data)
    return True

def make_pdf(file_path, text):
    c = canvas.Canvas(file_path, bottomup=False, pagesize=B5)
    c.setFont('Helvetica', 30)
    c.drawString(15, 40, text)
    c.showPage()
    c.save()
    return True

def parse_bytes(byte_str):
    if byte_str == None:
        return None

    if byte_str.endswith(('KB', 'Kb', 'kB', 'kb')):
        return int(byte_str[:-2]) * 1024
    elif byte_str.endswith(('MB', 'Mb', 'mB', 'mb')):
        return int(byte_str[:-2]) * 1024 * 1024
    elif byte_str.endswith(('GB', 'Gb', 'gB', 'gb')):
        return int(byte_str[:-2]) * 1024 * 1024 * 1024
    elif byte_str.endswith(('B', 'b')):
        return int(byte_str[:-1])
    else:
        try:
            return int(byte_str)
        except ValueError:
            print(Fore.RED + 'Error: Invalid byte size.')
            return None

def parse_args():
    colorama.init(autoreset=True)
    parser = argparse.ArgumentParser(description='Create a dummy file for testing.')
    parser.add_argument('file_path', help='Path to the generated file(.csv .jpeg, .png, .pdf)')
    parser.add_argument('-t', '--text', help='Text to be written in the file(Disabled in csv)', default='dummy file')
    parser.add_argument('-b', '--bytes', help='Bytes of file(.png, .csv)')

    args = parser.parse_args()
    if args.bytes is not None and not args.file_path.endswith('.png') and not args.file_path.endswith('.csv'):
        print(Fore.RED + 'Error: -b option is only available for .png or .csv files.')
        return
    
    # If the directory specified in path does not exist
    if args.file_path.rfind('/') != -1:
        dir_path = args.file_path[:args.file_path.rfind('/')]
        if not os.path.exists(dir_path):
            print(Fore.RED + 'Error: The specified directory does not exist.')
            return
    
    if args.file_path.endswith('.csv'):
        make_csv(args.file_path, parse_bytes(args.bytes))
        print(Fore.GREEN + 'Successfully generated: ' + args.file_path)

    elif args.file_path.endswith('.jpeg') or args.file_path.endswith('.jpg'):
        make_jpeg(args.file_path, args.text)
        print(Fore.GREEN + 'Successfully generated: ' + args.file_path)

    elif args.file_path.endswith('.png'):
        if make_png(args.file_path, args.text, parse_bytes(args.bytes)):
            print(Fore.GREEN + 'Successfully generated: ' + args.file_path)
        else:
            print(Fore.RED + 'Failed to generate file...')

    elif args.file_path.endswith('.pdf'):
        make_pdf(args.file_path, args.text)
        print(Fore.GREEN + 'Successfully generated: ' + args.file_path)

    else:
        print(Fore.RED + 'Error: Invalid file extension.')
