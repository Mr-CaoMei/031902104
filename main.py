# -*- coding:utf-8 -*-
import time
import os

curr_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件运行目录
org_path = os.path.join(curr_dir, 'org.txt')
words_path = os.path.join(curr_dir, 'words.txt')  
ans_path = os.path.join(curr_dir, 'ans.txt')
tire_list_path = os.path.join(curr_dir, 'tire_list.txt')  # 绝对路径的获取
time1 = time.time()
search = {'邪教': '邪教', '斜教': '邪教', 'xie教': '邪教', '邪较': '邪教', '牙阝孝攵': '邪教', 'fuck': 'fuck', 'Fuck': 'fuck',
          'FUCK': 'fuck',
          '法轮功': '法轮功', 'falungong': '法轮功', '法伦工': '法轮功', '发_囵_躬': '法轮功', '法伦功': '法轮功', '法轮g': '法轮功', 'f轮功': '法轮功',
          '法轮工': '法轮功',
          '法lun功': '法轮功', '氵去车仑工力': '法轮功', '发伦工': '法轮功', '灋輪功': '法轮功', 'FaLG': '法轮功', '珐轮功': '法轮功', '法l功': '法轮功',
          'fa轮功': '法轮功', }
# 创建衍生敏感词与初始敏感词匹配字典，便于在输出打印时打印初始敏感词
count_all = 0  # 统计敏感词出现个数


# DFA算法
class DfaFilter:
    def __init__(self):
        self.keyword_chains = {}  # 敏感词字典树
        self.delimit = '\x00'

    def add(self, keyword):  # 添加敏感词于敏感词字典树
        chars = keyword.strip()  # strip函数去除敏感词首尾无用字符，例如空白符，换行符，Tab符等
        if not chars:  # 排除空白行造成的敏感词筛选bug
            return
        level = self.keyword_chains
        for i in range(len(chars)):  # 敏感词字典树的迭代创建
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
        if i == len(chars) - 1:  # 定义敏感词字典树末尾定界符，便于判断敏感词匹配是否到达末尾
            level[self.delimit] = 0

    def parse(self, path):  # 从敏感词字典文档中导入初始敏感词以及衍生敏感词导入字典树当中
        with open(path, encoding='utf-8') as f:
            for keyword in f:
                self.add(str(keyword).strip())

    def filter(self, message, count):  # 逐行进行敏感词匹配，统计个数并输出
        count_all = 0  # 统计此行敏感词个数并作为函数返回值返回
        start = 0
        while start < len(message):
            level = self.keyword_chains
            step_ins = 0
            word_init = []
            word_change = []
            flag = 0
            for char in message[start:]:
                if char in level:
                    flag = 1
                    word_init.append(char)
                    # print(word_init, end="start：")
                    # print("%d", start)
                    word_change.append(char)
                    step_ins += 1
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        flag = 2
                        start += step_ins - 1
                        break
                else:
                    """if self.delimit == '\x00':
                        break"""
                    if not ('\u4e00' <= char <= '\u9fff'):
                        if flag == 1:
                            word_init.append(char)
                            # print(["非搜索："] + word_init)
                    else:
                        break
            """else:
                # ret.append(message[start])"""
            if flag == 2:
                str1 = ''.join(word_init)
                str2 = ''.join(word_change)
                str2 = search[str2]
                count_all += 1
                print("Line{}:<{}>".format(count, str2), ''.join(word_init), end="\n")
                f = open("self_ans.txt", 'a', encoding="utf-8")
                f.write("Line{}:<{}>{}\n".format(count, str2, str1))
                f.close()
                # print(''.join(word_change))
            start += 1

        return count_all


if __name__ == "__main__":
    gfw = DfaFilter()
    # path = "tire_list.txt"
    gfw.parse(tire_list_path)
    count = 1
    # print(gfw.keyword_chains)
    # Word = "法!@#$%^&*()+轮功法轮功"
    # gfw.filter(Word, 0)
    with open(org_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            count_all += gfw.filter(line, count)
            count += 1
    # print(text)
    # print(result)
    print("Total:{}".format(count_all))
    f = open("self_ans.txt", 'a', encoding="utf-8")  # 将输出结果打印入文档
    f.write("Total:{}".format(count_all))
    f.close()
time2 = time.time()
print('总共耗时：' + str(time2 - time1) + 's')  # 统 计程序运行处理时间
