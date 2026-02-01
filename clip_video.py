
import re
import os
import subprocess
import sys

def parse_time(t_str):
    h, m, s_ms = t_str.split(':')
    s, ms = s_ms.split(',')
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0

def clean_filename(text):
    # Take first line
    line = text.strip().split('\n')[0].strip()
    # Remove invalid chars
    return re.sub(r'[\\/*?:"<>| ]', "_", line)

def get_anchors(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    blocks = re.split(r'\n\s*\n', content.strip())
    anchors = []
    
    parsed_blocks = []
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            time_line = lines[1]
            text = "\n".join(lines[2:])
            if '-->' in time_line:
                start_str, end_str = time_line.split(' --> ')
                start = parse_time(start_str)
                end = parse_time(end_str)
                parsed_blocks.append({
                    'start': start,
                    'end': end,
                    'duration': end - start,
                    'text': text,
                    'lines_count': len(lines[2:])
                })

    # Heuristic
    for b in parsed_blocks:
        lines = b['text'].strip().split('\n')
        if len(lines) >= 2 and b['duration'] > 4.0:
            if lines[0].strip() != lines[1].strip():
                anchors.append(b)
    return anchors

def main():
    srt_file = "thai_chinese.srt"
    video_file = "常用泰语100句 - 天天泰语 (720p, h264).mp4"
    output_dir = "clips_chinese"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Modified parsing for generated SRT
    anchors = []
    with open(srt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    blocks = re.split(r'\n\s*\n', content.strip())
    
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            # Format: Index, Time, Thai, Chinese
            # Or Index, Time, Thai (if Chinese missing, but we generated it)
            time_line = lines[1]
            if '-->' in time_line:
                start_str, end_str = time_line.split(' --> ')
                start = parse_time(start_str)
                end = parse_time(end_str)
                
                # Assume last line is Chinese, second to last is Thai
                chinese_text = lines[-1]
                thai_text = lines[-2] if len(lines) > 2 else ""
                
                anchors.append({
                    'start': start,
                    'end': end,
                    'duration': end - start,
                    'text': chinese_text, # Use Chinese for filename
                    'lines_count': len(lines)
                })
    print(f"Found {len(anchors)} anchors.")
    
    prev_end = 0.0
    
    # Create a log file
    with open("clips_log.txt", "w", encoding="utf-8") as log:
        for i, anchor in enumerate(anchors):
            start = prev_end
            end = anchor['end']
            prev_end = end
            duration = end - start
            
            # Filename
            name = clean_filename(anchor['text'])
            # Add index
            filename = f"{i+1:03d}_{name}.mp4"
            out_path = os.path.join(output_dir, filename)
            
            print(f"Clipping {i+1}/{len(anchors)}: {filename} ({duration:.2f}s)")
            log.write(f"{filename}\t{start}\t{end}\n")
            
            cmd = [
                "ffmpeg", "-y",
                "-ss", str(start),
                "-i", video_file,
                "-t", str(duration),
                "-c:v", "libx264", "-c:a", "aac",
                "-preset", "ultrafast", # Use ultrafast for speed
                out_path
            ]
            # Capture output to avoid clutter, but check for errors
            result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            if result.returncode != 0:
                print(f"Error clipping {filename}: {result.stderr.decode()}")

if __name__ == "__main__":
    main()
