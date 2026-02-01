
import json
import os

# Manual translation mapping based on the Thai text found in the SRT
# I am providing the Chinese translation for the identified Thai sentences.
translations = {
    "สวัสดีค่ะ": "你好",
    "คุณสบายดีไหม": "你好吗",
    "ฉันสบายดี": "我很好",
    "ขอโทษ": "对不起",
    "ขอบคุณ": "谢谢",
    "ไม่ข้าวทราย": "不明白", # Likely typo for ไม่เข้าใจ or similar sound
    "ไม่เข้าใจ": "不明白",
    "ไม่เอา": "不要",
    "ไม่เป็นราย": "没关系", # Typo for ไม่เป็นไร
    "คุณชื่ออะไร": "你叫什么名字",
    "ฉันชื่อมานี": "我叫玛尼",
    "อามานี": "玛尼",
    "เดี๋ยวเจอกัน": "一会儿见",
    "คุณจะไปไหน": "你要去哪里",
    "คุณกินข้าวหรือยัง": "你吃饭了吗",
    "กินแล้ว": "吃过了",
    "ไม่ต้องกังวล": "别担心",
    "ฉันไปก่อนนะ": "我先走了",
    "We  Are จากประเทศจีน": "我们来自中国",
    "ฉันมาจากประเทศจีน": "我来自中国",
    "ฉันพูดไทยได้": "我会说泰语",
    "ห้องน้ำอยู่ที่ไหน": "洗手间在哪里",
    "ห้องน้ำอยู่ตรงนู้น": "洗手间在那边",
    "คุณอายุเท่าไหร่": "你多大",
    "หนูกี่ขวบแล้ว": "你几岁了",
    "ขอ": "给", # Context dependent, likely "Please give me" or "May I"
    "ราคาเท่าไหร่": "多少钱",
    "รู้แล้ว": "知道了",
    "แน่ใจหมาย": "确定吗", # Typo for แน่ใจไหม
    "ก็ไม่มีปัญหา": "没问题",
    "ฉันเห็นด้วย": "我同意",
    "ฟังไม่เข้าใจ": "听不懂", # Listen not understand
    "ฉันหิวแล้ว": "我饿了",
    "ทางจนปลาย": "一直走", # Context dependent
    "ระวังหน่อย": "小心点",
    "จริงๆหรอ": "真的吗",
    "แน่นอน": "当然",
    "เดินตรงไป": "直走",
    "ทำได้ดี": "做得好",
    "ก็ตามฉันมา": "跟我来", # Typo for ตามฉันมา
    "ฉันไม่ว่าง": "我没空",
    "ฉันอิ่มแล้ว": "我饱了",
    "เงียบหน่อย": "安静点",
    "ไปยางงายทั่วไปยางงายไปยังไง": "怎么去", # Garbled, likely "ไปอย่างไร"
    "สะดวกไหม": "方便吗",
    "เรียวเรียวหน่อย": "快点", # Typo for เร็วๆหน่อย
    "เรียวเรียวๆหน่อยเร็วๆหน่อย": "快点",
    "ฉันรักเธอ": "我爱你",
    "แต่": "但是",
    "ฉันคิดถึงเธอ": "我想你",
    "อร่อยไหม": "好吃吗",
    "กี่โมงแล้ว": "几点了",
    "ใครว่าเหรอ": "谁说的",
    "คุณว่าไง": "你说呢", # Or "What do you think"
    "ๆใจเย็น": "冷静点",
    "คุณบ้าไปแล้ว": "你疯了",
    "เหนื่อยจะตายแล้วถ้าเรา": "累死我了",
    "เหนื่อยจะตายแล้ว": "累死我了",
    "ยืมตังค์หน่อย": "借点钱",
    "เกิดอะไรขึ้น": "发生什么事了",
    "พูดช้าหน่อย": "说慢点",
    "ฉันเอาอันนี้": "我要这个",
    "คุณทำอะไรอยู่": "你在做什么",
    "ฉันเลี้ยงเอง": "我请客",
    "ฉันเอง": "是我",
    "ยินดีต้อนรับ": "欢迎光临",
    "ฝากเนื้อฝากตัวด้วย": "请多关照",
    "กรุณาพูดอีกครั้ง": "请再说一遍",
    "คุณใช้ WeChat หมาย": "你有微信吗", # Typo for ไหม
    "ฉันเป็นหวัด": "我感冒了",
    "ฉันไม่ทำแล้ว": "我不做了",
    "ดาย": "可惜", # Context likely เสียดาย
    "น่าเสียดาย": "真可惜",
    "ต้องลบกวนคุณแล้ว": "麻烦你了", # Typo for รบกวน
    "ต้องรบกวนคุณแล้ว": "麻烦你了",
    "ฉันหาไม่เจอ": "我找不到",
    "ฉันขับรถไม่ถ้าเป็น": "我不会开车", # Typo
    "ฉันขับรถไม่เป็น": "我不会开车",
    "ไม่มีเวลาแล้ว": "没时间了",
    "หุบป่า": "闭嘴", # Hup Pak -> Shut up
    "ฉันเป็นคนปากกิ่ง": "我是北京人", # Pak King -> Beijing
    "ฉันชอบอาหารทาย": "我喜欢泰国菜", # Thai -> Tai
    "ฉันกินเผ็ดไม่ได้": "我不能吃辣",
    "ฉันนหลงทาง": "我迷路了",
    "ฉันไม่ได้ยิน": "我听不见",
    "คุณอยู่ที่ไหน": "你在哪里",
    "ฉันไม่มีเงิน": "我没钱",
    "ขอขอขอดูหน่อย": "让我看看",
    "ฉันขอดูหน่อย": "让我看看",
    "คุณชินแล้วหรือยัง": "你习惯了吗",
    "ปวดหัว": "头痛",
    "ช่วงนี้เป็นไงบ้าง": "最近怎么样",
    "คุณชอบหมาย": "你喜欢吗", # Typo for ไหม
    "ฉันไม่มี": "我没有",
    "คุณยุ่งอยู่ไหม": "你忙吗",
    "ฉันเป็นครู": "我是老师",
    "นี่ไม่ใช่ความผิดฉัน": "这不是我的错",
    "ก็ไม่ใช่เรื่องของคุณ": "不关你的事",
    "อย่ามายุ่งกับฉัน": "别管我",
    "หยุดพูดเถอะ": "别说了",
    "ฉันเกลียดเธอ": "我讨厌你",
    "เชื่อฉัน": "相信我",
    "ช่วยฉันหน่อย": "帮帮我",
    "ฉันทำได้": "我做到了",
    "คุณน่ารักมาก": "你很可爱",
    "ๆคุณน่ารักมากๆคุณน่ารักมาก": "你很可爱",
    "ฉันไม่ดีเอง": "是我不好",
    "ไปด้วยกันนะ": "一起去吧",
    "ไปด้วยกันนะไปด้วยกันนะ": "一起去吧"
}

def generate_srt(candidates_file, output_file):
    # I will rely on the previous extraction logic to get candidates again, 
    # or I can just import the extraction script if I made it a module.
    # For simplicity, I will copy the candidates from the previous tool output since I can't easily pass data between tools except via files.
    # Actually, I'll read the 'extract_candidates.py' output if I saved it? 
    # No, I just printed it.
    
    # Re-run extraction
    import extract_candidates
    candidates = extract_candidates.get_candidates("/Users/meijin/Documents/thai-100/常用泰语100句 [-q7V-i5dlmA].th-orig.srt")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, c in enumerate(candidates):
            thai = c['thai_text']
            chinese = translations.get(thai, "")
            if not chinese:
                # Try partial match or fallback
                # For now use the phonetic line as fallback if translation missing, but I covered most.
                chinese = c['phonetic_text'] + " (Phonetic)"
            
            # Format:
            # Index
            # Start --> End
            # Thai
            # Chinese
            
            f.write(f"{i+1}\n")
            f.write(f"{c['start_str']} --> {c['end_str']}\n")
            f.write(f"{thai}\n")
            f.write(f"{chinese}\n")
            f.write(f"\n")
            
    print(f"Generated {output_file} with {len(candidates)} subtitles.")

if __name__ == "__main__":
    generate_srt(None, "thai_chinese.srt")
