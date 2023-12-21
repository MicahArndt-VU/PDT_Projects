from linearAlgebraFunctions import  dot, Vector, vector_mean
from GradientDescent import gradient_step
from LinearRegression import total_sum_of_squares
from typing import List
import random
import tqdm


def predict(x:Vector, beta:Vector):
    return dot(x, beta)

def error(x:Vector, y:float, beta:Vector):
    return predict(x, beta) - y

def squared_error(x:Vector, y:float, beta:Vector):
    return error(x,y, beta) ** 2

def sqerror_gradient(x:Vector, y:float, beta:Vector):
    err = error(x,y,beta)
    return [2 * err * x_i for x_i in x]

def least_squares_fit(xs:List[Vector], ys:List[float], learning_rate:float=0.001, num_steps:int = 1000, batch_size:int = 1):
    """Find the beta that minimizes the sum of squared errors
        assuming the model y = dot(x, beta)
    """
    #Start with a random guess
    guess = [random.random() for _ in xs[0]]
    for _ in tqdm.trange(num_steps, desc="least squares fit"):
        for start in range(0, len(xs), batch_size):
            batch_xs = xs[start:start+batch_size]
            batch_ys = ys[start:start+batch_size]

            gradient = vector_mean([sqerror_gradient(x,y,guess) for x,y in zip(batch_xs, batch_ys)])
            print("Gradient: ", gradient)
            guess = gradient_step(guess, gradient, -learning_rate)
            print("Guess: ", guess)
        print(guess)
    return guess

def multiple_r_squared(xs: List[Vector], ys: Vector, beta: Vector) -> float:
    sum_of_squared_errors = sum(error(x, y, beta) ** 2
    for x, y in zip(xs, ys))
    return 1.0 - sum_of_squared_errors / total_sum_of_squares(ys)


random.seed(0)
learning_rate = 0.0001
#Generate a dataset for number of friends
num_friends_good = [random.randrange(1, 50) for x in range(100)]
inputs = []
for i in range(len(num_friends_good)):
    row:Vector = []
    row.append(34)
    row.append(num_friends_good[i])
    row.append(random.randrange(0,8))
    row.append(random.randrange(0,2))
    inputs.append(row)

print("Inputs: ", inputs)
#Generate a dataset based on the above. Base time is roughly 22 minutes, with a relationship coefficient of .9
daily_minutes_good = [0.9 * num_friends_good[x] + 22.43 + random.randrange(-5,5) for x in range(100)]
beta = least_squares_fit(inputs, daily_minutes_good,learning_rate, 5000, 25)

print(multiple_r_squared(inputs, daily_minutes_good, beta))
#print(beta)