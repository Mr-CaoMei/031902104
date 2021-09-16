import os
import re
import chardet
import pypinyin


def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s


curr_dir = os.path.dirname(os.path.abspath(__file__))
org_path = os.path.join(curr_dir, 'org.txt')
words_path = os.path.join(curr_dir, 'words.txt')  # 绝对路径的获取
ans_path = os.path.join(curr_dir, 'ans.txt')
# print(org_path)
words_list = []
with open(words_path, 'r', encoding="utf-8") as file1_object:
    lines1 = file1_object.readlines()
    for line in lines1:
        words_list.append(line.strip())  # 将敏感词存储在列表words_list中
        words_list.append(pinyin(line))
    # print(words_list)
int_count = 0
for line in open(org_path, 'r', encoding="utf-8"):
    line = re.sub('[^\\na-zA-Z\u4e00-\u9fa5]', '', line)  # 去除文档中除了汉字和字母的其他符号
    int_count += 1
    for word in words_list:
        if word in line:
            print("Line%d:<%s>%s\n" % (int_count, word, word))
            #str1 = str("Line%d:<%s>%s\n" % (int_count, word, word))
            #with open(ans_path, 'r+',encoding="utf-8") as file3_object:
                #file3_object.write("Line%d:<%s>%s\n" % (int_count, word, word))

# print(int_count)

# 自定义中文英文拼音格式化函数
