*** Settings ***
Library           Selenium2Library
Library           DatabaseLibrary
Library           String
Library           Lib/MyLib.py
Resource          Elements_登录.txt
Resource          Elements_组织管理.txt
Resource          Elements_猪场管理.txt
Resource          Elements_Menu.txt
Resource          Elements_用户管理.txt
Resource          Task.txt
Resource          Elements_种猪档案.txt
Library           RequestsLibrary
Library           requests
Library           Collections
Library           BuiltIn
Library           AutoItLibrary

*** Test Cases ***
test
    ${b}    Conversion    9
    &{dict} =    Create Dictionary    Jan=一月    Feb=二月    Mar=三月    Apr=四月    May=五月
    ...    June=六月    Jully=七月    Aum=八月    Sept=九月    Oct=十月    Nov=十一月
    ...    Dec=十二月
    Comment    Length Should Be    ${dict}    12
    Comment    log    ${dict}
    Comment    ${a}    Set Variable    Dec
    Comment    Comment    ${a1}    Evaluate    str($a)    \    #unicode转为str
    Comment    Comment    ${a2}    Evaluate    type($a1)
    Log    ${dict.${b}}
    Comment    log    添加成功

database
    ${Data}    Read Csv File    3    Data.csv
    Connect To Database Using Custom Params    mysql.connector    user='${Data['dbUsername']}',password='${Data['dbPassword']}',host='${Data['dbHost']}',port='${Data['dbPort']}'
    @{res}    query    show databases
    log many    @{res}
    初始化_smart_base
    Comment    还原_smart_base
    Comment    还原_smart_event
