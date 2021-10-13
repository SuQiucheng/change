import decimal
import os

# 两个数据包的总大小
packetAllBytes = 512
# 第一个数据包的总大小
firstPacketBytes = 81
# 第一个数据包开头的几个字节的数据
firstStart = 8
# 开始有8个字节，16个通道，64个字节的数据
firstEnd = 64+8
# 第二个数据包的开头的几个字节的数据
secondStart = 8
# 开始有8个字节，16个通道，64个字节的数据
secondEnd = 64+8
# 16进制数据转为10进制后，需要除以的数字
dividedNumber = 24
# 16路，每一路4个字节，即32位
width = 32  # 16进制数所占位数，将16进制的数字转换的时候需要用到


class Change:
    def changeOneFile(self, fileName):
        fn = os.path.basename(fileName)
        # 除去文件名之后的路径名，因为需要修改文件名，所以需要先提取出来
        excludeFn = fileName[0:(len(fileName)-len(fn))]
        # 文件名修改
        fn = "processed_"+fn
        # 得到新修改的文件的完整路径
        fn = excludeFn+fn
        with open(fileName, 'rb') as f:
            with open(fn,'w') as f1:
                seek = 0
                while True:
                    f.seek(seek)
                    packet = f.read(packetAllBytes)
                    if(len(packet)<packetAllBytes):
                        break
                    seek += len(packet)

                    result = self.processPacket(packet)
                    for i in range(len(result[0])):
                        f1.write(str(result[0][i]))
                        f1.write(' ')
                    for i in range(len(result[1])):
                        f1.write(str(result[1][i]))
                        f1.write(' ')


    # 处理两个数据包512个字节
    # packet是字节流数组
    def processPacket(self,packet):
        # 因为是字节流数组，所以先解码
        packet = packet.decode()

        packetNew = []
        temp = ''
        # 解码之后，数组里是单个的字符，需要整合为字符串数组
        for i in range(len(packet)):
            if (packet[i] == ' '):
                packetNew.append(temp)
                temp = ''
            else:
                temp += packet[i]

        packet = packetNew
        firstResult = self.processFirstPacket(packet[0:firstPacketBytes])
        secondResult = self.processSecondPacket(packet[firstPacketBytes:len(packet)])

        return firstResult,secondResult



    # packet应该为字符数组
    def processFirstPacket(self, packet):
        result = []
        for i in range(0, firstEnd, 4):
            hexNumStrs = ""
            if i < firstStart:
                continue
            if(i+3>=len(packet)):
                break
            hexNumStrs = hexNumStrs + packet[i+3]+packet[i+2]+packet[i+1]+packet[i]

            # decimalNum = int(hexNumStrs, 16)
            decimalNum = self.hexToInt(hexNumStrs)
            # 数据除以24，同时保留2为小数
            decimalNum = decimalNum / dividedNumber
            decimalNum = decimal.Decimal(decimalNum).quantize(decimal.Decimal("0.00"), rounding="ROUND_HALF_UP")
            result.append(decimalNum)
        return result
    def processSecondPacket(self,packet):
        result = []
        for i in range(0,secondEnd,4):
            hexNumStrs = ""
            if i<secondStart:
                continue
            if 's' in packet[i]:
                break
            if(i+3>=len(packet)):
                break
            hexNumStrs = hexNumStrs + packet[i+3]+packet[i+2]+packet[i+1]+packet[i]

            # decimalNum = int(hexNumStrs, 16)
            decimalNum = self.hexToInt(hexNumStrs)
            decimalNum = decimalNum / dividedNumber
            decimalNum = decimal.Decimal(decimalNum).quantize(decimal.Decimal("0.00"), rounding="ROUND_HALF_UP")
            result.append(decimalNum)
        return result
    def hexToInt(self,data):
        dec_data = int(data, 16)
        if dec_data > 2 ** (width - 1) - 1:
            dec_data = 2 ** width - dec_data
            dec_data = 0 - dec_data
        return dec_data


if __name__ == '__main__':
    change = Change()
    fileName = "/Users/suqiucheng/Code/change/QHU_EEG_DATA.txt"
    change.changeOneFile(fileName)

