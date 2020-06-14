# sb3_extractor

`sb3_extractor` is a tool that extracts sprite information from Scratch SB3 files and dumps well-named image files. In addition to simply dumping `*.svg` files, the files are also be rasterized as `*.png` files too.

If you have some game assets in Scratch that you like and you would like to import them into another platform (i.e., Unity, PyGame, etc.), you may find this tool useful at organizing the files for import.

## Project status

Currently just a beta prototype. This is not a polished tool yet.

This project is built on top of the `sb3` library which is also not stable yet.

### Limitations

* only processes embedded `*.svg` (vector graphics) files currently.
* embedded pixel graphics not handled yet.
* embedded audio files not handled yet.

## Installation

### Requirements

This software requires Python 3.6 or above.

### Current installation procedure

pip3 install git+https://github.com/waterimp/sb3_extractor.git


## Running

### Example

```bash
/path/to/sb3_extractor.py my_scratch_project.sb3
```


## Background and motivation

SB3 files are just a simple zip file containing a `project.json` file and hexadecimal filenames for the asset. Although you can simply use an unzip utility to exract all of the files, they will not be named in a convenient manner.

### Example: unzipping `my_scratch_project.sb3` without sb3_extractor

```bash
$ unzip my_scratch_project.sb3
Archive:  my_scratch_project.sb3
  inflating: project.json            
  inflating: 83a9787d4cb6f3b7632b4ddfebf74367.wav  
  inflating: 83c36d806dc92327b9e7049a565c6bff.wav  
  inflating: cd21514d0531fdffb22204e0ec5ed84a.svg  
  inflating: b7853f557e4426412e64bb3da6531a99.svg  
  inflating: 0f1a9ae400aa0ef452b0a420547a010e.svg  
  inflating: ee299f6bb0802997ad8a7563b5d89af8.svg  
```

### Example: unzipping `my_scratch_project.sb3` WITH sb3_extractor

```bash
$ sb3_extractor/sb3_extractor.py my_scratch_project.sb3
processing my_scratch_project.sb3...
  * extracted Sprite1-000-costume1.svg
  * rasterized Sprite1-000-costume1-rasterized.png
  * extracted Sprite1-001-costume2.svg
  * rasterized Sprite1-001-costume2-rasterized.png
  * extracted Sprite1-002-costume3.svg
  * rasterized Sprite1-002-costume3-rasterized.png
$
$ # Now notice the *.svg files that were exported, with nice names. rasterized *.png files were rendered as well.
$ ls -1
my_scratch_project.sb3
Sprite1-000-costume1-rasterized.png
Sprite1-000-costume1.svg
Sprite1-001-costume2-rasterized.png
Sprite1-001-costume2.svg
Sprite1-002-costume3-rasterized.png
Sprite1-002-costume3.svg
```



## Contributing to sb3_extractor

Please feel free to raise issues and make PR under https://github.com/waterimp/sb3_extractor


## License

GPL3. This was chosen to match the license of the underlying library, `sb3`.
