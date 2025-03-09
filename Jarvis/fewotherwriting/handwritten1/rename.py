import os
a=os.listdir()

for i in range(92,97):
    os.rename(str(i)+'.png',str(i-1)+'.png')