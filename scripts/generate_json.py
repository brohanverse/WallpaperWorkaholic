import os
import json
import uuid

# Konfigurasi
GITHUB_USERNAME = "brohanverse"
REPO_NAME = "WallpaperWorkaholic"
BRANCH = "main"
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/{BRANCH}/"
IMAGES_DIR = "images"
OUTPUT_JSON = "wallpapers.json"

def generate_json():
    categories = []
    wallpapers = []
    
    if not os.path.exists(IMAGES_DIR):
        print(f"Folder '{IMAGES_DIR}' tidak ditemukan. Membuat folder...")
        os.makedirs(IMAGES_DIR)
        return
        
    # Daftar semua folder di dalam 'images' (dianggap sebagai Kategori)
    for category_name in os.listdir(IMAGES_DIR):
        category_path = os.path.join(IMAGES_DIR, category_name)
        
        if os.path.isdir(category_path):
            cat_id = f"cat_{uuid.uuid5(uuid.NAMESPACE_DNS, category_name).hex[:8]}"
            cat_wallpapers = []
            
            # Cari gambar di dalam folder kategori ini
            for img_file in os.listdir(category_path):
                if img_file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    # Nama file tanpa ekstensi untuk judul
                    title = os.path.splitext(img_file)[0].replace('_', ' ').replace('-', ' ').title()
                    wp_id = f"wp_{uuid.uuid5(uuid.NAMESPACE_DNS, img_file).hex[:8]}"
                    
                    image_url = f"{BASE_URL}{IMAGES_DIR}/{category_name}/{img_file}"
                    
                    wallpaper_obj = {
                        "id": wp_id,
                        "title": title,
                        "description": f"Wallpaper {title} dalam kategori {category_name}",
                        "imageUrl": image_url,
                        "thumbnailUrl": image_url, # Gunakan gambar yang sama sebagai thumbnail untuk mempermudah
                        "category": category_name,
                        "tags": [category_name.lower(), "wallpaper"],
                        "resolution": "1080x1920" # Default resolution
                    }
                    cat_wallpapers.append(wallpaper_obj)
                    wallpapers.append(wallpaper_obj)
            
            if len(cat_wallpapers) > 0:
                # Gunakan gambar pertama sebagai cover kategori
                cover_url = cat_wallpapers[0]['imageUrl']
                categories.append({
                    "id": cat_id,
                    "name": category_name,
                    "coverUrl": cover_url,
                    "wallpaperCount": len(cat_wallpapers)
                })

    # Susun JSON final
    final_json = {
        "categories": categories,
        "wallpapers": wallpapers
    }

    # Tulis ke file
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(final_json, f, indent=4, ensure_ascii=False)
        
    print(f"Berhasil menghasilkan {OUTPUT_JSON} dengan {len(categories)} kategori dan {len(wallpapers)} wallpaper.")

if __name__ == "__main__":
    generate_json()
