#coding=UTF-8

import time, os, platform, sys

def scrrenRecord():
    # 获取当前时间戳, 并用以文件命名;
    timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    fileName = 'screenRecord_' + timestamp + '.mp4'
    os.popen('adb wait-for-device')
    # 根据用户运行系统平台编辑不同命令, 获取输入值用作视频录制时长;
    if platform.system() == 'Windows':
        timeLimit = raw_input('请输入录制视频时长（单位:秒）, 直接回车默认录制10秒: '.decode('utf-8').encode('gbk'))
    else:
        timeLimit = raw_input(u'请输入录制视频时长（单位:秒）, 直接回车默认录制10秒: ')
    # 如输入为空则默认录制10秒视频;
    if timeLimit == '':
        print u'开始录制10秒视频。'
        command = 'adb shell screenrecord --time-limit 10 /sdcard/%s' %fileName
    # 判断输入值是否为数字, 如为数字且小于等于180则开始录制视频, 非数字则报出错误信息;
    else:
        try:
            recordTime = int(timeLimit)
            if recordTime <= 180:
                print u'开始录制%s秒视频。' %recordTime
                command = 'adb shell screenrecord --time-limit %s /sdcard/%s' %(recordTime, fileName)
        except:
            print u'参数输入错误, 请输入1-180数字。'
            sys.exit()
    os.popen(command)
    # 录制视频后拷贝视频到本地, 并删除手机内视频文件;
    print u'正在拷贝%s至脚本所在路径。' %fileName
    os.popen('adb pull /sdcard/' + fileName)
    os.popen('adb shell rm /sdcard/' + fileName)

if __name__ == '__main__':
    scrrenRecord()