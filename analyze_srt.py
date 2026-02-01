
import re
import sys

def parse_time(t_str):
    h, m, s_ms = t_str.split(':')
    s, ms = s_ms.split(',')
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0

def analyze_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by double newlines to get blocks
    blocks = re.split(r'\n\s*\n', content.strip())
    
    parsed_blocks = []
    
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            idx = lines[0]
            time_line = lines[1]
            text = "\n".join(lines[2:])
            
            if '-->' in time_line:
                start_str, end_str = time_line.split(' --> ')
                start = parse_time(start_str)
                end = parse_time(end_str)
                duration = end - start
                
                parsed_blocks.append({
                    'index': idx,
                    'start': start,
                    'end': end,
                    'duration': duration,
                    'text': text,
                    'lines_count': len(lines[2:])
                })

    # Heuristic 1: Duration > 4s
    long_blocks = [b for b in parsed_blocks if b['duration'] > 4.0]
    print(f"Total blocks: {len(parsed_blocks)}")
    print(f"Blocks > 4s: {len(long_blocks)}")
    
    # Heuristic 2: 2 lines
    two_line_blocks = [b for b in parsed_blocks if b['lines_count'] >= 2]
    print(f"Blocks with >= 2 lines: {len(two_line_blocks)}")
    
    # Heuristic 4: 2 lines AND > 4s AND lines are different
    combined = [b for b in parsed_blocks if b['lines_count'] >= 2 and b['duration'] > 4.0]
    def lines_different(b):
        lines = b['text'].strip().split('\n')
        if len(lines) < 2: return False
        # Remove whitespace and compare
        return lines[0].strip() != lines[1].strip()

    final_candidates = [b for b in combined if lines_different(b)]
    print(f"Blocks > 4s AND >= 2 lines AND different content: {len(final_candidates)}")
    
    print("\nSample final candidates:")
    for b in final_candidates[:20]:
        print(f"Time: {b['start']} - {b['end']} ({b['duration']:.2f}s) | Text: {b['text'].replace(chr(10), ' ')}")

if __name__ == "__main__":
    analyze_srt(sys.argv[1])
