#! /usr/bin/env python3

import sb3
import sys
import string
import os
import cairosvg

# def main():
filename = sys.argv[1]
print(filename)
base_folder, input_file_basename = os.path.split(filename)
project, assets = sb3.open_sb3(filename)

targets = project.targets
sprites = [target for target in targets if isinstance(target, sb3.Sprite)]
assets_map = {a.name: a for a in assets}

def replace_delimiters(path):
    path = path.replace('-', '_')
    path = path.replace('.', '_')
    return path

def sanitize_path_fragment(path):
    s = ''
    for c in path:
        # only include whitelisted characters. throw away all others.
        if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.':
            s += c
    return s

def beautify_path_fragment(path):
    path = path.replace(' ', '_')
    return path

def rasterize_png(svg_filename):
    prefix, _ = os.path.splitext(svg_filename)
    output_filename = prefix + '-rasterized.png'
    cairosvg.svg2png(url=svg_filename, write_to=output_filename)



for sprite in sprites:
    sprite_name = replace_delimiters(sprite.name)
    #print(sprite.__dict__)
    scripts = sprite.block_info.scripts()
    blocks = sprite.block_info.blocks()
    costumes = sprite.costumes
    for costume_index, costume in enumerate(costumes):
        # print(costume.__dict__)
        costume_name = replace_delimiters(costume.name)
        costume_center = (costume.center_x, costume.center_y)
        costume_filename = costume.filename

        #new_filename = f'{sprite_name}-{str(costume_index).zfill(3)}-{costume_name}-{costume_filename}'
        new_filename = f'{sprite_name}-{str(costume_index).zfill(3)}-{costume_name}{os.path.splitext(costume_filename)[1]}'
        new_filename = beautify_path_fragment(new_filename)
        new_filename = sanitize_path_fragment(new_filename)  # important for security
        new_filename = os.path.join(base_folder, new_filename)

        print(new_filename, costume_center)

        contents = assets_map[costume_filename].read()

        with open(new_filename, 'wb') as output_file:
            output_file.write(contents)

        rasterize_png(new_filename)

for asset in assets:
    name = asset.name
    contents = asset.read()



# if __name__ == '__main__':
#     main()
