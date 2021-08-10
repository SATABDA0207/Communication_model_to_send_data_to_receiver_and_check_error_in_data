import random
file1 = open("myfile.txt", "w")
s = ""
list1 = ["0","1"]
for j in range(0,50):
    for i in range(0,64):
        s += random.choice(list1)
    s += "\n"
    file1.write(s)
    # file1.write("\n")

# # file1.write("1010100101111\n")
# file1.close()
# file2 = open("myfile.txt")
# s = file2.readline()
# s = s[:len(s)-1]
# print(s)
# file2.close()
# print(random.randrange(10,20,1))