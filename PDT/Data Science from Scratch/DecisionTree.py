from typing import List, Any, NamedTuple, Optional, Dict, TypeVar, Union
from collections import Counter, defaultdict
import math

T = TypeVar('T')

class Candidate(NamedTuple):
    level: str
    lang: str
    tweets: bool
    phd: bool
    did_well: Optional[bool] = None  # allow unlabeled data

def entropy(class_probabilities:List[float]):
    return sum(-p * math.log(p,2) for p in class_probabilities if p > 0)

def class_probabilities(labels: List[Any]):
    total_count = len(labels)
    return [count / total_count for count in Counter(labels).values()]

def data_entropy(labels:List[Any]):
    return entropy(class_probabilities(labels))

def partition_entropy(subsets: List[List[Any]]) -> float:
    """Returns the entropy from this partition of data into subsets"""
    total_count = sum(len(subset) for subset in subsets)
    return sum(data_entropy(subset) * len(subset) / total_count
    for subset in subsets)


def partition_by(inputs: List[T], attribute: str) -> Dict[Any, List[T]]:
    """Partition the inputs into lists based on the specified attribute."""
    partitions: Dict[Any, List[T]] = defaultdict(list)
    for input in inputs:
        key = getattr(input, attribute) # value of the specified attribute
        partitions[key].append(input) # add input to the correct partition
    return partitions

def partition_entropy_by(inputs: List[Any],
attribute: str,label_attribute: str) -> float:
    """Compute the entropy corresponding to the given partition"""
    # partitions consist of our inputs
    partitions = partition_by(inputs, attribute)
    # but partition_entropy needs just the class labels
    labels = [[getattr(input, label_attribute) for input in partition]
              for partition in partitions.values()]
    return partition_entropy(labels)



inputs = [Candidate('Senior', 'Java', False, False, False),
Candidate('Senior', 'Java', False, True, False),
Candidate('Mid', 'Python', False, False, True),
Candidate('Junior', 'Python', False, False, True),
Candidate('Junior', 'R', True, False, True),
Candidate('Junior', 'R', True, True, False),
Candidate('Mid', 'R', True, True, True),
Candidate('Senior', 'Python', False, False, False),
Candidate('Senior', 'R', True, False, True),
Candidate('Junior', 'Python', True, False, True),
Candidate('Senior', 'Python', True, True, True),
Candidate('Mid', 'Python', False, True, True),
Candidate('Mid', 'Java', True, False, True),
Candidate('Junior', 'Python', False, True, False)
]

for key in ['level','lang','tweets','phd']:
    print(key, partition_entropy_by(inputs, key, 'did_well'))

#Now Create the Tree
class Leaf(NamedTuple):
    value:Any

class Split(NamedTuple):
    attribute: str
    subtrees: dict
    default_value: Any = None

DecisionTree = Union[Leaf, Split]

hiring_tree = Split('level', { # first, consider "level"
'Junior': Split('phd', { # if level is "Junior", next look at "phd"
False: Leaf(True), # if "phd" is False, predict True
True: Leaf(False) # if "phd" is True, predict False
}),
'Mid': Leaf(True), # if level is "Mid", just predict True
'Senior': Split('tweets', { # if level is "Senior", look at "tweets"
False: Leaf(False), # if "tweets" is False, predict False
True: Leaf(True) # if "tweets" is True, predict True
})
})

def classify(tree: DecisionTree, input: Any) -> Any:
    """classify the input using the given decision tree"""
    # If this is a leaf node, return its value
    if isinstance(tree, Leaf):
        return tree.value
    # Otherwise this tree consists of an attribute to split on
    # and a dictionary whose keys are values of that attribute
    # and whose values are subtrees to consider next
    subtree_key = getattr(input, tree.attribute)
    if subtree_key not in tree.subtrees: # If no subtree for key,
        return tree.default_value # return the default value.
    subtree = tree.subtrees[subtree_key] # Choose the appropriate subtree
    return classify(subtree, input) # and use it to classify the input.

def build_tree_id3(inputs: List[Any],
    split_attributes: List[str],
    target_attribute: str) -> DecisionTree:

    # Count target labels
    label_counts = Counter(getattr(input, target_attribute)
    for input in inputs)
    most_common_label = label_counts.most_common(1)[0][0]
    # If there's a unique label, predict it
    if len(label_counts) == 1:
        return Leaf(most_common_label)
    # If no split attributes left, return the majority label
    if not split_attributes:
        return Leaf(most_common_label)

    def split_entropy(attribute: str) -> float:
        """Helper function for finding the best attribute"""
        return partition_entropy_by(inputs, attribute, target_attribute)

    best_attribute = min(split_attributes, key=split_entropy)
    partitions = partition_by(inputs, best_attribute)
    new_attributes = [a for a in split_attributes if a != best_attribute]
    # Recursively build the subtrees
    subtrees = {attribute_value : build_tree_id3(subset,
    new_attributes,
    target_attribute)
    for attribute_value, subset in partitions.items()}
    return Split(best_attribute, subtrees, default_value=most_common_label)

tree = build_tree_id3(inputs, ['level', 'lang', 'tweets', 'phd'],
'did_well')

print(classify(tree, Candidate("Junior", "Java", True, False))) #True