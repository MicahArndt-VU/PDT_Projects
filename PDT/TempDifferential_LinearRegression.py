import numpy as np
import random
import matplotlib.pyplot as plt
import tqdm
from typing import List, Tuple
#Create a vector type for processing
Vector = List[float]

#Helper Functions
def add(v:Vector, w:Vector) -> Vector:
    return [v_i + w_i for v_i, w_i in zip(v,w)]

def scalar_multiply(c:float, v:Vector):
    return [c * v_i for v_i in v]

def mean(xs:List[float]):
    return sum(xs)/ len(xs)

def de_mean(xs:List[float]):
    bar = mean(xs)
    return([x - bar for x in xs])

def dot(v:Vector, w:Vector):
    assert (len(v) == len(w)), "Vectors must be equal length"

    return sum(v_i * w_i for v_i, w_i in zip(v,w))
#Sum of Squares of a Vector
def sum_of_squares(v:Vector):
    return dot(v,v)

def variance(xs:List[float]):
    assert len(xs) > 1, "Variance Requires at least two elements"

    n = len(xs)
    deviations = de_mean(xs)
    return sum_of_squares(deviations) / (n - 1)
#Calculate the Standard Deviation- The average amount of variability in a dataset
def standard_deviation(xs:List[float]):
    return math.sqrt(variance(xs))

def correlation(xs:List[float], ys:List[float]):
    stddev_x = standard_deviation(xs)
    stddev_y = standard_deviation(ys)
    if stddev_x > 0 and stddev_y > 0:
        return covariance(xs,ys) / stddev_x / stddev_y
    else:
        return 0


#Now we get functions for gradient descent
def gradient_step(v:Vector, gradient:Vector, step_size:float):
    step = scalar_multiply(step_size, gradient)
    return add(v, step)

#Prediction Function
def predict(alpha: float, beta: float, x_i: float) -> float:
    return beta * x_i + alpha

def error(alpha: float, beta: float, x_i: float, y_i: float) -> float:
    """
    The error from predicting beta * x_i + alpha
    when the actual value is y_i
    """
    return predict(alpha, beta, x_i) - y_i

def sum_of_sqerrors(alpha: float, beta: float, x: Vector, y: Vector) -> float:
    return sum(error(alpha, beta, x_i, y_i) ** 2
        for x_i, y_i in zip(x, y))


def least_squares_fit(x: Vector, y: Vector) -> Tuple[float, float]:
    """
    Given two vectors x and y,
    find the least-squares values of alpha and beta
    """
    beta = correlation(x, y) * standard_deviation(y) / standard_deviation(x)
    alpha = mean(y) - beta * mean(x)
    return alpha, beta

def total_sum_of_squares(y: Vector) -> float:
    """the total squared variation of y_i's from their mean"""
    return sum(v ** 2 for v in de_mean(y))

def r_squared(alpha: float, beta: float, x: Vector, y: Vector) -> float:
    """
    the fraction of variation in y captured by the model, which equals
    1 - the fraction of variation in y not captured by the model
    """
    return 1.0 - (sum_of_sqerrors(alpha, beta, x, y) /
        total_sum_of_squares(y))



interior = [random.randrange(0,100) for i in range(100)]
exterior = [random.randrange(0,100) for i in range(100)]
temp_diff = []
for i in range(100):
    temp_diff.append(np.abs(interior[i] - exterior[i]))
temp_diff = list(set(temp_diff))

cost = [temp_diff[i] * random.uniform(3,7) + random.randint(-temp_diff[i], temp_diff[i]) for i in range(len(temp_diff))]


plt.scatter(temp_diff, cost)
plt.xlabel("Temperature Differential")
plt.ylabel("Cost per Mile")

#Find a function mapping the two values together
#Random alpha Beta guess
guess = [random.uniform(0, 1), random.uniform(0,1)]
#How Fast we want our algorithm to learn - to high and we may overstep our actual value, to small and we will never reach our values
learning_rate = 0.000001

num_epochs = 100000
with tqdm.trange(num_epochs) as t:
    for _ in t:
        #Extract our alpha beta values (Intercept and slope respectively)
        alpha, beta = guess
        #print(alpha, beta)
        #Partial Derivative of loss with respect to alpha
        #What we are trying to minimize for both
        grad_a = sum(2* error(alpha, beta, x_i, y_i) for x_i, y_i in zip(temp_diff, cost))
        grad_b = sum(2 * error(alpha, beta,x_i, y_i) * x_i for x_i, y_i in zip(temp_diff, cost))

        #Our loss value
        loss = sum_of_sqerrors(alpha, beta, temp_diff, cost)
        t.set_description(f"loss: {loss:.3f}")

        #Now, we follow the curve to arrive at our next alpha and beta values
        guess = gradient_step(guess, [grad_a, grad_b], -learning_rate)
        #print(guess)
bf_line_x = [x for x in range(max(temp_diff) + 5)]
bf_line = [guess[1] * x + guess[0] for x in bf_line_x]
plt.plot(bf_line_x, bf_line, '--')
plt.show()

print(f"Formula for our line of best fit: y={guess[1]:.3f}x + {guess[0]}")