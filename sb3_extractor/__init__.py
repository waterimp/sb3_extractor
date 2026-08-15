
import sb3
import sys
import string
import os
import cairosvg
import xml.etree.ElementTree as ET

__all__ = ['extract_sb3', 'main']

USAGE = f'''Usage: {sys.argv[0]} SBC_FILES...
'''

DEFAULT_MAX_WIDTH = 480
DEFAULT_MAX_HEIGHT = 360

SVG_DRAWABLE_TAGS = {'path', 'rect', 'circle', 'ellipse', 'polygon', 'polyline', 'image', 'line', 'text'}
LENGTH_UNIT_SUFFIXES = ('px', 'pt', 'pc', 'mm', 'cm', 'in', 'em', 'rem')


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


def fit_within_bounds(width, height, max_width, max_height):
    scale = min(max_width / width, max_height / height)
    return max(1, round(width * scale)), max(1, round(height * scale))


def _local_tag(element):
    tag = element.tag
    return tag.split('}', 1)[1] if '}' in tag else tag


def _parse_length(value):
    if value is None:
        return None
    value = value.strip()
    for suffix in LENGTH_UNIT_SUFFIXES:
        if value.endswith(suffix):
            value = value[:-len(suffix)]
            break
    try:
        length = float(value)
    except ValueError:
        return None
    return length if length > 0 else None


def parse_svg_root(svg_filename):
    try:
        return ET.parse(svg_filename).getroot()
    except ET.ParseError:
        return None


def svg_intrinsic_size(root):
    """The size the SVG itself declares it spans, straight from its own
    width/height (or, failing that, viewBox) attributes -- independent
    of whether cairosvg thinks that's usable for sizing a canvas.
    """
    width = _parse_length(root.get('width'))
    height = _parse_length(root.get('height'))
    if width and height:
        return width, height

    view_box = root.get('viewBox')
    if view_box:
        parts = view_box.replace(',', ' ').split()
        if len(parts) == 4:
            vb_width = _parse_length(parts[2])
            vb_height = _parse_length(parts[3])
            if vb_width and vb_height:
                return vb_width, vb_height

    return None, None


def svg_has_visible_content(root):
    for element in root.iter():
        tag = _local_tag(element)
        if tag not in SVG_DRAWABLE_TAGS:
            continue
        if tag == 'path':
            if element.get('d', '').strip():
                return True
        elif tag == 'text':
            if (element.text or '').strip():
                return True
        else:
            sizes = (element.get('width'), element.get('height'), element.get('r'))
            if any(_parse_length(v) is None and v is not None for v in sizes):
                continue  # a declared-but-zero size means nothing is drawn
            return True
    return False


def explain_rasterize_error(e):
    msg = str(e)
    if 'size is undefined' in msg:
        return f'SVG has no width/height/viewBox to size the image ({msg})'
    if 'no element found' in msg:
        return f'SVG is empty or corrupt, no XML content ({msg})'
    return msg


def rasterize_png(svg_filename, center_x=0, center_y=0):
    prefix, _ = os.path.splitext(svg_filename)
    output_filename = prefix + '-rasterized.png'
    try:
        cairosvg.svg2png(url=svg_filename, write_to=output_filename)
    except ValueError as e:
        if str(e) != 'The SVG size is undefined':
            print(f'  ! could not rasterize {os.path.basename(svg_filename)}: '
                  f'{explain_rasterize_error(e)}')
            return

        root = parse_svg_root(svg_filename)
        if root is None:
            print(f'  ! could not rasterize {os.path.basename(svg_filename)}: '
                  f'{explain_rasterize_error(e)}')
            return

        if not svg_has_visible_content(root):
            # nothing to draw either way -- a 1x1 transparent pixel says so
            # without paying for a full blank 480x360 canvas.
            cairosvg.svg2png(url=svg_filename, write_to=output_filename,
                              output_width=1, output_height=1)
            print(f'  * rasterized {output_filename} as a 1x1 transparent pixel '
                  f'(SVG has no visible content)')
            return

        # the SVG has real content but cairosvg can't size the canvas from
        # its own width/height/viewBox. Prefer the SVG's own declared
        # dimensions (even sub-pixel ones) to derive an aspect ratio; if it
        # truly declares none, fall back to the costume's rotation center as
        # a rough stand-in; if neither is available, use the stage box as-is.
        intrinsic_width, intrinsic_height = svg_intrinsic_size(root)
        if intrinsic_width and intrinsic_height:
            output_width, output_height = fit_within_bounds(
                intrinsic_width, intrinsic_height, DEFAULT_MAX_WIDTH, DEFAULT_MAX_HEIGHT)
        elif center_x > 0 and center_y > 0:
            output_width, output_height = fit_within_bounds(
                center_x * 2, center_y * 2, DEFAULT_MAX_WIDTH, DEFAULT_MAX_HEIGHT)
        else:
            output_width, output_height = DEFAULT_MAX_WIDTH, DEFAULT_MAX_HEIGHT

        try:
            cairosvg.svg2png(url=svg_filename, write_to=output_filename,
                              output_width=output_width, output_height=output_height)
        except Exception as e2:
            print(f'  ! could not rasterize {os.path.basename(svg_filename)}: '
                  f'{explain_rasterize_error(e2)}')
            return

        print(f'  * rasterized {output_filename} at fallback size '
              f'{output_width}x{output_height} ({explain_rasterize_error(e)})')
        return
    except Exception as e:
        # not a missing-size problem (e.g. the SVG has no XML content at
        # all) -- a sized retry wouldn't help, so don't attempt one.
        print(f'  ! could not rasterize {os.path.basename(svg_filename)}: '
              f'{explain_rasterize_error(e)}')
        return

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
        costumes = sprite.costumes
        sounds = sprite.sounds
        for costume_index, costume in enumerate(costumes):
            costume_name = replace_delimiters(costume.name)
            costume_filename = costume.filename
            costume_extension = os.path.splitext(costume_filename)[1]

            new_filename = f'{sprite_name}-{str(costume_index).zfill(3)}-{costume_name}{costume_extension}'
            new_filename = beautify_path_fragment(new_filename)
            new_filename = sanitize_path_fragment(new_filename)  # important for security
            new_filename = os.path.join(base_folder, new_filename)

            print(f'  * extracted {new_filename}')

            contents = assets_map[costume_filename].read()

            with open(new_filename, 'wb') as output_file:
                output_file.write(contents)

            if costume_extension.lower() == '.svg':
                rasterize_png(new_filename, costume.center_x, costume.center_y)

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
