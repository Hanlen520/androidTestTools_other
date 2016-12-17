#coding=UTF-8

import os, time, platform, sys

# 创建日志存储文件夹;
timestamp = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
folderName = 'dropBoxLog_' + timestamp
os.mkdir(folderName)
time.sleep(1)

# 获取dropbox命令所有返回值并过滤有效值;
dropboxList = []
dropboxList_save = []
anr = 0
dropboxList_all = os.popen('adb shell dumpsys dropbox').readlines()
for dropboxLog in dropboxList_all:
    if 'system_app_crash' in dropboxLog or 'data_app_crash' in dropboxLog or 'system_app_anr' in dropboxLog or 'data_app_anr' in dropboxLog:
        log_position =  dropboxList_all.index(dropboxLog)
        log = dropboxList_all[log_position] + dropboxList_all[log_position + 1]
        dropboxList.append(log)
print dropboxList

# 根据用户运行系统平台编辑不同命令;
if platform.system() == 'Windows':
    logCount_input = raw_input('点回车默认取最后1份日志, 输入任意字符则获取所有日志:'.decode('utf-8').encode('gbk'))
else:
    logCount_input = raw_input('点回车默认取最后1份日志, 输入任意字符则获取所有日志:')

if len(dropboxList) > 0:
    # 如输入为空则取最后一份log, 反之取所有log;
    if logCount_input != '':
        dropboxList_save = dropboxList
        print u'共%s份日志, 正在获取...' %len(dropboxList_save)
    else:
        dropboxList_save.append(dropboxList[-1])
else:
    print u'dropbox内无有效日志, 程序退出。'
    os.rmdir(folderName)
    sys.exit()


logCount = len(dropboxList_save)
for i in range(logCount):
    dropCommand_element = dropboxList_save[i].replace('\r\n', '').split(' ')
    ymd = dropCommand_element[0]
    hms = dropCommand_element[1]
    logTimestamp = ymd.replace('-', '') + hms.replace(':', '')
    if 'anr' in dropCommand_element[2]:
        anr = 1
        errType = 'ANR'
    else:
        errType = 'CRASH'
    # 返回process字段的位置, 用以计算截取processName;
    if 'Process:' in dropCommand_element:
        processName_position = dropCommand_element.index('Process:') + 1
        processName = dropCommand_element[processName_position].split('/')[0]
    else:
        processName = None
    writeLogCommand = 'adb shell dumpsys dropbox --print %s %s > ./%s/%s_%s_%s.log' %(ymd, hms, folderName, logTimestamp, errType, processName)
    # writeLogCommand = 'adb shell dumpsys dropbox --print %s %s' %(ymd, hms)
    os.system(writeLogCommand)
if anr == 1:
    os.system('adb pull /data/anr ./%s/' %folderName)

print u'日志获取完毕。'