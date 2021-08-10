import socket
import random


# e = random.randrange(0,63)
# mul = random.randrange(2,63)
# randomlist = []
# for i in range(0,mul):
#     z = random.randrange(0,63)
#     randomlist.append(z)

def send(s):
    try:
        clint_socket.send(bytes(s,'utf-8'))
        print("Data has been sent successfuly!!\nThe data which has been sent is : " + s)
    except KeyboardInterrupt:
        print("exited by user")
    


def padding(s):
    rem = len(s) % 9
    
    if rem != 0:
        for i in range(0, 9 - rem):
            s = "0" + s
    return s



def lrc(s):
    print("Data will be send after applying lrc!! just wait!!....")
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
    k = input("do you want to add error(y/n): ")
    cer = "y"
    if(k == "y"):
        cer = input("Do you want to add error in checkbits(y/n): ")
        if(cer == "n"):
            s = input("Enter the errored data: ")
            # s = padding(s)
    # print("love u")
    # if k == "n" or cer == "n":
    for i in range(0, len(parity)):
        s = s + parity[i]
    if(k == "y" and cer == "y"):
        print("the correct data with  checkbits is: ", s)
        s = input("Enter the errored data with checkbits: ")
    return s


def lrc_random(s, sm,e,randomlist):
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
    # e = random.randrange(0,63)
    if sm == "1":
        el = s[e:e+1]
        if(el == "0"):
            el = "1"
        else:
            el = "0"
        s = s[:e] + el + s[e+1:]

    if sm == "2":
        for i in range(0,len(randomlist)):
            el = randomlist[i]
            el = s[i:i+1]
            if(el == "0"):
                el = "1"
            else:
                el = "0"
            s = s[:i] + el + s[i+1:]

    for i in range(0, len(parity)):
        s = s + parity[i]
    return s
    


def vrc(s):
    print("Data will be send after applying vrc!! just wait!!....")
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

    k = input("do you want to add error(y/n): ")
    cer = "y"
    if(k == "y"):
        cer = input("Do you want to add error in checkbits(y/n): ")
        if(cer == "n"):
            s = input("Enter the errored data: ")
            # s = padding(s)
    
    start = 8
    # if k == "n" or cer == "n":
    for i in range(0,len(parity)):
        s = s[:start] + parity[i] + s[start:]
        start = start + 9
    if(k == "y" and cer == "y"):
        print("the correct data with  checkbits is: ", s)
        s = input("Enter the errored data with checkbits: ")
    return s


def vrc_random(s, sm,e,randomlist):
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
    # e = random.randrange(0,63)
    if sm == "1":
        el = s[e:e+1]
        if(el == "0"):
            el = "1"
        else:
            el = "0"
        s = s[:e] + el + s[e+1:]
    if sm =="2":
        for i in range(0,len(randomlist)):
            el = randomlist[i]
            el = s[i:i+1]
            if(el == "0"):
                el = "1"
            else:
                el = "0"
            s = s[:i] + el + s[i+1:]
    start = 8
    for i in range(0,len(parity)):
        s = s[:start] + parity[i] + s[start:]
        start = start + 9

    return s



def checksum(s):
    print("Data will be send after applying checksum!! just wait!!....")
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
    k = input("do you want to add error(y/n): ")
    cer = "y"
    if(k == "y"):
        cer = input("Do you want to add error in checkbits(y/n): ")
        if(cer == "n"):
            s = input("Enter the errored data: ")
            # s = padding(s)
    # if k == "n" or cer == "n":
    s = s + p
    if(k == "y" and cer == "y"):
        print("the correct data with  checkbits is: ", s)
        s = input("Enter the errored data with checkbits: ")
    return s


def checksum_random(s,sm,e,randomlist):
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
    # e = random.randrange(0,63)
    if sm =="1":
        el = s[e:e+1]
        if(el == "0"):
            el = "1"
        else:
            el = "0"
        s = s[:e] + el + s[e+1:]
    if sm =="2":
        for i in range(0,len(randomlist)):
            el = randomlist[i]
            el = s[i:i+1]
            if(el == "0"):
                el = "1"
            else:
                el = "0"
            s = s[:i] + el + s[i+1:]
    s = s + p
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
    print("Data will be send after applying crc!! just wait!!....")
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

    rem = padding(rem)
    s = s[:len(s)-8]
    k = input("do you want to add error?(y/n): ")
    cer = "y"
    if(k == "y"):
        cer = input("Do you want to add error in checkbits(y/n): ")
        if(cer == "n"):
            s = input("Enter the errored data: ")
    # if k == "n" or cer == "n":
    s += rem
    if(k == "y" and cer == "y"):
        print("the correct data with  checkbits is: ", s)
        s = input("Enter the errored data with checkbits: ")
    return s


def crc_random(s, sm,e,randomlist):
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

    rem = padding(rem)
    s = s[:len(s)-8]
    # e = random.randrange(0,63)
    if sm =="1":
        el = s[e:e+1]
        if(el == "0"):
            el = "1"
        else:
            el = "0"
        s = s[:e] + el + s[e+1:]
    if sm =="2":
        for i in range(0,len(randomlist)):
            el = randomlist[i]
            el = s[i:i+1]
            if(el == "0"):
                el = "1"
            else:
                el = "0"
            s = s[:i] + el + s[i+1:]
    s += rem
    return s



if __name__ == '__main__':
    c = input("Enter what you want to do:\n1. To enter the data manually\n2. To enter the data Randomly\nEnter your choice: ")
    clint_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clint_socket.connect(('localhost',9999))
    send(c)
    recv_data = clint_socket.recv(1024).decode()
    print(recv_data)
    if(c == "1"):
        file = open("input.txt", "r")
        print("Reading data from file input.txt!!")

        s = file.read()
        print("The data in the file is: ", s)
        # s = padding(s)
        sending = "*" + lrc(s)
        sending += "*" + vrc(s)
        sending += "*" + checksum(s)
        sending += "*" + crc(s)
        send(sending)   
        clint_socket.close()

    elif c == "2":
        sm = input("1. To add single bit error\n2. To add multiple bit error\nEnter your choice: ")
        file1 = open("myfile.txt", "w")
        s = ""
        list1 = ["0","1"]
        for j in range(0,44):
            for i in range(0,64):
                s += random.choice(list1)
            s += "\n"
            file1.write(s)

        file1.close()
        file2 = open("myfile.txt")
        for i in range(0,990):
            e = random.randrange(0,63)
            mul = random.randrange(2,63)
            randomlist = []
            for j in range(0,mul):
                z = random.randrange(0,63)
                randomlist.append(z)
            s = file2.readline()
            s = s[:len(s)-1]
            print(s)
            sending = "*" + lrc_random(s,sm,e,randomlist)
            sending += "*" + vrc_random(s,sm,e,randomlist)
            sending += "*" + checksum_random(s,sm,e,randomlist)
            sending += "*" + crc_random(s,sm,e,randomlist)
            clint_socket.send(bytes(sending,'utf-8'))
            data = clint_socket.recv(1024).decode()
            print("data which has been sent is: ",data)
        file2.close()
        clint_socket.close()
            

    else:
        print("you have entered a wrong choice!!\n")