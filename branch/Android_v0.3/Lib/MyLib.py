# coding=utf-8

import os, time, subprocess, sys, csv, chardet, re, datetime
from appium import webdriver

def startapp(android_path, android_app):
    '''
    启动模拟器
    android_path:   模拟器所在路径
    android_app:	模拟器名称
    Genymotion 是基于vbox的虚拟机运行的，所以以命令行模式启动时，所有的vbox虚拟机进程和adb进程是挂在第一个发起的进程下，调试时
    如果遇到命令行启动不了Genymotion 可能是由于VBOX和ADB绑定了的进程，请运行注释了的代码，释放ADB和VBOX
    '''
    PreStepNeceStr =  "taskkill /F /IM player.exe" #启动前杀掉可能存在的player进程,头次启动会很慢因为需要启动vbox虚拟机
    PreStepStr = "taskkill /F /IM adb.exe & taskkill /F /IM VBoxSVC.exe & taskkill /F /IM VBoxHeadless.exe & taskkill /F /IM VBoxNetDHCP.exe"
    print PreStepNeceStr
    PreStepNece = subprocess.Popen(PreStepNeceStr, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    Judge = PreStepNece.stdout.read()
    PreStepNece.stdout.close()
    Env = chardet.detect(Judge)['encoding']
    if str(Env) == "None":
        print PreStepNece.stderr.read().decode('gbk')
        PreStepNece.stderr.close()
    else:
        print Judge.decode('gbk')
    ############杀掉所有相关进程释放vbox###########
    print PreStepStr
    PreStep = subprocess.Popen(PreStepStr, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    Judge = PreStep.stdout.read()
    PreStep.stdout.close()
    Env = chardet.detect(Judge)['encoding']
    # print Env
    if str(Env) == "None":
        print PreStep.stderr.read().decode('gbk')
        PreStep.stderr.close()
    else:
        print Judge.decode('gbk')
    time.sleep(1)
    try:
        PreStepNece.terminate()
        pass
    except:
        print "error"
    try:
        PreStep.terminate()
        pass
    except:
        print "error"
    Str = "cd " + android_path + " & " + "player --vm-name \"" + android_app + "\""
    StrUse = "d: &" + Str
    print StrUse
    startapp = subprocess.Popen(StrUse, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    print "started Genymotion"
    # print "Start andoid simulator..."
    time.sleep(15)
    try:
        startapp.terminate()
        pass
    except:
        print "error"
    return startapp

def New_Is_started(path, file):
    '''
     用Genymotion日志判断底层虚拟机是否已经启动，未启动则继续待机5秒，
     path: Genymotion 日志所在路径
     file: 日志名
    '''
    destfile = os.path.join(path, file)
    os.chdir(path)#切换路径
    # print os.getcwd()
    Juge = "false"
    for Time in range(0,100,1):
        Content = open(file, "r")
        lines = Content.readlines()
        # print lines
        Content.close()
        for L in lines:
            # print L
            Str = r"VM engine version: \"5.2.6r120293\""
            Switch = re.search(Str,L)
            # print Switch
            if Switch:
                Juge = "true"
        if Juge == "true":
            print "Vbox is started"
            break
        else:
            print "System is starting, Please wait 5 SEC"
            time.sleep(5)
#########最后clean日志#################
    os.remove(destfile)
    open(destfile, "w+").close()
    print "The Vbox log has been cleaned"
#########检验开机动画是否加载完毕#################
    for Time in range(0,100,1):
        Str = "adb shell getprop init.svc.bootanim"
        StopGenymotion = subprocess.Popen(Str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        print (StopGenymotion.stderr.read().decode('gbk'))
        StopGenymotion.stderr.close()
        Text = StopGenymotion.stdout.read().decode('gbk')
        StopGenymotion.stdout.close()
        print Text
        if Text:
            try:
                StopGenymotion.terminate()
                pass
            except:
                print "error"
        # print re.search(r'(stopped)',Text)
        if re.search(r'(stopped)',Text):
            print "genymotion is started"
            break
        else:
            print "genymotion is starting, Please wait 5 SEC"
            time.sleep(5)

def StopAppium():
    '''
    关闭Appium服务
    appium:   Appium进程名
    '''
    Str = "netstat -nao |findstr /c:\"TCP    127.0.0.1:4723         0.0.0.0:0\""# CMD下/c: 可以包含空格，默认情况下CMD命令没法使用空格
    StopAppiumpro = subprocess.Popen(Str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    print (StopAppiumpro.stderr.read().decode('gbk'))
    StopAppiumpro.stderr.close()
    Text = StopAppiumpro.stdout.read().decode('gbk')
    print Text
    if not Text:
        print "Appium is not started,Not needed kill"
        try:
            StopAppiumpro.terminate()
            pass
        except:
            print "error"
        return Text
    Pid = re.findall("LISTENING       (.+)\r", Text)
    StopAppiumpro.stdout.close()
    try:
        StopAppiumpro.terminate()
        pass
    except:
        print "error"
    # print Pid[0]
    StrKill = "taskkill /F /IM  " + str(Pid[0])
    print StrKill
    KillAppium = subprocess.Popen(StrKill, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    print (KillAppium.stderr.read().decode('gbk'))
    KillAppium.stderr.close()
    print (KillAppium.stdout.read().decode('gbk'))
    KillAppium.stdout.close()
    try:
        KillAppium.terminate()
        pass
    except:
        print "error"


def RebootGeny():
    '''
    连接到adb
    '''
    Str = "adb shell reboot"
    RebootGeny = subprocess.Popen(Str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    print 'Reboot Genymotion'
    time.sleep(1)
    try:
        RebootGeny.terminate()
        pass
    except:
        print "error"
    for Time in range(0,100,1):
        # print "1111"
        Str2 = "adb shell getprop init.svc.bootanim"
        StopGenymotion1 = subprocess.Popen(Str2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        TxError = (StopGenymotion1.stderr.read().decode('gbk'))
        StopGenymotion1.stderr.close()
        Text = StopGenymotion1.stdout.read().decode('gbk')
        StopGenymotion1.stdout.close()
        try:
            StopGenymotion1.terminate()
            pass
        except:
            print "error"
        print Text
        if re.search(r'(no devices)', TxError):
            print "genymotion is restarted"
            break
        else:
            print "genymotion is rebooting, Please wait 2 SEC"
            time.sleep(2)
    for Time in range(0,100,1):
        Str3 = "adb shell getprop init.svc.bootanim"
        StopGenymotion = subprocess.Popen(Str3, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        print (StopGenymotion.stderr.read().decode('gbk'))
        StopGenymotion.stderr.close()
        Text = StopGenymotion.stdout.read().decode('gbk')
        StopGenymotion.stdout.close()
        print Text
        if Text:
            try:
                StopGenymotion.terminate()
                pass
            except:
                print "error"
        # print re.search(r'(stopped)',Text)
        if re.search(r'(stopped)',Text):
            print "genymotion is started"
            break
        else:
            print "genymotion is starting, Please wait 5 SEC"
            time.sleep(5)


def selectmonth(str_date_origin, str_date_input):
    '''
    选择日期（只能选月份）
	locator_date_origin:	已选日期的locator
	str_date_input:		要选的日期“yyyy-mm-dd”
	locator_month_pre:	向前一个月的locator
	locator_month_next:	向后一个月的locator
	'''
    date_origin_list = str_date_origin.strip(' ').split('-')
    date_input_list = str_date_input.split('-')
    date_origin_list[1] = date_origin_list[1].strip(' ').lstrip('0')
    date_input_list[1] = date_input_list[1].strip(' ').lstrip('0')
    date_y = int(date_input_list[0].strip(' ')) - int(date_origin_list[0].strip(' '))
    date_m = int(date_input_list[1]) - int(date_origin_list[1])
    res = date_y * 12 + date_m
    return res


def read_csv_file(input_value):
    '''
    读取数据文件
    input_value:    所选的环境
    '''
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(BASE_DIR, 'Data', 'Data.csv')
    for Strvar in csv.DictReader(open(file_path)):
        if Strvar['No']==input_value:
            break
    return Strvar

def NewStartAppium(destfile):
    '''
    启动Appium服务
    appium_path:   Appium所在路径
    '''
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(BASE_DIR, 'lib')
    os.chdir(file_path)
    print os.getcwd()
    ###########################清除日志###########################
    try:
        os.remove(destfile)
        open(destfile, "w+").close()
        print "The appium log has been cleaned"
        time.sleep(3)
        pass
    except:
        print "Warning: Log file is opened or in used by another process, Can not clean logs"
    Str = "start /b startappium.bat"
    startappium = subprocess.call(Str, shell=True, stdout=open(destfile,'w'), stderr=subprocess.STDOUT)
    print "Appium is starting"
    print startappium

def StartAutomator2(platformName, platformVersion, deviceName, apptarget, judge):
    '''
    robotframework 当前版本调用uiautomator2有问题，需要先在PYTHON调用PYclient预先安装uiautomator2-server到目标机上
    '''
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(BASE_DIR, 'apk')
    os.chdir(file_path)
    print os.getcwd()
    desired_caps = {}
    desired_caps['platformName'] = str(platformName)
    desired_caps['platformVersion'] = str(platformVersion)
    desired_caps['deviceName'] = str(deviceName)
    desired_caps['app'] = file_path + "\\" + apptarget
    desired_caps['noReset'] = str(judge)
    desired_caps['noSign'] = 'true'
    desired_caps['appPackage'] = 'com.newhope.smartpig.test1'
    desired_caps['appActivity'] = 'com.newhope.smartpig.module.main.LoginActivity'
    desired_caps['automationName'] = 'uiautomator2'
    desired_caps['newCommandTimeout'] = '6000'
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    time.sleep(3)
    driver.close_app()
    driver.quit()

def BackUpCurrent(Db_name):
    '''
    在SQL文件夹下建立当天的数据库导出用空文件,入参为数据库名称;删除超出10天的数据库文件
    返回参为文件是否存在1为存在，0为不存在，避免初始化反复写入，同批次脚本只用初始化一次
    '''
    SqlName = str(Db_name),"_",str(datetime.date.today())#获取当天时间,转化数据库名为STR方便组合
    CurrentName = ''.join(SqlName)+".sql"#组合数据库名和当天时间为联合名称
    Base_Dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))#获取当前文件上级路径
    File_Path = os.path.join(Base_Dir, 'Sql')#组合路径
    os.chdir(File_Path)#切换路径
    print os.getcwd()
####################################删除历史文件########################################
    LastestTime = datetime.date.today()+datetime.timedelta(days=-10) #当前时间7天前
    LastestTimeStr = str(LastestTime)
    print "Force deleted time is "+LastestTimeStr
    files = os.listdir(File_Path)
    for f in files:
        ################
        code_list = ['ISO-8859-1', 'GB2312']
        enc = chardet.detect(f) #识别当前对象的编码,chardet专用于识别编码并以字典储存
        if str(enc['encoding']) in code_list:
            f = f.decode('gbk')#以GBK解码，PYTHON内部是以unicode来识别的
            print "中文乱码处理转换后为"+ str(f)+"\n"
        ################
        destfile = os.path.join(File_Path, f);
        if (os.path.isfile(destfile)):  # 判断是否文件
            name = os.path.splitext(f)[0]  # 分离文件和后缀名
            postfix = os.path.splitext(f)[1]
            if (postfix == ".sql"):  # 只删除sql相关
                if name.find(Db_name) == 0:  # 只删除该数据库的
                    modifytime = time.localtime((os.path.getmtime(destfile)))  # 日期分片
                    year = modifytime[0]
                    month = modifytime[1]
                    day = modifytime[2]
                    Filedate = datetime.date(year, month, day)  # 将日期赋值给date
                    FiledateStr = str(Filedate)
                    print destfile+"     "+FiledateStr
                    if (LastestTime > Filedate):
                        print("The sql file will be deleted which over 10 days.")
                        os.remove(destfile)
                        print "Deleted file is "+destfile
####################################创建备份文件########################################
    # print File_Path
    if os.path.exists(CurrentName):
        print "Sql file existed"
        if (os.path.getsize(CurrentName) > 0): #判断文件是否为空
            return 1
        else:
            return 0
    else:
        open(CurrentName, "w+").close()#建立空文件
        print "Created"+" "+File_Path+"\\"+CurrentName
        return 0


def db_backup(evn_Data, dbname, Jenkins):
    '''
    备份数据库
    evn_Data:	环境设定
    dbname:     还原的数据库名称
    Jenkins;    Jenkins 开关1 ,为在Jenkins里使用
    '''
    SqlName = str(dbname),"_",str(datetime.date.today())#获取当天时间,转化数据库名为STR方便组合
    CurrentName = ''.join(SqlName)+".sql" # 组合数据库名和当天时间为联合名称
    StrUse = "cd " + evn_Data['dbDump_path']
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    File_Absolute = os.path.join(BASE_DIR, 'Sql', CurrentName)
    print evn_Data
    if os.path.exists(File_Absolute):
        if (os.path.getsize(File_Absolute) > 0):  # 判断文件是否为空
            print "backfile is existed"
            if Jenkins == str(1):
                Prompt = "@echo backfile is existed"
                JName = "BackUp_"+str(dbname)+".bat"
                CurrentJName = "C:\\robot"+"\\"+JName
                JFile = open(CurrentJName, "w+")
                JFile.write(str(Prompt))
                JFile.close()
        else:
            StrUse ="d: & " + StrUse + " & mysqldump -u" + evn_Data['dbUsername'] + " -p" + evn_Data['dbPassword'] + " --host=" + evn_Data['dbHost'] + " --port=" + evn_Data['dbPort'] +  " " + dbname + " > " + File_Absolute
            print StrUse
            if Jenkins == str(1): #Jenkins远程调用逻辑
                JName = "BackUp_"+str(dbname)+".bat"
                CurrentJName = "C:\\robot"+"\\"+JName
                JFile = open(CurrentJName, "w+")
                JFile.write(str(StrUse))
                JFile.close()
                return StrUse
            BackUp = subprocess.Popen(StrUse, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)#开启子进程,目的是为了如果写入时间过长，方便监视
            #BackUp.wait()
            BackUp.communicate() #wait取决于操作系统本身的pipe size可能造成溢出，而communicate使用的是内存，避免使用wait切记~
            print "Finished backup of database..."

def db_restore(evn_Data, dbname, Jenkins):
    '''
    还原数据库
    evn_Data:	环境设定
    dbname:     要还原的数据库名称
    Jenkins:    jenkins远程无法调用subprocess.Popen,把命令参数返回
    '''
    SqlName = str(dbname),"_",str(datetime.date.today())#获取当天时间,转化数据库名为STR方便组合
    CurrentName = ''.join(SqlName)+".sql"#组合数据库名和当天时间为联合名称
    StrUse = "cd " + evn_Data['dbDump_path']
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(BASE_DIR, 'Sql', CurrentName)
    TruncateStrUse = "d: & " + StrUse + " & mysql -u" + evn_Data['dbUsername'] + " -p" + evn_Data['dbPassword'] + " --host=" + evn_Data['dbHost'] + " --port=" + evn_Data['dbPort'] + " "  + "drop database " + dbname
    StrUse = "d: & " + StrUse + " & mysql -u" + evn_Data['dbUsername'] + " -p" + evn_Data['dbPassword'] + " --host=" + evn_Data['dbHost'] + " --port=" + evn_Data['dbPort'] + " " + dbname + " < " + file_path
    print TruncateStrUse
    print StrUse
    if Jenkins == str(1): #Jenkins远程调用逻辑
        JName = "Restore_"+str(dbname)+".bat"
        CurrentJName = "C:\\robot"+"\\"+JName
        JFile = open(CurrentJName, "w+")
        JFile.write(str(StrUse))
        JFile.close()
        return StrUse
    # Truncate = subprocess.Popen(TruncateStrUse, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    # Truncate.communicate()
    Restore = subprocess.Popen(StrUse, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    Restore.communicate()
    # print Restore.pid
    print "Finished restore of database..."