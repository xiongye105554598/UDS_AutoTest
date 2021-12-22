# _*_ coding:utf-8 _*_

from can.interfaces.pcan.pcan import PcanBus
from udsoncan.connections import PythonIsoTpConnection
import xlrd, os, udsoncan, isotp, sys, binascii


class udstest(object):
    def __init__(self):
        udsoncan.setup_logging()  # udslog

    def get_xlsx(self, sheet):
        "获取指定Excel数据"
        excel = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'UDSTestcase.xlsx')  # 获取用例文件路径
        file = xlrd.open_workbook(excel)
        list = []
        sheet = file.sheet_by_name(sheet)  # 获得指定sheet数据
        row_value1 = sheet.row_values(0)  # 获取第1行的标题
        nrows = sheet.nrows  # 获取当前sheet行数
        ncols = sheet.ncols  # 获取当前sheet列数
        for i in range(1, nrows):  # 从第2行遍历当前sheet
            row = sheet.row_values(i)  # 获取行数据
            dict = {}  # 创建空字典
            for j in range(0, ncols):  # 遍历sheet列，组成字典
                if row_value1[j] == 'NO.':
                    dict[row_value1[j]] = int(row[j])
                else:
                    dict[row_value1[j]] = row[j]  # 从第一列开始，将每一列的数据与第1行的数据组成一个键值对，形成字典
            list.append(dict)  # 将字典添加list中
        return list

    def set_can(self, txid, rxid):
        """can总线相关配置"""
        if isinstance(txid, str) or isinstance(rxid, str):
            txid = eval(txid)
            rxid = eval(rxid)
        isotp_params = {
            'stmin': 5,  # 流控帧间隔时间，0-127ms 或 100-900ns 值从 0xF1-0xF9
            'blocksize': 0,  # 流控帧单包大小，0表示不限制
            'tx_padding': 0,  # 当 notNone表示用于填充发送的消息的字节。
            'rx_flowcontrol_timeout': 1000,  # 在停止接收和触发之前等待流控制帧的毫秒数
            'rx_consecutive_frame_timeout': 1000,  # 在停止接收和触发 a 之前等待连续帧的毫秒数
        }
        try:
            self.canbus = PcanBus(channel='PCAN_USBBUS1', bitrate=500000)  # CAN总线初始化
            self.tp_addr = isotp.Address(isotp.AddressingMode.Normal_29bits, txid=txid, rxid=rxid)  # 网络层寻址方法
            tp_stack = isotp.CanStack(bus=self.canbus, address=self.tp_addr, params=isotp_params)  # 网络/传输层（IsoTP 协议）
            self.conn = PythonIsoTpConnection(tp_stack)  # 应用层和传输层之间建立连接

        except:
            print(sys.exc_info()[1])
        else:
            print('CAN配置成功')

    def uds_request_respond(self, request_command):
        """发送uds请求和接收uds响应"""
        if not isinstance(request_command, str):  # 判断request_command数据类型
            request_command = str(int(request_command))
        requestPdu = binascii.a2b_hex(request_command.replace(' ', ''))  # 处理request_command
        if not self.conn.is_open():
            self.conn.open()  # 打开连接
        try:
            self.conn.specific_send(requestPdu)  # 发送uds请求
        except:
            print("发送请求失败")
        else:
            print('UDS发送请求：%s' % request_command)

        try:
            respPdu = self.conn.specific_wait_frame(timeout=3)  # 接收uds响应
        except:
            print('响应数据失败')
        else:
            res = respPdu.hex().upper()
            respond = ''
            for i in range(len(res)):
                if i % 2 == 0:
                    respond += res[i]
                else:
                    respond += res[i] + ' '
            print('UDS响应结果：%s' % respond)
            self.conn.close()  # 关闭连接
            self.canbus.shutdown()  # 关闭总线
            return respond.strip()

# if __name__ == '__main__':
#     uds = udstest()
#     x=uds.get_xlsx('$10')
#     uds.set_can(txid=0x18DA004A, rxid=0x18DA4A00)
#     m=uds.uds_request_respond('10 40')
