import os
import time

from linearAlgebraFunctions import Vector
from statisticsFunctions import correlation, standard_deviation, mean, de_mean
from typing import Tuple
import random
import tqdm
from GradientDescent import gradient_step
import matplotlib.pyplot as plt

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

#Now test our a b finder
"""
x = [i for i in range(-100, 110, 10)]
y = [3 * i - 5 for i in x]

print(least_squares_fit(x, y))
"""

#Use Gradient Descent

#Set up iterations of Descent
num_epochs = 10000
#Seed our random data
random.seed()

#Random alpha Beta guess
guess = [random.random(), random.random()]
#How Fast we want our algorithm to learn - to high and we may overstep our actual value, to small and we will never reach our values
learning_rate = 0.00001

#Generate a dataset for number of friends
num_friends_good = [random.randrange(1, 50) for x in range(100)]
#Generate a dataset based on the above. Base time is roughly 22 minutes, with a relationship coefficient of .9
daily_minutes_good = [0.9 * num_friends_good[x] + 22.43 + random.randrange(-20,20) for x in range(100)]
#Now Graph our datasets
plt.scatter(num_friends_good, daily_minutes_good)

#Now begin our linear regression to simply find what a good model would be
with tqdm.trange(num_epochs) as t:
    for _ in t:
        #Extract our alpha beta values (Intercept and slope respectively)
        alpha, beta = guess
        #Partial Derivative of loss with respect to alpha
        #What we are trying to minimize for both
        grad_a = sum(2* error(alpha, beta, x_i, y_i) for x_i, y_i in zip(num_friends_good, daily_minutes_good))
        grad_b = sum(2 * error(alpha, beta,x_i, y_i) * x_i for x_i, y_i in zip(num_friends_good, daily_minutes_good))

        #Our loss value
        loss = sum_of_sqerrors(alpha, beta, num_friends_good, daily_minutes_good)
        t.set_description(f"loss: {loss:.3f}")

        #Now, we follow the curve to arrive at our next alpha and beta values
        guess = gradient_step(guess, [grad_a, grad_b], -learning_rate)
        print(guess)
#create line of best fit
bf_line_x = [x for x in range(50)]
bf_line = [guess[1] * x + guess[0] for x in bf_line_x]
#plt.plot(bf_line_x, bf_line, '--', c='r')
plt.ylim(15,80)
plt.xlim(0,55)
plt.xlabel("Number of Friends")
plt.ylabel("Average Minutes on Site")
plt.title("Effect of Number of Friends on Time Spent on a Social Media Website")
plt.show()

time.sleep(10)

plt.scatter(num_friends_good, daily_minutes_good)
plt.plot(bf_line_x, bf_line, '--', c='r')
plt.ylim(15,80)
plt.xlim(0,55)
plt.xlabel("Number of Friends")
plt.ylabel("Average Minutes on Site")
plt.title("Effect of Number of Friends on Time Spent on a Social Media Website")


plt.show()
#Spit out what formula will give us our best approximation of how much time
#will be spent on a website based on how many friends a person has on that site
print(f"Formula for our line of best fit: y={guess[1]:.3f}x + {guess[0]}")
print(f"Relactionship Coefficient: {correlation(num_friends_good, daily_minutes_good): .3f}")