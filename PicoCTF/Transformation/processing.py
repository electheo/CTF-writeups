encoded_string = "灩捯䍔䙻ㄶ形楴獟楮獴㌴摟潦弸形㝦㘲捡㕽"

flag = []
for char in encoded_string:
    char_val = ord(char)
    for i in range(256):
        if ((char_val - i) / 256) % 1 == 0:
            real_char = int((char_val - i) / 256)
            flag.append(chr(real_char))
            flag.append(chr(i))

print("".join(flag))


"""
processed = ''.join(
    [chr((ord(test[i]) << 8) + ord(test[i + 1])) for i in range(0, len(test), 2)])
"""
