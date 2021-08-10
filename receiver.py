import socket

# def sckt():
#     server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#     server_socket.bind(('localhost',9999))
#     server_socket.listen(5)
#     k = "Y"
#     while k == "Y":
#         print("server waiting for connection...")
#         clint_socket,adder=server_socket.accept()
#         print("client connected from:",adder)
        
#         while True:
#             data = clint_socket.recv(1024).decode()
#             if not data or data == 'end':
#                 break
#             print(data)
#             try:
#                 sending_data = input()
#                 clint_socket.send(bytes(sending_data,'utf-8'))

#                 if sending_data == "end":
#                     break
#             except:
#                 print("exited by the user")
        
#         clint_socket.close()
#         k=input("do you want to continue(Y/N):")

#     server_socket.close()
lrc_err = 0
vrc_err = 0
crc_err = 0
checksum_err = 0
def lrc(s):
    p = s[len(s) -8 : len(s)]
    s = s[: len(s) -8]
    matrix = []
    start = 0
    end = 8
    while (end <= len(s)):
        matrix.append(s[start : end])
        start = end
        end = end + 8
    
    parity = []
    for j in range(0, 8):
        count = 0
        for i in range(0, len(matrix)):
            if matrix[i][j] == '1':
                count = count + 1
        if count%2 == 0:
            parity.append("0")
        else:
            parity.append("1")
    
    c = 0
    for i in range(0, 8):
        if p[i] != parity[i]:
            c = 1
            print("LRC has detected an error!!\n data rejected!!")
            global lrc_err
            lrc_err += 1
            break;
    if c == 0:
        print("LRC can't detect any error!!\ndata accepted!")
    


def vrc(s):
    p = []
    l = len(s)
    for i in range(8, l):
        if i%8 == 0:
            # print(i)
            p.append(s[i])
            s = s[:i] + s[i+1:]
    # print(s)
    matrix = []
    parity = []
    start = 0
    end = 8
    while (end <= len(s)):
        matrix.append(s[start : end])
        start = end
        end = end + 8
    
    for i in range(0, len(matrix)):
        count = 0
        for j in range(0, 8):
            if matrix[i][j] == "1":
                count = count + 1
        if count % 2 == 0:
            parity.append("0")
        else:
            parity.append("1")

    c = 0
    for i in range(0, len(parity)):
        if p[i] != parity[i]:
            c = 1
            print("VRC has detected an error!!\n data rejected!!")
            global vrc_err
            vrc_err += 1
            break;
    if c == 0:
        print("VRC can't detect any error!!\ndata accepted!")



def checksum(s):
    check = s[len(s) -8 : len(s)]
    s = s[: len(s) -8]
    matrix = []
    start = 0
    end = 8
    while (end <= len(s)):
        matrix.append(s[start : end])
        start = end
        end = end + 8
    
    sum = 0
    for i in range(0, len(matrix)):
        sum += int(matrix[i], 2)
    
    p = bin(sum)
    p = p[2:]
    
    if len(p) > 8:
        p = bin(int(p[len(p) - 8 :], 2) + int(p[: len(p) - 8]))
        p = p[2:]

    if len(p) < 8:
        for i in range(0, 8 - len(p)):
            p = "0" + p
    
    if p == check:
        print("Checksum can't detect any error!!\ndata accepted!")
    else:
        print("Checksum has detected an error!!\n data rejected!!")
        global checksum_err
        checksum_err += 1



def padding(s):
    rem = len(s) % 9
    
    if rem != 0:
        for i in range(0, 9 - rem):
            s = "0" + s
    return s


def xor(s1, s2):
    ret = "0"
    for i in range(1, len(s1)):
        if s1[i] == s2[i]:
            ret += "0"
        else:
            ret += "1"
    
    for i in range(0, len(ret)):
        if ret[i] == "1":
            break
    ret = ret[i:]
    return ret


def crc(s):
    check = s[len(s) -9 : len(s)]
    s = s[: len(s) -9]
    divisor = "110001101"
    s = s + "00000000"
    count = 9
    rem = xor(divisor, s[0 : 9])

    while count < len(s):
        x = len(rem)
        rem += s[count : count + 9-len(rem)]
        if(len(rem) != 9):
            break
        count = count + 9-x
        rem = xor(divisor, rem)
    # rem ="1" +rem+ "0"
    # print("rem = ", rem)
    rem = padding(rem)
    s = s[:len(s)-8]
    if rem == check:
        print("CRC can't detect any error!!\ndata accepted!")
    else:
        print("CRC has detected an error!!\n data rejected!!")
        global crc_err
        crc_err += 1



if __name__ == '__main__':
    # sckt()
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind(('localhost',9999))
    server_socket.listen(5)
    print("server waiting for connection...")
    clint_socket,adder=server_socket.accept()
    print("client connected from:",adder)
    data = clint_socket.recv(1024).decode()
    if data == "1":
        clint_socket.send(bytes("Server know that you have chosen to manually add error method", 'utf-8'))
        data = clint_socket.recv(1024).decode()
        print("Received data from sender: " ,data)
        lrc_s = data[1]
        for i in range(2, len(data)):
            if data[i] == "*":
                break
            lrc_s += data[i]
        lrc(lrc_s)

        vrc_s = data[i+1]
        for j in range(i+2, len(data)):
            if data[j] == "*":
                break
            vrc_s += data[j]
        vrc(vrc_s)

        checksum_s = data[j+1]
        for k in range(j+2, len(data)):
            if data[k] == "*":
                break;
            checksum_s += data[k]
        checksum(checksum_s)

        crc_s = data[k+1]
        for l in range(k+2, len(data)):
            crc_s += data[l]
        crc(crc_s)
    elif data == "2":
        clint_socket.send(bytes("Server know that you have chosen to randomly add error method", 'utf-8'))
        for i in range(0,990):
            data = clint_socket.recv(1024).decode()
            print("Received data from sender: " ,data)
            lrc_s = data[1]
            for i in range(2, len(data)):
                if data[i] == "*":
                    break
                lrc_s += data[i]
            lrc(lrc_s)

            vrc_s = data[i+1]
            for j in range(i+2, len(data)):
                if data[j] == "*":
                    break
                vrc_s += data[j]
            vrc(vrc_s)

            checksum_s = data[j+1]
            for k in range(j+2, len(data)):
                if data[k] == "*":
                    break;
                checksum_s += data[k]
            checksum(checksum_s)

            crc_s = data[k+1]
            for l in range(k+2, len(data)):
                crc_s += data[l]
            crc(crc_s)
            clint_socket.send(bytes("data has been checked", 'utf-8'))
            print("LRC can detect ", lrc_err, " error; VRC can detect ", vrc_err," error; checksum can detect ", checksum_err, " error; CRC can detect ", crc_err, " error")
    # while True:
    #     data1 = clint_socket.recv(1024).decode()
    #     print("Received data from sender: " ,data1)
    #     print("sdhf")
    #     data2 = clint_socket.recv(1024).decode()
    #     print("Received data from sender: " ,data2)
    #     print("lkdjnmgpo")
    #     data3 = clint_socket.recv(1024).decode()
    #     print("Received data from sender: " ,data3)
    #     print("ksjhfoi")
    #     data4 = clint_socket.recv(1024).decode()
    #     print("Received data from sender: " ,data4)
    #     print("kjgowkdrmgmg")
    #     break;

    # print("Received data from sender: " ,data)
    # lrc(data)

    # data = clint_socket.recv(1024).decode()
    # print("Received data from sender: " ,data)

    # data = clint_socket.recv(1024).decode()
    # print("Received data from sender: " ,data)
    # checksum(data)

    # data = clint_socket.recv(1024).decode()
    # print("Received data from sender: " ,data)
    # crc(data)


    clint_socket.close()
    server_socket.close()
    