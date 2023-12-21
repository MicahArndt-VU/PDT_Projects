import math
SQRT_TWO_PI = math.sqrt(2 * math.pi)
#Function for uniform probability density function
def uniform_pdf(x):
    return 1 if 0 <= x < 1 else 0

#Calculate uniform cumulative distrabution
def uniform_cdf(x):
    if x < 0: return 0
    elif x < 1: return x
    else: return 1

def normal_pdf(x:float, mu:float = 0, sigma:float = 1):
    return ((math.exp(-(x-mu) ** 2 / 2 / sigma **2)) / SQRT_TWO_PI * sigma)

def normal_cdf(x: float, mu: float = 0, sigma: float = 1) -> float:
    return (1 + math.erf((x - mu) / math.sqrt(2) / sigma)) / 2

def inverse_normal_cdf(p: float,
    mu: float = 0,
    sigma: float = 1,
    tolerance: float = 0.00001) -> float:
    """Find approximate inverse using binary search"""
    # if not standard, compute standard and rescale
    if mu != 0 or sigma != 1:
        return mu + sigma * inverse_normal_cdf(p, tolerance=tolerance)

    low_z = -10.0 # normal_cdf(-10) is (very close to) 0
    hi_z = 10.0 # normal_cdf(10) is (very close to) 1
    while hi_z - low_z > tolerance:
        mid_z = (low_z + hi_z) / 2  # Consider the midpoint
    mid_p = normal_cdf(mid_z)  # and the CDF's value there
    if mid_p < p:
        low_z = mid_z  # Midpoint too low, search above it
    else:
        hi_z = mid_z  # Midpoint too high, search below it
    return mid_z

def bernoulli_trial(p: float) -> int:
    """Returns 1 with probability p and 0 with probability 1-p"""
    return 1 if random.random() < p else 0
def binomial(n: int, p: float) -> int:
    """Returns the sum of n bernoulli(p) trials"""
    return sum(bernoulli_trial(p) for _ in range(n))