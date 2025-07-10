# Minecraft Map Merge

A Python script to combine multiple PNG map tiles (128x128 px) into larger images based on YAML configuration files from ImageOnMap plugin. It supports both multi-tile posters and single tile images.

---

## Features

- Reads one or more `.yml` configuration files from a `maps/` directory
- Supports tiled images with rows and columns layout, stitching tiles accordingly
- Supports single tile images (copies with renamed output)
- Automatically resolves filename conflicts by appending incremental suffixes (`_1`, `_2`, etc.)
- Sanitizes output filenames to avoid invalid characters
- Uses PNG tiles with a configurable prefix (`map`) in the `tiles/` folder
- Outputs combined images to an `output/` folder
- Prints clear success and warning messages during processing

---

## Requirements

- Python 3.6+
- [Pillow](https://python-pillow.org/) (for image processing)
- PyYAML (for reading YAML files)

Install dependencies with:

```bash
pip install pillow pyyaml
```
## Folder structure
```
project/
├── compose_maps.py        # Main Python script
├── tiles/                 # Input folder with tile PNG images (e.g., map491.png)
├── maps/                  # Folder containing YAML config files (e.g., 0ef8e9ee-4143-4f50-97cc-ed9f0b7f7139.yml)
└── output/                # Output folder where composed images will be saved (auto-created)
```

## Usage
Place your tiles (named like map463.png) inside the tiles/ directory.
Place your .yml map definitions inside the maps/ directory.
Run the script:
```
python compose_maps.py
```
The script will:
- Process all .yml files in the maps/ folder
- Compose images based on the definitions inside each YAML file
- Save the results into the output/ folder with safe and unique filenames
