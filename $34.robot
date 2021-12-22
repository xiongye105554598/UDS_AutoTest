*** Settings ***
Suite Setup       获取$34服务测试数据
Resource          Public.robot

*** Test Cases ***
负响应-请求下载
    UDS_Test    ${test_data[0]}

*** Keywords ***
获取$34服务测试数据
    ${test_data}    Get Xlsx    $34
    Set Suite Variable    ${test_data}
