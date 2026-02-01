
import re
import sys

def check_chinese(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex for CJK characters
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', content)
    
    if chinese_chars:
        print(f"Found {len(chinese_chars)} Chinese characters.")
        print(f"Sample: {chinese_chars[:20]}")
    else:
        print("No Chinese characters found in the file.")

    # Also print some lines that might look like they end the sentence
    print("\nChecking for lines that might be the 'Chinese' part (Thai transliteration):")
    blocks = re.split(r'\n\s*\n', content.strip())
    for i, block in enumerate(blocks[:20]): # Check first 20 blocks
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            print(f"Block {lines[0]}: {lines[2:]}")

if __name__ == "__main__":
    check_chinese(sys.argv[1])
