
import sb3
import sys
import string
import os
import cairosvg

__all__ = ['extract_sb3', 'main']

USAGE = f'''Usage: {sys.argv[0]} SBC_FILES...
'''


def main():
    filenames = sys.argv[1:]
    if not filenames:
        print(USAGE)
        sys.exit(1)

    for filename in filenames:
        extract_sb3(filename)


def replace_delimiters(path):
    path = path.replace('-', '_')
    path = path.replace('.', '_')
    return path


def sanitize_path_fragment(path):
    # characters that will not cause us to write outside of the intended path and
    # that will not cause inconveniences with command line or programmatic access.
    SAFE_CHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.'
    s = ''
    for c in path:
        if c in SAFE_CHARACTERS:
            s += c
    while '..' in s:
        s = s.replace('..', '.')
    return s


def beautify_path_fragment(path):
    path = path.replace(' ', '_')
    return path


def rasterize_png(svg_filename):
    prefix, _ = os.path.splitext(svg_filename)
    output_filename = prefix + '-rasterized.png'
    cairosvg.svg2png(url=svg_filename, write_to=output_filename)
    print(f'  * rasterized {output_filename}')


def extract_sb3(filename):
    print(f'processing {filename}...')
    base_folder, input_file_basename = os.path.split(filename)
    project, assets = sb3.open_sb3(filename)

    targets = project.targets
    sprites = [target for target in targets if isinstance(target, sb3.Sprite)]
    assets_map = {a.name: a for a in assets}

    for sprite in sprites:
        sprite_name = replace_delimiters(sprite.name)
        scripts = sprite.block_info.scripts()
        blocks = sprite.block_info.blocks()
        costumes = sprite.costumes
        sounds = sprite.sounds
        for costume_index, costume in enumerate(costumes):
            costume_name = replace_delimiters(costume.name)
            costume_center = (costume.center_x, costume.center_y)
            costume_filename = costume.filename

            new_filename = f'{sprite_name}-{str(costume_index).zfill(3)}-{costume_name}{os.path.splitext(costume_filename)[1]}'
            new_filename = beautify_path_fragment(new_filename)
            new_filename = sanitize_path_fragment(new_filename)  # important for security
            new_filename = os.path.join(base_folder, new_filename)

            print(f'  * extracted {new_filename}')

            contents = assets_map[costume_filename].read()

            with open(new_filename, 'wb') as output_file:
                output_file.write(contents)

            rasterize_png(new_filename)

        for sound_index, sound in enumerate(sounds):
            sound_name = replace_delimiters(sound.name)
            sound_filename = sound.filename

            new_filename = f'{sprite_name}-{str(sound_index).zfill(3)}-{sound_name}{os.path.splitext(sound_filename)[1]}'
            new_filename = beautify_path_fragment(new_filename)
            new_filename = sanitize_path_fragment(new_filename)  # important for security
            new_filename = os.path.join(base_folder, new_filename)

            print(f'  * extracted {new_filename}')
            
            contents = assets_map[sound_filename].read()

            with open(new_filename, 'wb') as output_file:
                output_file.write(contents)

if __name__ == '__main__':
    main()
