*** Settings ***
Library           udstest.py

*** Variables ***
${txid}           0x18DA004A    # 用于传输的CANID
${rxid}           0x18DA4A00    # 用于接收的CANID

*** Keywords ***
UDS_Test
    [Arguments]    ${test_data}
    set_can    ${txid}    ${rxid}    #CAN设置
    ${respond}    Uds Request Respond    ${test_data['request']}    #UDS请求响应
    Should Be Equal    ${test_data['expected']}    ${respond}    #断言
