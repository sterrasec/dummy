#!/usr/bin/env python3
# coding: UTF-8

import argparse
import binascii
import colorama
import io

from colorama import Fore
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import B5


def make_jpeg(file_path, text):
    image = Image.new('RGB', (729, 516), (255, 255, 255)) # B5, White
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), text, fill=(0, 0, 0)) # Black
    image.save(file_path, format='jpeg')

def make_png(file_path, text, byte_size):
    image = Image.new('RGB', (729, 516), (255, 255, 255)) # B5, White
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), text, fill=(0, 0, 0)) # Black
    output = io.BytesIO()
    image.save(output, format='png')
    png_data = output.getvalue()

    if (byte_size == None) or (len(png_data) > byte_size):
        with open(file_path, 'wb') as f:
            f.write(png_data)
        return False

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

def parse_bytes(byte_str):
    if byte_str == None:
        return None

    if byte_str.endswith(('B', 'b')):
        return int(byte_str[:-1])
    elif byte_str.endswith(('KB', 'Kb', 'kB', 'kb')):
        return int(byte_str[:-2]) * 1024
    elif byte_str.endswith(('MB', 'Mb', 'mB', 'mb')):
        return int(byte_str[:-2]) * 1024 * 1024
    elif byte_str.endswith(('GB', 'Gb', 'gB', 'gb')):
        return int(byte_str[:-2]) * 1024 * 1024 * 1024
    else:
        try:
            return int(byte_str)
        except ValueError:
            print(Fore.RED + 'Error: Invalid byte size.')
            return None

def parse_args():
    colorama.init(autoreset=True)
    parser = argparse.ArgumentParser(description='Create a dummy file for testing.')
    parser.add_argument('file_path', help='Path to the generated file(.jpeg, .png, .pdf)')
    parser.add_argument('-t', '--text', help='Text to be written in the file', default='dummy file')
    parser.add_argument('-b', '--bytes', help='Bytes of file(.png only)')

    args = parser.parse_args()
    if args.file_path.endswith('.jpeg') or args.file_path.endswith('.jpg'):
        make_jpeg(args.file_path, args.text)
    elif args.file_path.endswith('.png'):
        make_png(args.file_path, args.text, parse_bytes(args.bytes))
    elif args.file_path.endswith('.pdf'):
        make_pdf(args.file_path, args.text)
    else:
        print(Fore.RED + 'Error: Invalid file extension.')

