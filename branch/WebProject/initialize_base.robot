*** Settings ***
Library           Selenium2Library
Library           DatabaseLibrary
Library           String
Resource          Elements_登录.txt    # 登录页面元素
Resource          Elements_组织管理.txt    # 组织管理页面元素
Resource          Elements_猪场管理.txt    # 猪场管理页面元素
Resource          Elements_Menu.txt    # 菜单元素
Resource          Elements_用户管理.txt    # 用户管理页面元素
Resource          Task.txt    # 业务层
Resource          Elements_种猪档案.txt
Resource          Elements_供应商管理.txt
Resource          Elements_客户管理.txt
Resource          Elements_物料管理.txt
Library           AutoItLibrary
Library           Lib/MyLib.py

*** Test Cases ***
Init_base
    初始化_smart_base
    sleep    3

Init_event
    初始化_smart_event
    sleep    3
