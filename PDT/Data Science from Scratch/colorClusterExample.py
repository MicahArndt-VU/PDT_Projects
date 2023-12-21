import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from linearAlgebraFunctions import  Vector, vector_mean, squared_distance
from typing import List
import itertools
import random
import tqdm

def num_differences(v1: Vector, v2: Vector) -> int:
    assert len(v1) == len(v2)
    return len([x1 for x1, x2 in zip(v1, v2) if x1 != x2])

class KMeans:
    def __init__(self, k: int) -> None:
        self.k = k # number of clusters
        self.means = None
    def classify(self, input: Vector) -> int:
        """return the index of the cluster closest to the input"""
        return min(range(self.k),
                   key=lambda i: squared_distance(input, self.means[i]))
    def train(self, inputs: List[Vector]) -> None:
        # Start with random assignments
        assignments = [random.randrange(self.k) for _ in inputs]
        with tqdm.tqdm(itertools.count()) as t:
            for _ in t:
                # Compute means and find new assignments
                self.means = cluster_means(self.k, inputs, assignments)
                new_assignments = [self.classify(input) for input in inputs]
                # Check how many assignments changed and if we're done
                num_changed = num_differences(assignments, new_assignments)
                if num_changed == 0:
                    return
                # Otherwise keep the new assignments, and compute new means
                assignments = new_assignments
                self.means = cluster_means(self.k, inputs, assignments)
                t.set_description(f"changed: {num_changed} / {len(inputs)}")

def cluster_means(k: int,
    inputs: List[Vector],
    assignments: List[int]) -> List[Vector]:
    # clusters[i] contains the inputs whose assignment is i
    clusters = [[] for i in range(k)]
    for input, assignment in zip(inputs, assignments):
        clusters[assignment].append(input)
    # if a cluster is empty, just use a random point
    return [vector_mean(cluster) if cluster else random.choice(inputs)
        for cluster in clusters]

#Input Image path here
image_path = r"C:\Users\micah.arndt\Downloads\pumpkin.jpg"


img = mpimg.imread(image_path) / 256
plt.imshow(img)
plt.axis('off')
plt.show()
#Demonstration
top_row = img[0]
top_left_pixel = top_row[0]
r,g,b = top_left_pixel


pixels =[pixel.tolist() for row in img for pixel in row]

clusterer = KMeans(16)
clusterer.train(pixels)

def recolor(pixel:Vector):
    cluster = clusterer.classify(pixel)
    return clusterer.means[cluster]

new_img = [[recolor(pixel) for pixel in row]for row in img]

plt.imshow(new_img)
plt.axis('off')
plt.show()

path = r"C:\Users\micah.arndt\Documents\TestImages\derpyBash.jpg"
img = mpimg.imread(path) / 256
pixels = [pixel.tolist() for row in img for pixel in row]
new_img = [[recolor(pixel) for pixel in row]for row in img]
plt.imshow(new_img)
plt.axis('off')
plt.show()