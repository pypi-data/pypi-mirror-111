from . import convert_items
from pathlib import Path


for xml in Path().glob('data/*.xml'):
    print(f'Processing: {xml}')
    convert_items(xml)
