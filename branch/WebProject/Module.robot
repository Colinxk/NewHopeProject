*** Settings ***
Library           Selenium2Library
Library           DatabaseLibrary
Library           String
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
Resource          new_underlying.txt
Library           Lib/MyLib.py

*** Test Cases ***
新增种猪档案-查询
    [Documentation]    1. 登录系统（管理员权限）
    ...    2. Click【新增种猪档案】
    ...    3. 输入组织等必填信息
    ...    4. 输入种猪对应必填信息
    ...    5. 点击【保存】
    ...    6. 输入耳牌号
    ...    7. 点击【查询】
    ...    8. 点击【批量导入】 9. 导入模板，验证种猪档案 10. 上传种猪档案 11. 查询上次的种猪档案 12. 点击【退出】 13. 点击【确定】
    初始化_smart_event
    登录    4    Data.csv
    Menu_点击猪种档案
    sleep    1
    新增种猪档案    2017-9-9    20170123    2017-7-1
    查询种猪档案    20170123
    批量导入种猪档案    SMARTPIG-慧养猪-种猪档案批量导入模板.xlsx
    查询种猪档案    20180318
    Menu_点击退出
    Menu_确定退出
    close browser

种猪档案_统计验证
    [Documentation]    1. 登录系统（管理员权限）
    ...    2 比对统计信息
    ...    3 选定高密猪场_后备舍查询并比对统计信息
    ...    4. 点击【退出】
    ...    5. 点击【确定】
    登录    4    Data.csv
    Menu_点击猪种档案
    统计验证    1    Data2.csv
    Menu_点击退出
    Menu_确定退出
    close browser

种猪档案_重置验证
    登录    4    Data.csv
    Menu_点击猪种档案
    重置验证
    Menu_点击退出
    Menu_确定退出
    close browser
    Comment    还原_smart_event

test
    Comment    ${a}    create list    test1    test2
    Comment    log    ${a[0]}
    Comment    ${b}    Evaluate    type($a[0])
    Comment    ${a}    Set Variable    九月
    Comment    ${a1}    Evaluate    str($a)    \    #unicode转为str
    Comment    ${b}    Evaluate    type($a1)
    Comment    log    ${b}
    Comment    ${t1}    Set Variable    合计：10144
    Comment    ${t2}    decode bytes to string    ${t1}    utf-8
    Comment    log    \uff1a
    Comment    ${t3}    evaluate    re.findall(u"\uff1a(.+)",$t1)    re
    Comment    log    ${t3}
    Comment    ${c}    Evaluate    type($t3[0])
    Comment    log    ${c}
    Comment    ${d}    Evaluate    str($t3[0])
    Comment    log    ${d}
    Comment    ${e}    Evaluate    type($d)
    Comment    ${data2}    Read Csv File    2    Data2.csv
    Comment    log    ${data2}
    Comment    初始化_smart_base
    Comment    ${a}    Set Variable    09
    Comment    ${d}    create dictionary
    Comment    set to dictionary    ${d}    09=九月    08=八月
    Comment    ${keys}=    get dictionary keys    ${d}
    Comment    : FOR    ${var}    IN    ${d}
    Comment    \    run keyword if    '${var}'=='${a}'    run keyword    log    ${var}
    Comment    log    ${keys}
    Comment    log    ${d[0]}
    Comment    &{dict1}=    create dictionary    09=九月    08=八月
    Comment    ${dict}=    &{dict1}
    Comment    ${keys}=    get dictionary keys    ${dict}
    Comment    log    ${keys}
    Comment    ${a}    Set Variable    打开
    Comment    ${d}    Evaluate    str($a)
    Comment    log    ${d}

test2
    Comment    ${b}    Conversion    9
    Comment    &{dict} =    Create Dictionary    Jan=一月    Feb=二月    Mar=三月    Apr=四月
    ...    May=五月    June=六月    Jully=七月    Aum=八月    Sept=九月    Oct=十月
    ...    Nov=十一月    Dec=十二月
    Comment    Length Should Be    ${dict}    12
    Comment    log    ${dict}
    Comment    ${a}    Set Variable    Dec
    Comment    Comment    ${a1}    Evaluate    str($a)    \    #unicode转为str
    Comment    Comment    ${a2}    Evaluate    type($a1)
    Comment    Log    ${dict.${b}}
