import math
from linearAlgebraFunctions import Vector, dot, vector_sum
from typing import List
from machineLearningFunctions import train_test_split
from matplotlib import pyplot as plt


from typing import Tuple
from scratch.linear_algebra import vector_mean
from scratch.statistics import standard_deviation

def scale(data: List[Vector]) -> Tuple[Vector, Vector]:
    """returns the mean and standard deviation for each position"""
    dim = len(data[0])
    means = vector_mean(data)
    stdevs = [standard_deviation([vector[i] for vector in data])
        for i in range(dim)]
    return means, stdevs

def rescale(data: List[Vector]) -> List[Vector]:
    """
    Rescales the input data so that each position has
    mean 0 and standard deviation 1. (Leaves a position
    as is if its standard deviation is 0.)
    """
    dim = len(data[0])
    means, stdevs = scale(data)
    # Make a copy of each vector
    rescaled = [v[:] for v in data]
    for v in rescaled:
        for i in range(dim):
            if stdevs[i] > 0:
                v[i] = (v[i] - means[i]) / stdevs[i]
    return rescaled

def logistic(x:float):
    return 1.0 / (1 + math.exp(-x))

def logistic_prime(x:float):
    y = logistic(x)
    return y * (1 - y)

def _negative_log_likelihood(x:Vector, y:float, beta:Vector):
    if y == 1:
        return -math.log(logistic(dot(x, beta)))
    else:
        return -math.log(1 - logistic(dot(x(beta))))


def negative_log_likelihood(xs:List[Vector], ys:List[float], beta:Vector):
    return  sum(_negative_log_likelihood(x, y, beta) for x, y in zip(xs, ys))

def _negative_log_partial_j(x:Vector, y:float, beta:Vector, j:int):
    return -(y- logistic(dot(x, beta) * x[j]))

def _negative_log_gradient(x:Vector, y:float, beta:Vector):
    return [_negative_log_partial_j(x,y,beta,j) for j in range(len(beta))]

def negative_log_gradient(xs:List[Vector], ys:List[float], beta:Vector):
    return vector_sum([_negative_log_gradient(x,y,beta) for x,y in zip(xs, ys)])

"""
xs formatted like this:
    
"""

random.seed(0)
x_train, x_test, y_train, y_test = train_test_split(rescaled_xs, ys, 0.33)
learning_rate = 0.01
# pick a random starting point
beta = [random.random() for _ in range(3)]

with tqdm.trange(5000) as t:
    for epoch in t:
        gradient = negative_log_gradient(x_train, y_train, beta)
        beta = gradient_step(beta, gradient, -learning_rate)
        loss = negative_log_likelihood(x_train, y_train, beta)
        t.set_description(f"loss: {loss:.3f} beta: {beta}")