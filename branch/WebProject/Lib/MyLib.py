# coding=utf-8

import os, time, subprocess, sys, csv, datetime, chardet

def read_csv_file(input_value, Filename):
    '''
    读取数据文件
    input_value:    所取数据的第几行
    Filename：     文件名
    '''
    BASE_DIR = os.path.dirname(os.path.dirname(__file__)) #返回上级路径 类似..
    file_path = os.path.join(BASE_DIR, 'Data', Filename) #组合成绝对路径
    for var in csv.DictReader(open(file_path)):
        intvar = var['No']
        if intvar == input_value:
            break
    return var

def stopchromedriver():
    '''
    关闭chromedriver
    '''
    str1 = "taskkill /F /IM chromedriver.exe"
    os.system(str1)
    str1 = "taskkill /F /IM chrome.exe"
    os.system(str1)
    print "stop chrome..."

def get_temp_path(tempname):
    '''
    获取模板地址
    tempname:   模版名称
    '''
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(BASE_DIR, 'Template', tempname)
    return file_path

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

def Conversion(month):
    MonthInt = int(month)
    if MonthInt > 12:
        print "wrong input"
    else:
        MonthStr = str(month)
        dict = {"1": "Jan", "2": "Feb", "3": "Mar", "4": "Apr", "5": "May", "6": "June",
                "7": "July","8": "Aug", "9": "Sept", "10": "Oct", "11": "Nov", "12": "Dec"}
        return dict[MonthStr]