#coding=utf-8
import re
def _isContainChinese(word):
    zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')

    # word = word.decode()
    match = zh_pattern.search(word)

    return True if match is not None else False


ad="Edit the Expression 你好吧是打发& Text to see matches. Roll over matches or t"
print(_isContainChinese(ad))