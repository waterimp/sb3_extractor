# sb3_extractor

`sb3_extractor` is a tool that extracts sprite information from Scratch SB3 files and dumps well-named image files. In addition to simply dumping `*.svg` files, the files are also rasterized as `*.png` files too.

If you have some game assets in Scratch that you like and you would like to import them into another platform (i.e., PyGame, Godot, Unity, GameMaker, RPGMaker, etc.), you may find this tool useful at organizing the files before the import.


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

```bash
pip3 install git+https://github.com/waterimp/sb3_extractor.git
```


## Running

### Example

```bash
/path/to/sb3_extractor.py my_scratch_project.sb3
```


## Background and motivation

SB3 files are just a simple zip file containing a `project.json` file and hexadecimal filenames for the asset.
Although you can simply use an unzip utility to extract all of the files, they will not be named in a convenient manner.

Let's say you have a project named "my_scratch_project" on Scratch.
You can export your Scratch project to your computer by clicking on `File -> Save to your computer`.
Your browser will then download a file called `my_scratch_project.sb3`.
Once downloaded, there are some different ways we can extract the assets from the files.
Below you can find two different ways to extract the files: normal zip extration tools and `sb3_extractor`.

### Example: unzipping `my_scratch_project.sb3` without sb3_extractor


```bash
$ # Note: unzip is a utility on Linux and Mac. For Windows, you can just right-click on the file to unzip or use the "Expand-Archive" powershell command.
$ unzip my_scratch_project.sb3
Archive:  my_scratch_project.sb3
  inflating: project.json            
  inflating: 83a9787d4cb6f3b7632b4ddfebf74367.wav  
  inflating: 83c36d806dc92327b9e7049a565c6bff.wav  
  inflating: cd21514d0531fdffb22204e0ec5ed84a.svg  
  inflating: b7853f557e4426412e64bb3da6531a99.svg  
  inflating: 0f1a9ae400aa0ef452b0a420547a010e.svg  
```

If all you need is the files, then the sb3_extractor tool may not be needed.
However, you may prefer more meaningful filenames and may benefit from the additional converted files. Let's have a look at how sb3_extractor handles the same file.

### Example: unzipping `my_scratch_project.sb3` WITH sb3_extractor

Let's invoke `sb3_extractor` and see what happens...

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

You may find these exported filenames more meaningful and conveniently organized for an import into another game platform.

Also, notice the rasterized images that were generated (`*.png` files from `*.svg`). These `*.png` files may be useful if you need pixel graphics for your new endeavor. If not, the `*.svg` files are available for infinite resolution.

Please note at this time that the `*.wav` files are not extracted.

## Contributing to sb3_extractor

Please feel free to raise issues and make PR under https://github.com/waterimp/sb3_extractor


## License

GPL3. This was chosen to match the license of the underlying library, `sb3`.
