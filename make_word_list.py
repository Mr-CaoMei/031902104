import os
import pypinyin


def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s


curr_dir = os.path.dirname(os.path.abspath(__file__))
org_path = os.path.join(curr_dir, 'org.txt')
words_path = os.path.join(curr_dir, 'words.txt')  # 绝对路径的获取
words_list = []
with open(words_path, 'r', encoding="utf-8") as file1_object:
    lines1 = file1_object.readlines()
    for line in lines1:
        words_list.append(line.strip())  # 将敏感词存储在列表words_list中
        words_list.append(pinyin(line))
print(words_list)
