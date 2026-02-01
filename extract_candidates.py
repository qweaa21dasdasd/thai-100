
import re
import sys
import json

def parse_time(t_str):
    h, m, s_ms = t_str.split(':')
    s, ms = s_ms.split(',')
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0

def get_candidates(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    blocks = re.split(r'\n\s*\n', content.strip())
    parsed_blocks = []
    
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            idx = lines[0]
            time_line = lines[1]
            text = "\n".join(lines[2:])
            text_lines = [l.strip() for l in lines[2:] if l.strip()]
            
            if '-->' in time_line:
                start_str, end_str = time_line.split(' --> ')
                start = parse_time(start_str)
                end = parse_time(end_str)
                duration = end - start
                
                parsed_blocks.append({
                    'index': idx,
                    'start_str': start_str,
                    'end_str': end_str,
                    'start': start,
                    'end': end,
                    'duration': duration,
                    'text_lines': text_lines
                })

    # Filter logic: Duration > 4s AND >= 2 lines AND lines different
    candidates = []
    for b in parsed_blocks:
        if b['duration'] > 4.0 and len(b['text_lines']) >= 2:
            if b['text_lines'][0] != b['text_lines'][1]:
                # Heuristic: The first line is usually the Thai sentence
                candidates.append({
                    'index': b['index'],
                    'start_str': b['start_str'],
                    'end_str': b['end_str'],
                    'thai_text': b['text_lines'][0],
                    'phonetic_text': b['text_lines'][1]
                })
    return candidates

def main():
    srt_file = sys.argv[1]
    candidates = get_candidates(srt_file)
    
    print(f"Found {len(candidates)} candidates.")
    
    # Dump to JSON for easy reading by LLM
    print(json.dumps(candidates, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
