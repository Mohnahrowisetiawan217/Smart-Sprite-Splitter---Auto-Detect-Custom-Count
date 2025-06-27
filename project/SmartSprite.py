from PIL import Image
import os
import glob
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import numpy as np

def auto_detect_sprites(img_path, method="transparency"):
    """
    Auto-detect the number of sprites in an image.

    Args:
        img_path: path to the image
        method: "transparency", "color_change", "edge_detect"

    Returns:
        int: detected number of sprites
    """
    try:
        with Image.open(img_path) as img:
            # Convert to RGBA for transparency detection
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            width, height = img.size
            img_array = np.array(img)
            
            if method == "transparency":
                alpha_channel = img_array[:, :, 3]
                
                transparent_cols = []
                for x in range(width):
                    if np.all(alpha_channel[:, x] == 0):
                        transparent_cols.append(x)
                
                if transparent_cols:
                    gaps = []
                    for i in range(1, len(transparent_cols)):
                        gap = transparent_cols[i] - transparent_cols[i-1]
                        if gap > 10:
                            gaps.append(gap)
                    
                    if gaps:
                        sprite_width = max(set(gaps), key=gaps.count)
                        sprite_count = width // sprite_width
                        return max(1, sprite_count)
            
            elif method == "color_change":
                rgb_array = img_array[:, :, :3]
                
                col_colors = np.mean(rgb_array, axis=0)
                
                changes = []
                threshold = 30 
                
                for x in range(1, width):
                    color_diff = np.linalg.norm(col_colors[x] - col_colors[x-1])
                    if color_diff > threshold:
                        changes.append(x)
                
                if len(changes) > 1:
                    avg_sprite_width = width // (len(changes) + 1)
                    return max(1, width // avg_sprite_width)
            
            if width > height:
                estimated_sprite_width = height
                return max(1, width // estimated_sprite_width)
            else:
                return 1
                
    except Exception as e:
        print(f"   ⚠️  Auto-detect failed for {os.path.basename(img_path)}: {e}")
        return 8

def create_sprite_config(input_dir, output_file="sprite_config.json"):
    """
    Create a configuration file to map the number of sprites per file.
    """
    
    if not os.path.exists(input_dir):
        print(f"❌ Input folder '{input_dir}' not found!")
        return {}

    print("🔧 CREATING SPRITE CONFIGURATION")
    print("=" * 50)
    
    # Find images
    all_files = []
    for ext in ["*.png", "*.jpg", "*.jpeg", "*.bmp"]:
        all_files.extend(glob.glob(os.path.join(input_dir, "**", ext), recursive=True))
    
    config = {}
    
    print(f"📁 Analyzing {len(all_files)} files...")
    
    for i, file_path in enumerate(all_files, 1):
        filename = os.path.relpath(file_path, input_dir)
        
        # Auto-detect sprite count
        detected_count = auto_detect_sprites(file_path)
        
        config[filename] = {
            "sprite_count": detected_count,
            "auto_detected": True,
            "file_size": os.path.getsize(file_path)
        }
        
        print(f"[{i:3d}/{len(all_files)}] {filename} -> {detected_count} sprites")
    
    if not os.path.isabs(output_file):
        output_file = os.path.join(input_dir, output_file)
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Configuration saved to '{output_file}'")
    print("📝 Edit this file to adjust the sprite count per image")
    return config

def load_sprite_config(config_file="sprite_config.json"):
    """Load sprite configuration from a JSON file"""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Config file '{config_file}' not found!")
        return {}

def split_single_sprite_smart(file_info):
    """
    Split sprites with the specified count per file.
    """
    file_path, output_base_dir, sprite_config, input_base_dir = file_info
    
    try:
        rel_path = os.path.relpath(file_path, input_base_dir)
        
        sprite_count = 8  # default
        if rel_path in sprite_config:
            sprite_count = sprite_config[rel_path]["sprite_count"]
        else:
            sprite_count = auto_detect_sprites(file_path)
        
        if sprite_count <= 1:
            return (True, file_path, f"⏭️  Skip (only {sprite_count} sprite)")
        
        # Make output folder
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        rel_dir = os.path.dirname(rel_path)
        
        if rel_dir:
            output_dir = os.path.join(output_base_dir, rel_dir, file_name)
        else:
            output_dir = os.path.join(output_base_dir, file_name)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Process sprites
        with Image.open(file_path) as img:
            width, height = img.size
            sprite_width = width // sprite_count
            
            # Split sprites
            for i in range(sprite_count):
                left = i * sprite_width
                right = min(left + sprite_width, width)  # Prevent overflow
                
                sprite = img.crop((left, 0, right, height))
                output_path = os.path.join(output_dir, f"sprite_{i+1:02d}.png")
                sprite.save(output_path)
        
        return (True, file_path, f"✓ {sprite_count} sprites")
        
    except Exception as e:
        return (False, file_path, f"✗ Error: {str(e)}")

def batch_split_smart(input_dir="input", output_dir="output", 
                     config_file="sprite_config.json", max_workers=4):
    """
    Batch split with per-file configuration
    """
    print("🚀 SMART SPRITE SPLITTER")
    print("=" * 50)

    # Check input folder
    if not os.path.exists(input_dir):
        print(f"❌ Input folder '{input_dir}' not found. Creating folder...")
        os.makedirs(input_dir)
        print(f"📁 Folder '{input_dir}' has been created. Please put images in this folder and rerun.")
        return

    # Check output folder
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load config
    sprite_config = load_sprite_config(config_file)
    
    if not sprite_config:
        print("⚠️  Creating automatic configuration...")
        sprite_config = create_sprite_config(input_dir, config_file)
    
    # Find files
    all_files = []
    for ext in ["*.png", "*.jpg", "*.jpeg", "*.bmp"]:
        all_files.extend(glob.glob(os.path.join(input_dir, "**", ext), recursive=True))
    
    total_files = len(all_files)
    
    if total_files == 0:
        print(f"❌ No image files found in '{input_dir}'")
        return
    
    print(f"📁 Processing {total_files} files with custom configuration")
    print(f"🔧 Using {max_workers} threads")
    print("-" * 50)
    
    # Make output folder
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Prepare tasks
    file_tasks = [(file_path, output_dir, sprite_config, input_dir) 
                  for file_path in all_files]
    
    # Progress tracking
    completed = 0
    successful = 0
    failed = 0
    total_sprites = 0
    start_time = time.time()
    
    # Process threading
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(split_single_sprite_smart, task): task[0] 
                         for task in file_tasks}
        
        for future in as_completed(future_to_file):
            file_path = future_to_file[future]
            success, processed_file, message = future.result()
            
            completed += 1
            
            if success:
                successful += 1
                # Extract sprite count from message
                if "sprites" in message and "✓" in message:
                    try:
                        count = int(message.split()[1])
                        total_sprites += count
                    except:
                        pass
            else:
                failed += 1
            
            rel_path = os.path.relpath(processed_file, input_dir)
            print(f"[{completed:3d}/{total_files}] {rel_path} {message}")
            
            # Progress update
            if completed % 50 == 0:
                elapsed = time.time() - start_time
                rate = completed / elapsed
                eta = (total_files - completed) / rate if rate > 0 else 0
                print(f"   📊 Progress: {completed}/{total_files} | Rate: {rate:.1f}/sec | ETA: {eta:.0f}s")
    
    # Summary
    elapsed = time.time() - start_time
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print(f"✅ Success: {successful} files")
    print(f"❌ Failed: {failed} files")
    print(f"🖼️  Total sprites: {total_sprites}")
    print(f"⏱️  Time: {elapsed:.1f} seconds")
    print("=" * 50)

def manual_config_mode():
    """Mode for manual input of sprite count per file"""
    print("📝 MANUAL CONFIGURATION MODE")
    print("Input the number of sprites for each file")
    print("=" * 50)
    
    input_dir = input("Input folder: ").strip() or "input"
    
    # Find all files
    all_files = []
    for ext in ["*.png", "*.jpg", "*.jpeg", "*.bmp"]:
        all_files.extend(glob.glob(os.path.join(input_dir, "**", ext), recursive=True))
    
    if not all_files:
        print(f"❌ No image files found in '{input_dir}'")
        return
    
    config = {}
    
    print(f"\n📁 Found {len(all_files)} files")
    print("Enter the number of sprites for each file (Enter = auto-detect):")
    print("-" * 50)
    
    for file_path in all_files:
        filename = os.path.relpath(file_path, input_dir)
        
        # Auto-detect as suggestion
        suggested = auto_detect_sprites(file_path)
        
        while True:
            try:
                user_input = input(f"{filename} [suggested: {suggested}]: ").strip()
                
                if user_input == "":
                    sprite_count = suggested
                    break
                else:
                    sprite_count = int(user_input)
                    if sprite_count >= 0:
                        break
                    else:
                        print("   ❌ Count must be >= 0")
                        
            except ValueError:
                print("   ❌ Input must be a number")
        
        config[filename] = {
            "sprite_count": sprite_count,
            "auto_detected": user_input == "",
            "file_size": os.path.getsize(file_path)
        }
    
    config_file = os.path.join(input_dir, "manual_sprite_config.json")
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Configuration saved to '{config_file}'")
    
    # Ask if want to process immediately
    if input("\nProcess now? (y/n): ").strip().lower() == 'y':
        output_dir = input("Output folder: ").strip() or "output"
        batch_split_smart(input_dir, output_dir, config_file)

# Main program
if __name__ == "__main__":
    print("🎯 SMART SPRITE SPLITTER")
    print("Handle images with different sprite counts")
    print("=" * 50)
    print("SELECT MODE:")
    print("1. Auto-detect sprite count (fast)")
    print("2. Manual input per file (accurate)")
    print("3. Load from config file")
    print("4. Create config file only")
    
    choice = input("\nChoose (1/2/3/4): ").strip()
    
    if choice == "1":
        input_folder = input("Input folder: ").strip() or "input"
        output_folder = input("Output folder: ").strip() or "output"
        
        # Auto-detect and process immediately
        print("\n🤖 Auto-detect mode enabled...")
        batch_split_smart(input_folder, output_folder, "auto_config.json")
    
    elif choice == "2":
        manual_config_mode()
    
    elif choice == "3":
        input_folder = input("Input folder: ").strip() or "input"
        output_folder = input("Output folder: ").strip() or "output"
        config_file = input("Config file: ").strip() or "sprite_config.json"
        
        batch_split_smart(input_folder, output_folder, config_file)
    
    elif choice == "4":
        input_folder = input("Input folder: ").strip() or "input"
        config_file = input("Config file name: ").strip() or "sprite_config.json"
        
        create_sprite_config(input_folder, config_file)
        print(f"\n📝 Edit '{config_file}' to adjust the sprite count")
        print("Then run again with mode 3")
    
    else:
        print("❌ Invalid choice!")
        
        