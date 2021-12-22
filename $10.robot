*** Settings ***
Suite Setup       获取$10服务测试数据
Test Setup
Test Teardown
Resource          Public.robot

*** Test Cases ***
正响应-启动车载信息会话
    UDS_Test    ${test_data[0]}
    sleep    10

负响应-不支持请求服务子功能
    UDS_Test    ${test_data[1]}

负响应-请求报文数据长度不符合标准
    UDS_Test    ${test_data[2]}

*** Keywords ***
获取$10服务测试数据
    ${test_data}    Get Xlsx    $10
    Set Suite Variable    ${test_data}
