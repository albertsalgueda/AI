import matplotlib.pyplot as plt
import random
import numpy as np

#generate sythetic data for linear regression
data = []
for i in range(50):
    x = random.randint(0,9)
    y = random.randint(4,6)
    data.append((x,y))

print(*zip(*data))
plt.scatter(*zip(*data))
#find the optimal model parameters using gradient descent 
# y = wT*x
def mse(n,y):
    mse = 1/n + [(y0-y1)**2 for y0,y1 in y]

def gradient_descent(iterations,learning_rate):
    w=0
    for i in range(iterations):
        w = w - learning_rate*mse()


#plot the line
x = np.linspace(0,10)
y = x + 1
plt.plot(x,y)


#must choose a good learning rate, number of iterations

plt.show()
