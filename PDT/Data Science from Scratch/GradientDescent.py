from typing import Callable, TypeVar, List, Iterator
from linearAlgebraFunctions import Vector, distance,add, scalar_multiply, vector_mean
import random

T = TypeVar('T') #Allows for generic Functions

def difference_quotient(f:Callable[[float], float], x:float, h:float):
    return (f(x+h) - f(x))/ h

def partial_difference_quotient(f:Callable[[Vector], float], v:Vector, i:int, h:float):
    """Returns the i-th partial difference quotient of f at v"""
    w = [v_j + (h if j == i else 0) for j, v_j in enumerate(v)]
    return (f(w) - f(v)) / h

def estimate_gradient(f:Callable[[Vector], float], v:Vector, h:float = 0.0001):
    return [partial_difference_quotient(f, v, i, h) for i in range(len(v))]


def gradient_step(v:Vector, gradient:Vector, step_size:float):
    step = scalar_multiply(step_size, gradient)
    return add(v, step)

def sum_of_squares_gradient(v:Vector):
    return [2 * v_i for v_i in v]

def linear_gradient(x:float, y:float, theta:Vector):
    slope, intercept = theta
    predicted = slope * x + intercept
    error = predicted - y
    squared_error = error ** 2
    grad = [2* error * x, 2 * error]
    return grad

def minibatches(dataset: List[T], batch_size: int, shuffle:bool = True):
    """Generates batch size - sized mini batches from the dataset"""
    batch_starts = [start for start in range(0, len(dataset), batch_size)]
    if shuffle: random.shuffle(batch_starts)

    for start in batch_starts:
        end = start + batch_size
        yield dataset[start:end]

"""Example on page 101"""
"""
inputs = [(x, 20 * x + 5) for x in range(-50, 50)]
#start with random values for slope and intercept
theta = [random.uniform(-1,1), random.uniform(-1,1)]
learning_rate = 0.001

for epoch in range(5000):
    #Compute mean of gradients
    grad = vector_mean([linear_gradient(x,y,theta) for x, y in inputs])
    #take a step in that direction
    theta = gradient_step(theta, grad, -learning_rate)
    print(epoch, theta)

#Slope = ~20, intercept = ~5
print(theta) 
"""


"""Re-worked example on page 102 - Called Minibatch gradient descent"""
inputs = [(x, 20 * x + 5) for x in range(-50, 50)]
learning_rate = 0.001
theta = [random.uniform(-1,1), random.uniform(-1, 1)]
for epoch in range(1000):
    for batch in minibatches(inputs, batch_size=20):
        grad = vector_mean([linear_gradient(x,y,theta) for x,y in batch])
        theta = gradient_step(theta, grad, -learning_rate)
    print(epoch, theta)
#Slope = ~20, intercept = ~5
print(theta)

"""Final re-worked example: Stochastic Gradient Descent"""
inputs = [(x, 20 * x + 5) for x in range(-50, 50)]
learning_rate = 0.001
theta = [random.uniform(-1,1), random.uniform(-1, 1)]
for epoch in range(100):
    for x, y in inputs:
        grad = linear_gradient(x, y, theta)
        theta = gradient_step(theta, grad, -learning_rate)
    print(epoch, theta)
#Slope = ~20, intercept = ~5
print(theta)
