# turns base36 to decimal
def t2d(value):
    dec = 0
    value = value.upper()
    l = list(value)
    l.reverse()
    for i in range(len(l)):
        try:
            dec += int(l[i])*36**i
        except:
            valu = ord(l[i])-55
            print(valu)
            dec = dec + valu*36**i
    return dec

# turns decimal to base 32
def d2t(val):
    hex_digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    hex_value = ""

    while val > 0:
        remainder = val % 36
        hex_value = hex_digits[remainder] + hex_value
        val //= 36
    return "{:0>3}".format(hex_value)



# for i in hex_digits:
#     print("{:0>3}".format(i+i))