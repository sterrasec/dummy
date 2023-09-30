#!/usr/bin/env python3
# coding: UTF-8

import argparse
import binascii
import colorama
import pypdf
import io

from colorama import Fore, Back, Style
from PIL import Image, ImageDraw, ImageFont

def make_png_data(text, byte_size):
    image = Image.new('RGB', (516, 729), (255, 255, 255)) # B5, White
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), text, fill=(0, 0, 0)) # Black
    output = io.BytesIO()
    image.save(output, format='png')
    png_data = output.getvalue()

    if len(png_data) > byte_size:
        with open('dummy.png', 'wb') as f:
            f.write(png_data)
        return None

    # IEND chunk is the last chunk of a PNG file
    iend_type_index = png_data.find(b'IEND')
    if iend_type_index == -1:
        print(Fore.RED + 'Error: IEND chunk not found.')
        return None

    # The first 4 bytes of the IEND chunk are data length
    # IEND chunk type (4 bytes) follows IEND chunk data length (4 bytes)
    iend_chunk_index = iend_type_index - 4

    # 12 = 4 (chunk length) + 4 (chunk type) + 4 (chunk CRC)
    extra_chunk_length = byte_size - len(png_data) - 12
    # private chunk type 
    extra_chunk_type = b'exTr'
    extra_chunk_data = b'\x00' * extra_chunk_length
    extra_chunk_crc = binascii.crc32(extra_chunk_type + extra_chunk_data)
    extra_chunk = extra_chunk_length.to_bytes(4, byteorder='big')
    extra_chunk += (extra_chunk_type + extra_chunk_data)
    extra_chunk += extra_chunk_crc.to_bytes(4, byteorder='big')

    added_png_data = png_data[:iend_chunk_index] + extra_chunk + png_data[iend_chunk_index:]
    return added_png_data

def parse_args():
    colorama.init(autoreset=True)
    parser = argparse.ArgumentParser(description='Create a dummy file of the specified size.')
    parser.add_argument('-type', '--type', help='File type', choices=['png', 'pdf', 'txt'], required=True)
    parser.add_argument('-text', '--text', help='Text to be written in the file')
    parser.add_argument('-size', '--size', help='File size (bytes)', type=int)
    args = parser.parse_args()
    if args.type == 'png':
        added_png_data = make_png_data(args.text, args.size)
        with open('dummy.png', 'wb') as f:
            f.write(added_png_data)
    else:
        print(Fore.RED + 'Error: Invalid file type.')
        parser.print_help()

if __name__ == '__main__':
    colorama.init(autoreset=True)
    png_data = make_png_data('sample png', 400001)
    with open('dummy.png', 'wb') as f:
        f.write(png_data)
