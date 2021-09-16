import os
import re

# import chardet

curr_dir = os.path.dirname(os.path.abspath(__file__))
org_path = os.path.join(curr_dir, 'org.txt')
words_path = os.path.join(curr_dir, 'words.txt')  # 绝对路径的获取

for line in open(org_path, 'r', encoding="utf-8"):
    line = re.sub('[^\\na-zA-Z\u4e00-\u9fa5]', '', line)
    print(line)