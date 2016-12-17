#!/usr/bin/python

import os, time


def screenshot():
    timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    os.popen('adb wait-for-device')
    os.popen('adb shell screencap -p /data/local/tmp/tmp.png')
    os.popen('adb pull /data/local/tmp/tmp.png ./' + str(timestamp) + '.png')
    os.popen("adb shell rm /data/local/tmp/tmp.png")
    print "success"

if __name__ == "__main__":
    screenshot()
