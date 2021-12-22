*** Settings ***
Suite Setup       获取$3E服务测试数据
Resource          Public.robot

*** Test Cases ***
正响应-测试在线
    UDS_Test    ${test_data[0]}

*** Keywords ***
获取$3E服务测试数据
    ${test_data}    Get Xlsx    $3E
    Set Suite Variable    ${test_data}
