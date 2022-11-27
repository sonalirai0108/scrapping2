
def mystery(n):
    v = 0
    for x in range(1, n+1):
        string = ""
        for i in range(1, x+1):
            string += str(x)
        v += int(string)
    return v
v = mystery(4)
print(v)