*** Settings ***
Suite Setup       获取$22服务测试数据
Resource          Public.robot

*** Test Cases ***
正响应-读取设备ID
    UDS_Test    ${test_data[0]}

正响应-读取ECM缓存内存重启地址
    UDS_Test    ${test_data[1]}

正响应-读取ECM缓存内存字节接收数
    UDS_Test    ${test_data[2]}

负响应-请求超出范围
    UDS_Test    ${test_data[3]}

*** Keywords ***
获取$22服务测试数据
    ${test_data}    Get Xlsx    $22
    Set Suite Variable    ${test_data}
