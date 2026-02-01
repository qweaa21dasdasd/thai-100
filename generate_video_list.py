
import os
import json

def generate_video_list():
    clips_dir = "clips_chinese"
    if not os.path.exists(clips_dir):
        print(f"Directory {clips_dir} not found.")
        return

    files = [f for f in os.listdir(clips_dir) if f.endswith(".mp4")]
    files.sort() # Ensure order by filename (which has index)
    
    with open("videos.json", "w", encoding="utf-8") as f:
        json.dump(files, f, ensure_ascii=False, indent=2)
    
    print(f"Generated videos.json with {len(files)} videos.")

if __name__ == "__main__":
    generate_video_list()
