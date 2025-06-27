# Smart Sprite Splitter

**Smart Sprite Splitter** is a Python tool for automatically or manually splitting sprite sheet images into multiple small image files, with automatic sprite count detection.

## Features

- **Auto-detect sprite count** for each image (based on transparency, color changes, or fallback aspect ratio).
- **Manual input** for sprite count per file for more accuracy.
- **Batch processing** with multi-threading (fast for multiple files).
- **Per-file configuration** (edit sprite count in JSON file).
- **Flexible input/output folders** (specify any folder path, doesn't need to be inside project folder).

## Usage

### 1. Install Dependencies

Make sure Python 3 is installed.  
Install required libraries:

```bash
pip install pillow numpy
```

### 2. Run the Program

```bash
python SmartSprite.py
```

### 3. Choose Mode

When running, select the mode according to your needs:

1. **Auto-detect sprite count (fast)**  
   Automatically detect sprite count for each image.

2. **Manual input per file (accurate)**  
   Manually input sprite count for each file.

3. **Load from config file**  
   Use sprite count configuration from existing JSON file.

4. **Create config file only**  
   Only create sprite count configuration file (without splitting images).

### 4. Input Folders

- When prompted for "Input folder" and "Output folder", **enter the folder path you want**.
- Paths can be absolute (e.g., `D:\Game Assets\input_sprites`) or relative (`input`).
- No need to create special folders inside the project, the program will automatically create folders if they don't exist.

**Example:**
```
Input folder: D:\Game Assets\input_sprites
Output folder: D:\Game Assets\output_sprites
```

### 5. Results

- Split image results will be saved in the output folder you specified.
- Configuration file (JSON) will be saved in the input folder or according to the path you choose.

## Notes

- To edit sprite count per image, edit the generated JSON configuration file.
- For folders with spaces, simply copy-paste the path from Windows Explorer (no quotes needed).
- Windows shortcuts (.lnk) are not supported, use the actual folder path.

## License

MIT License

---

**By:** [MohNahrowiSetiawan](https://github.com/Mohnahrowisetiawan217)