import time

m=(not(i % 6) for i in range(0,10))
print(list(m))

# print("Waiting for timeout in ", end = " ")
# for i in range(5,0,-1):
#     print(i,end=" ")
#     time.sleep(1)