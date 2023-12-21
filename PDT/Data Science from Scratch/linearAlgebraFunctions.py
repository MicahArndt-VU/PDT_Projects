from typing import List, Tuple, Callable
import math
#Establish Vector Type
Vector = List[float]

"""
Collection of Vector Functions that will be heavily used throughout the Data Science Book
"""
#Add Vector Function
def add(v:Vector, w:Vector) -> Vector:
    return [v_i + w_i for v_i, w_i in zip(v,w)]
#Vector Sum Function
def vector_sum(v:List[Vector]):
    num_elements = len(v[0])
    #assert all(len(v) == num_elements for vec in v), "Different Sizes"
    return [sum(vec[i] for vec in v) for i in range(num_elements)]
#Subtract Vector Function
def subtract(v:Vector, w:Vector):
    return [v_i - w_i for v_i, w_i in zip(v,w)]
#Scalar Multiplication on a vector
def scalar_multiply(c:float, v:Vector):
    return [c * v_i for v_i in v]
#Vector Mean Function
def vector_mean(vectors:List[Vector]):
    n = len(vectors)
    return scalar_multiply((1/n),vector_sum(vectors))
#DotProd
def dot(v:Vector, w:Vector):
    #assert(len(v) == len(w)), "Vectors must be equal length"
    #print(len(w), len(v))
    #print(w, '\n',v)
    assert (len(v) == len(w)), "Vectors must be equal length"

    return sum(v_i * w_i for v_i, w_i in zip(v,w))
#Sum of Squares of a Vector
def sum_of_squares(v:Vector):
    return dot(v,v)
#Magnitude of a vector
def magnitude(vector:Vector):
    return math.sqrt(sum_of_squares(vector))
#Distance Function
def distance(v:Vector, w:Vector):
    return magnitude(subtract(v,w))

def squared_distance(v: Vector, w: Vector) -> float:
    """Computes (v_1 - w_1) ** 2 + ... + (v_n - w_n) ** 2"""
    return sum_of_squares(subtract(v, w))

"""
Matrix Functions and Definitions that will be used later.
"""
#Establish Matrix type
Matrix = List[List[float]]

#Take Matrix and return (rows, cols)
def shape(A:Matrix):
    return (len(A), len(A[0]) if A else 0)
def get_row(A:Matrix, i:int):
    return A[i]
def get_col(A:Matrix, j:int):
    return [A_i[j] for A_i in A]
#Now we want a function for generating a matrix
def make_matrix(num_rows: int, num_cols:int, entry_fn: Callable[[int, int],float]):
    return[[entry_fn(i,j) for j in range(num_cols)]for i in range(num_rows)]
#Generate an Identity Matrix of a given size
def identity_matrix(i):
    return make_matrix(n, n, lambda i,j: 1 if i==j else 0)
