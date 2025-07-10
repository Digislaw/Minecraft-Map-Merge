import os
import yaml
from PIL import Image
import shutil
import re

# 🔧 Configuration
TILE_SIZE = 128
INPUT_DIR = 'tiles'
OUTPUT_DIR = 'output'
YAML_DIR = 'maps'
TILE_PREFIX = 'map'  # Prefix for tile filenames, e.g., map491.png

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def sanitize_filename(name):
    # Replaces forbidden characters in filenames with underscores
    return re.sub(r'[\\/*?:"<>|]', '_', name)

def get_unique_output_path(base_name):
    """
    Returns a unique output path in OUTPUT_DIR, adding _1, _2 etc. if needed.
    """
    safe_base = sanitize_filename(base_name)
    base_path = os.path.join(OUTPUT_DIR, f"{safe_base}.png")
    if not os.path.exists(base_path):
        return base_path

    counter = 1
    while True:
        new_path = os.path.join(OUTPUT_DIR, f"{safe_base}_{counter}.png")
        if not os.path.exists(new_path):
            return new_path
        counter += 1

def compose_image(name, columns, rows, map_ids):
    width = columns * TILE_SIZE
    height = rows * TILE_SIZE
    result = Image.new('RGBA', (width, height))

    for index, map_id in enumerate(map_ids):
        tile_filename = f"{TILE_PREFIX}{map_id}.png"
        tile_path = os.path.join(INPUT_DIR, tile_filename)
        if not os.path.exists(tile_path):
            print(f"❌ Tile not found: {tile_path}")
            continue

        tile = Image.open(tile_path)
        x = (index % columns) * TILE_SIZE
        y = (index // columns) * TILE_SIZE
        result.paste(tile, (x, y))

    output_path = get_unique_output_path(name)
    result.save(output_path)
    print(f"✅ Image created: {output_path}")

def copy_single_tile(name, map_id):
    tile_filename = f"{TILE_PREFIX}{map_id}.png"
    src_path = os.path.join(INPUT_DIR, tile_filename)
    output_path = get_unique_output_path(name)

    if os.path.exists(src_path):
        shutil.copy(src_path, output_path)
        print(f"✅ Single tile copied: {output_path}")
    else:
        print(f"❌ Tile not found: {src_path}")

def process_maps(data):
    maps = data.get("PlayerMapStore", {}).get("mapList", [])
    for entry in maps:
        name = entry.get("name") or entry.get("id") or "Unnamed"

        map_ids = entry.get("mapIDs") or entry.get("mapsIDs")
        if map_ids is not None:
            columns = entry.get("columns", 1)
            rows = entry.get("rows", 1)
            compose_image(name, columns, rows, map_ids)
        elif entry.get("mapID") is not None:
            copy_single_tile(name, entry["mapID"])
        else:
            print(f"⚠️ Missing mapID/mapIDs for: {name}")

def process_all_yaml_files():
    if not os.path.exists(YAML_DIR):
        print(f"❌ YAML folder not found: {YAML_DIR}")
        return

    yaml_files = [f for f in os.listdir(YAML_DIR) if f.lower().endswith('.yml')]
    if not yaml_files:
        print("⚠️ No YAML files found in folder:", YAML_DIR)
        return

    for filename in yaml_files:
        path = os.path.join(YAML_DIR, filename)
        print(f"\n📄 Processing YAML: {filename}")
        try:
            data = load_yaml(path)
            process_maps(data)
        except Exception as e:
            print(f"❌ Failed to process {filename}: {e}")

if __name__ == "__main__":
    process_all_yaml_files()
