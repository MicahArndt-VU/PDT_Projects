from typing import List
from linearAlgebraFunctions import *
import math
#Define function to calculate mean
def mean(xs:List[float]):
    return sum(xs)/ len(xs)
#Calculate the median of a dataset
def median(v:List[float]):
    def _median_odd(v):
        return sorted(xs)[len(xs // 2)]
    def _median_even(v):
        return ((sorted(xs)[(len(xs) // 2) - 1] + sorted(xs)[(len(xs) // 2)]) / 2)
    return _median_even(v) if len(v) % 2 == 0 else _median_odd(v)
#Return a value that a percentage of the data falls under
def quantile(xs:List[float], p:float):
    return sorted(xs)[(int) (p * len(xs))]
#Return the mode of a dataset
def mode(x:List[float]):
    counts = Counter(x)
    max_count = max(counts.value)
    return [x_i for x_i, count in counts.items if count == max_count]
#Return the range of a dataset
def data_range(xs:List[float]):
    return sorted(xs)[-1] - sorted(xs)[0]
#Calculate the deviation mean
def de_mean(xs:List[float]):
    bar = mean(xs)
    return([x - bar for x in xs])
#Return variance- Measurement of the Spread between numbers in a dataset
def variance(xs:List[float]):
    assert len(xs) > 1, "Variance Requires at least two elements"

    n = len(xs)
    deviations = de_mean(xs)
    return sum_of_squares(deviations) / (n - 1)
#Calculate the Standard Deviation- The average amount of variability in a dataset
def standard_deviation(xs:List[float]):
    return math.sqrt(variance(xs))
#Calculate the interquartile range- Range between the first and third quartiles
def interquartile_range(xs:List[float]):
    return quantile(xs, 0.75) - quantile(xs, 0.25)
#Calculate the covariance- Measure of how two variables change together over time
def covariance(xs:List[float], ys:List[float]):
    assert len(xs) == len(ys), "xs and ys must have same number of elements"
    return (dot(de_mean(xs), de_mean(ys)) / (len(xs) - 1))
#Calculate correlation- statistical measure that describes the size and direction of a relationship between two or more variables
def correlation(xs:List[float], ys:List[float]):
    stddev_x = standard_deviation(xs)
    stddev_y = standard_deviation(ys)
    if stddev_x > 0 and stddev_y > 0:
        return covariance(xs,ys) / stddev_x / stddev_y
    else:
        return 0