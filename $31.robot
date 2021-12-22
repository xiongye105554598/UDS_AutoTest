*** Settings ***
Suite Setup       获取$31服务测试数据
Resource          Public.robot

*** Test Cases ***
负相应-当前会话不支持服务
    UDS_Test    ${test_data[0]}

负相应-安全访问被拒绝
    set_can    ${txid}    ${rxid}
    Uds Request Respond    10 40    #进入车载会话模式
    UDS_Test    ${test_data[1]}

*** Keywords ***
获取$31服务测试数据
    ${test_data}    Get Xlsx    $31
    Set Suite Variable    ${test_data}
