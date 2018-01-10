#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import commands
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from PIL import Image, ImageOps
import pytesseract
import requests
import urllib

SCREEN_SHOT_PATH = "/sdcard/hero_screenshot.png"

ROOT = os.path.dirname(os.path.abspath(__file__))

LOCAL_SCREEN_PATH = '{}/screenshot.png'.format(ROOT)

MAX_RETRY_TIME = 3


def run_command(cmd):
    retry = 0
    while retry < MAX_RETRY_TIME:
        status, output = commands.getstatusoutput(cmd)
        print("the status is %d, and the result is %s" %(status, output))
        if status != 0:
            retry += 1
            continue
        return status, output

def capture():
    cmd = "adb shell /system/bin/screencap -p {}".format(SCREEN_SHOT_PATH)
    run_command(cmd)

def transfer():
    cmd = "adb pull {} {}".format(SCREEN_SHOT_PATH, LOCAL_SCREEN_PATH)
    print("local path is : %s" % LOCAL_SCREEN_PATH)
    run_command(cmd)

def recognition():
    file = Image.open(LOCAL_SCREEN_PATH)

    question_box = file.crop((50, 205, 1100, 560))
    question = pytesseract.image_to_string(question_box, lang='chi_sim')
    question = question[question.index(u'.')+1:]
    print(question)

    """
        回答 TODO:
    """
    #answers = []
    """"
    answer_box = file.crop((50, 560, 1100, 1300))
    answer_box = answer_box.convert("RGB")
    pixdata = answer_box.load()
    width, height = answer_box.size
    for y in xrange(height):
        for x in xrange(width):
            if pixdata[x, y] == (230, 235, 239):
                pixdata[x, y] = (255, 255, 255)
            item = pixdata[x, y]
            if (item[0]>=137 and item[0]<= 140) and (item[1]>=144 and item[1]<=185) and (item[2]>=148 and item[2]<=170):
                pixdata[x, y] = (0, 0, 0)

    answers = pytesseract.image_to_string(answer_box, lang='chi_sim')
    """

    return question

def search(question):
    params = {'wd': question}
    query = urllib.urlencode(params)
    print(query)
    url = u"https://www.baidu.com/s?"+query
    cmd = u'open "{}"'.format(url)
    print(url)
    run_command(cmd=cmd)

def main():
    import time

    begin = time.time() * 1000

    capture()

    transfer()

    question = recognition()

    search(question)

    #analyze(question, answers)

    end = time.time() * 1000

    print "cost time: ", (end-begin), " ms"


if __name__ == '__main__':
    main()