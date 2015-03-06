sentences =  "Athens " "Greece " "Baghdad " "Iraq"

f = open('input', 'w')
for i in range(1,20000):
    f.write(str(sentences) + "\n")
f.close()
