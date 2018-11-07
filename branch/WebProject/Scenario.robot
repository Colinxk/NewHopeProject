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
Resource          new_underlying.txt
Library           Lib/MyLib.py

*** Test Cases ***
新增组织-猪场-用户（组织/用户）
    [Documentation]    0.初始化
    ...    1.管理员登录系统
    ...    2.点击左侧菜单【组织管理】
    ...    3.点击【新增组织】
    ...    4.输入内容，点击【保存并关闭】
    ...    5.点击【基础数据管理】
    ...    6.点击【猪场管理】
    ...    7.点击【新建猪场】
    ...    8.编辑后点击【保存并关闭】
    ...    9.输入新增的组织名，点击【查询】
    ...    10.点击展开猪场下的猪舍
    ...    11.点击【新增单元】
    ...    12.输入点击【保存】
    ...    13.点击左侧菜单栏【系统管理】
    ...    14.点击【用户管理】
    ...    15.点击【新增】
    ...    16.输入必填项，点击【保存并关闭】
    ...    17.点击右上角【退出】
    ...    18.点击【确定】
    初始化_smart_base
    登录    3    Data.csv
    新增部门    test2    测试二    0002
    Menu_点击基础数据管理
    Menu_点击猪场管理
    新增猪场    6244    0285    19    7294    中山路123    9571
    Menu_点击退出
    登录    3    Data.csv
    Menu_点击基础数据管理
    Menu_点击猪场管理
    猪场管理_新增单元    测试二    ATWY    2    3
    Menu_点击系统管理
    Menu_点击用户管理
    新增用户    Xuke21    xuke1    123456    00982748281
    Menu_点击退出
    Menu_确定退出
    close browser

V2.0供应商管理
    [Documentation]    1. 点击【基础数据管理】--【供应商管理】
    ...    2. 录入必填项
    ...    3. 点击【保存并关闭】
    ...    4. 输入新增的供应商对应的授权公司名/编码/简称/供应商名称/联系电话等，点击【查询】
    ...    5. 点击供应商列表前面的修改按钮
    ...    6. 传入修改内容，点击【保存】
    ...    7. 点击该供应商前面的删除按钮
    ...    8. 点击【确定】
    登录    3    Data.csv
    Menu_点击基础数据管理
    sleep    1
    Menu_点击供应商管理
    sleep    1
    新增供应商    123451234512345    12345    导入测试公司    新希望六和
    查询供应商    新希望六和    123    ${EMPTY}    导入测试公司    ${EMPTY}
    编辑供应商    99999    更新供应商名称    简称    备注    详细地址    联系人
    ...    职位    12312312309
    查询供应商    ${EMPTY}    99999    简称    更新供应商名称    12312312309
    删除供应商
    Menu_点击退出
    Menu_确定退出
    close browser

V2.0客户管理
    [Documentation]    1. 点击【基础数据管理】--【客户管理】
    ...    2. 录入必填项
    ...    3. 点击【保存并关闭】
    ...    4. 输入新增的客户对应的授权公司名/编码/简称/客户名称等，点击【查询】
    ...    5. 点击客户列表前面的修改按钮
    ...    6. 传入修改内容，点击【保存】
    ...    7. 点击该客户前面的删除按钮
    ...    8. 点击【确定】
    登录    3    Data.csv
    Menu_点击基础数据管理
    sleep    1
    Menu_点击客户管理
    sleep    1
    新增客户    个人    123456789012345678    0403    客户名称20180403    简称0403    屠宰场
    ...    龙口六和养殖有限公司
    sleep    1
    查询客户    龙口六和养殖有限公司    0403    客户名称20180403    简称0403    个人    全部
    ...    全部    正常    1
    编辑客户    公司    122101    客户名称更新    简称更新    养殖公司    备注
    ...    详细地址    联系人    职位    12345678901    临沭六和种猪有限公司
    查询客户    临沭六和种猪有限公司    122101    客户名称更新    简称更新    公司    全部
    ...    全部    正常    2
    删除客户
    Menu_点击退出
    Menu_确定退出
    close browser

V2.0物料管理
    [Documentation]    1. 点击【基础数据管理】--【客户管理】
    ...    2. 录入必填项
    ...    3. 点击【保存并关闭】
    ...    4. 输入新增的客户对应的授权公司名/编码/简称/客户名称等，点击【查询】
    ...    5. 点击客户列表前面的修改按钮
    ...    6. 传入修改内容，点击【保存】
    ...    7. 点击该客户前面的删除按钮
    ...    8. 点击【确定】
    登录    3    Data.csv
    Menu_点击基础数据管理
    sleep    1
    Menu_点击物料管理
    sleep    2
    新增物料    0313    物料名称0313    饲料    仔猪教槽料    kg    ${EMPTY}
    ...    无    \    \    \    ${EMPTY}    ${EMPTY}
    ...    临沭六和种猪有限公司
    查询物料    临沭六和种猪有限公司    0313    物料名称0313    \    \    正常
    编辑物料    030902    物料名称0313更新    药品    消毒药    简称0313更新    袋
    ...    袋    1    生产商    经销商    ${EMPTY}    备注
    ...    龙口六和养殖有限公司
    查询物料    龙口六和养殖有限公司    030902    物料名称0313更新    \    ${EMPTY}    正常
    删除物料
    Menu_点击退出
    Menu_确定退出
    close browser

database
    ${Data}    Read Csv File    3    Data.csv
    log    ${Data}
    Connect To Database Using Custom Params    mysql.connector    user='${Data['dbUsername']}',password='${Data['dbPassword']}',host='${Data['dbHost']}',port='${Data['dbPort']}'
    @{res}    query    show databases
    log many    @{res}
    Comment    初始化_smart_base
    Comment    sleep    6
    Comment    初始化_smart_event
    还原_smart_base
    Comment    还原_smart_event
