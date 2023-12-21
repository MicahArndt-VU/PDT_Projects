"""
Perceptrons - approximates a single neuron with n binary inputs.
Computes a weighted sum of inputs, then fires if the weighted sum
is greater than the threshhold value (0)
"""

from linearAlgebraFunctions import  Vector, dot, squared_distance
from typing import List
def step_function(x:float):
    return 1.0 if x >= 0 else 0.0

def perceptron_output(weights:Vector, bias:float, x:Vector):
    return step_function(dot(weights, x) + bias)

"""
We can create an and gate with this perceptron. See Below
"""

and_weights = [2., 2.]
and_bias = -3.
"""
print(perceptron_output(and_weights, and_bias, [1,1])) #1 True
print(perceptron_output(and_weights, and_bias, [1,0])) #0 False
print(perceptron_output(and_weights, and_bias, [0,1])) #0 False
print(perceptron_output(and_weights, and_bias, [0,0])) #0 False
"""

import math
#Need a smooth function if we are using more than one neuron, Hence, Sigmoid
def sigmoid(t:float):
    return 1/(1 + math.exp(-t))

#Now we can calculate the neuron output like this:
def neuron_output(weights:Vector, inputs:Vector):
    return sigmoid(dot(weights, inputs))

"""
The above function allows us to represent a neuron as a vector of weights whose
length is more than the number of inputs in to that neuron

This allows us to represent a neural network as a list of noninput layers where each layer is a list of neurons.
ie a list of a list of neurons (Vectors)
"""
def feed_forward(neural_network:List[List[Vector]], input_vector:List[Vector]):
    """
    Feeds the input vector through the neural network.
    returns the outputs of all layers (not just the last one).

    :param neural_network:
    :param input_vector:
    :return:
    """
    outputs: List[Vector] = []
    for layer in neural_network:
        inputs_with_bias = input_vector + [1]
        output =[neuron_output(neuron, inputs_with_bias) for neuron in layer]
        outputs.append(output)
        input_vector = output
    return outputs

#Now, we can build a Neural Network to compute XOR gates that we couldn't with a perceptron
xor_network = [# hidden layer
[[20., 20, -30], # 'and' neuron
[20., 20, -10]], # 'or' neuron
# output layer
[[-60., 60, -30]]] # '2nd input but not 1st input' neuron

#Now, we test
"""
print()
print("Neural Network XOR Gate:")
print("0 XOR 0: ", round(feed_forward(xor_network, [0,0])[-1][0]))
print("0 XOR 1: ", round(feed_forward(xor_network, [0,1])[-1][0]))
print("1 XOR 0: ",round(feed_forward(xor_network, [1,0])[-1][0]))
print("1 XOR 1: ",round(feed_forward(xor_network, [1,1])[-1][0]))
"""


"""
Now we will automate our Neural Network building using a Backpropagation algorithm (Uses Gradient Descent)
"""

def sqerror_gradients(network:List[List[Vector]], input_vector:Vector, target_vector:Vector):
    """
    Given a neural network, an input vector, and a target vector,
make a prediction and compute the gradient of the squared error
loss with respect to the neuron weights.
    :param network:
    :param input_vector:
    :param target_vector:
    :return:
    """
    #Forward Pass
    hidden_outputs, outputs = feed_forward(network, input_vector)
    #Gradients with respect to the output neuron pre-activation targets
    output_deltas = [output * (1 - output) * (output - target) for output, target in zip(outputs, target_vector)]
    #Gradients with respect to output neuron weights
    output_grads = [[output_deltas[i] * hidden_output for hidden_output in hidden_outputs + [1]] for i, output_neuron in enumerate(network[-1])]
    #Gradients with respect to hidden neuron pre-activation outputs
    hidden_deltas = [hidden_output * (1 - hidden_output) * dot(output_deltas, [n[i] for n in network[-1]]) for i, hidden_output in enumerate(hidden_outputs)]
    #Gradients with respect to hidden neuron weights
    hidden_grads = [[hidden_deltas[i] * input for input in input_vector + [1]] for i, hidden_neuron in enumerate(network[0])]
    return [hidden_grads, output_grads]

"""
Now we will try to 'learn' the XOR network we designed by hand above
"""
"""
import random
random.seed(0)

# training data
xs = [[0., 0], [0., 1], [1., 0], [1., 1]]
ys = [[0.], [1.], [1.], [0.]]

#Start with random weights
network = [ # hidden layer: 2 inputs -> 2 outputs
[[random.random() for _ in range(2 + 1)], # 1st hidden neuron
[random.random() for _ in range(2 + 1)]], # 2nd hidden neuron
# output layer: 2 inputs -> 1 output
[[random.random() for _ in range(2 + 1)]] # 1st output neuron
]

from GradientDescent import gradient_step
import tqdm

learning_rate = 1.0
for epoch in tqdm.trange(20000, desc="Neural Net for XOR"):
    for x, y in zip(xs, ys):
        gradients = sqerror_gradients(network, x, y)
        #Take gradient step for each layer
        network = [[gradient_step(neuron, grad, -learning_rate) for neuron, grad in zip(layer, layer_grad)] for layer, layer_grad in zip(network, gradients)]

#Now we test to make sure the network has learned properly
print()
print("Trained Neural Network XOR Gate:")
print("0 XOR 0: ", round(feed_forward(network, [0,0])[-1][0]))
print("0 XOR 1: ", round(feed_forward(network, [0,1])[-1][0]))
print("1 XOR 0: ",round(feed_forward(network, [1,0])[-1][0]))
print("1 XOR 1: ",round(feed_forward(network, [1,1])[-1][0]))

print("Resulting Neural Network Output Layer: ", network[-1])


"""
"""
Practical Problem: Solve the fizzbuzz problem using a neural network
"""
"""

#Create a way to encode numbers into a vector, This generates our Target Vectors
def fizz_buzz_encode(x:int):
    if x % 15 == 0:
        return [0,0,0, 1]
    elif x % 5 == 0:
        return [0,0,1,0]
    elif x % 3 == 0:
        return[0,1,0,0]
    else:
        return [1,0,0,0]

#Now create a way to generate our input vector
def binary_encode(x:int):
    ret = []
    for i in range(10):
        ret.append(x % 2)
        x = x // 2
    return ret

def argmax(xs: list) -> int:
    """"""Returns the index of the largest value""""""
    return max(range(len(xs)), key=lambda i: xs[i])

#Train on data not in our test set (1-100)
xs = [binary_encode(n) for n in range(101, 1024)]
ys = [fizz_buzz_encode(n) for n in range(101, 1024)]

NUM_HIDDEN = 25

fizzbuzz_network = [
# hidden layer: 10 inputs -> NUM_HIDDEN outputs
[[random.random() for _ in range(10 + 1)] for _ in range(NUM_HIDDEN)],
# output_layer: NUM_HIDDEN inputs -> 4 outputs
[[random.random() for _ in range(NUM_HIDDEN + 1)] for _ in range(4)]
]

learning_rate = 1.0
with tqdm.trange(500) as t:
    for epoch in t:
        epoch_loss = 0.0
        for x, y in zip(xs, ys):
            predicted = feed_forward(fizzbuzz_network, x)[-1]
            epoch_loss += squared_distance(predicted, y)
            gradients = sqerror_gradients(fizzbuzz_network, x, y)
            # Take a gradient step for each neuron in each layer
            fizzbuzz_network = [[gradient_step(neuron, grad, -learning_rate)
                    for neuron, grad in zip(layer, layer_grad)]
                for layer, layer_grad in zip(fizzbuzz_network, gradients)]
        t.set_description(f"fizz buzz (loss: {epoch_loss:.2f})")



#Now we can train our set
num_correct = 0

for n in range(1, 101):
    x = binary_encode(n)
    predicted = argmax(feed_forward(fizzbuzz_network, x)[-1])
    actual = argmax(fizz_buzz_encode(n))

    #print(actual)
    labels = [str(n), "fizz", "buzz", "fizzbuzz"]
    print(n, labels[predicted], labels[actual])
    if predicted == actual:
        num_correct += 1

print(num_correct,"/", 100)
"""