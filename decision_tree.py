from math import log2, inf
import matplotlib.pyplot as plt

class Node:
    def __init__(self, attribute):
        """
        Create a node
        Attributes:
        left: left child of this node
        right: right child of this node
        attribute: the attribute that this node represents
        threshold: the threshold used for that attribute
        """
        
        self.left = None
        self.right = None
        self.attribute = attribute
        self.threshold = gain[attribute][1]

def target_entropy():
    """
    Find the entropy when splitting on the age attribute
    """
    
    counts = {
        'age_under_18': 0,
        'age_18_30': 0,
        'age_30_40': 0,
        'age_40_50': 0,
        'age_50_60': 0,
        'age_over_60': 0
    }
    
    # count how many of each attribute there are
    for x in training_data:
        counts[training_data[x][-1]] += 1
    
    # calculate and return the entropy
    count = sum([counts[x] for x in counts])
    total = 0
    for age in counts:
        total -= (counts[age]/count)*log2(counts[age]/count)
        
    return total

def split(field, threshold, subset):
    """
    Split a subset of the data, using a specific field on a threshold
    """
    left = 0
    right = 0
    field_index = fields.index(field)
    
    # go through each data item and split it to the left if it is less or equal to 
    # than the threshold and to the right if it is greater than it
    for x in subset:
        if training_data[x][field_index-1] <= threshold:
            left += 1
        else:
            right += 1
    if left == 0 or right == 0:
        return inf
    # return the entropy of the split
    return -(left*log2(left/(left+right))+right*log2(right/(left+right)))/(left+right)
    
def entropy(field, threshold):
    """
    Calculate the total entropy of the data by splitting it on all attributes
    """
    total_count = 0
    for subset in data:
        total_count += len(data[subset])
    total = 0
    for subset in data:
        total += len(data[subset])/total_count*split(field, threshold, data[subset])
    return total

def information_gain(field, threshold, target):
    """
    Return the information gain of the data
    """
    return target-entropy(field, threshold)


def find_best_attribute(depth, attributes):
    """
    Find the 'depth'th best attribute
    e.g. if depth = 2, find the 2nd best attribute
    """
    gains = [(field, gain[field][0]) for field in attributes]
    gains = sorted(gains, key=lambda x: x[1])
    return gains[depth-1]

def age_mode(examples):
    """
    Find the the most common age in a set of data
    """
    
    counts = {
        'age_under_18': 0,
        'age_18_30': 0,
        'age_30_40': 0,
        'age_40_50': 0,
        'age_50_60': 0,
        'age_over_60': 0
    }
    
    for example in examples:
        counts[example[-1]] += 1
        
    best_value = 0
    best = ""
    for count in counts:
        if counts[count] > best_value:
            best_value = counts[count]
            best = count
            
    return best

def split_data(examples, best):
    """
    Split the data on a given attribute 'best'
    """
    
    left = []
    right = []
    
    threshold = gain[best][1]
    index = fields.index(best)-1
    
    # if x is less than the threshold, go left, otherwise right
    for x in examples:
        if float(x[index]) <= float(threshold):
            left.append(x)
        else:
            right.append(x)
    
    return left, right
    
def dtl(examples, attributes, default, depth):
    """
    Create a decision tree on the data
    """
    
    # if the depth is 0, there are no more examples, no more attributes
    # or all of the examples are the same age, return the most common age
    if depth == 0:
        return age_mode(examples)
    if len(examples) == 0:
        return default
    if len(attributes) == 0:
        return age_mode(examples)
    if len(set([example[-1] for example in examples])) == 0:
        return examples[0][-1]
    else:
        # otherwise split the data left and right on the next best attribute,
        # and branch the decision tree
        best = find_best_attribute(len(attributes), attributes)[0]
        node = Node(best)
        left, right = split_data(examples, best)
        attributes.remove(best)
        if len(left) == 0:
            node.left = default
        else:
            node.left = dtl(left, attributes, age_mode(left), depth-1)
        if len(right) == 0:
            node.right == default
        else:
            node.right = dtl(right, attributes, age_mode(right), depth-1)
        
    return node
        
        
    
# unpack the data
file = open("data.csv", "r")
data_raw = file.readlines()

fields = []
for field in data_raw[0].split(","):
    fields.append(field)
fields[-1] = fields[-1].rstrip("\n")

# create the training data with 3/4 of the data
data_raw = data_raw[1:]
training_data = {}

for entry in data_raw[:int(3*len(data_raw)/4)]:
    entry=entry.rstrip("\n").split(",")
    training_data[entry[0]] = entry[1:]
    
# split the data on age    
data = {
        'age_under_18': [],
        'age_18_30': [],
        'age_30_40': [],
        'age_40_50': [],
        'age_50_60': [],
        'age_over_60': []
}
for x in training_data:
    data[training_data[x][-1]].append(x)
 
# find the maximum information gain for each attribute
gain = {}
for field in fields[1:-1]:
    gain[field] = [0,0]
    
target = target_entropy()
for x in training_data:
    for y in range(len(training_data[x])-1):
        if training_data[x][y] == 0:
            continue
        ig = information_gain(fields[y+1], training_data[x][y], target)
        if gain[fields[y+1]][0] < ig:
            gain[fields[y+1]][0] = ig
            gain[fields[y+1]][1] = training_data[x][y]
            
# calculate the accuracy with varying depth
examples = [training_data[key] for key in training_data]    
accuracies = []

for i in range(len(fields[1:-1])):  
    root = dtl(examples, fields[1:-1], None, i)

    total = 0
    correct = 0

    # try to classify each point, and check the proprtion which the tree got correct
    test_keys = [key for key in training_data.keys()][int(3*len(training_data)/4):]
    for x in test_keys:
        answer = training_data[x][-1]
        current = root
        while type(current) != str:
            if current == None:
                break
            field_index = fields.index(current.attribute)-1
            if training_data[x][field_index] <= current.threshold:
                current = current.left
            else:
                current = current.right
        total += 1
        if current == answer:
            correct += 1

    accuracies.append(correct/total)
    
# show the graph of accuracies
plt.scatter(range(1,len(fields[1:-1]),2), accuracies[1::2])
plt.xlabel("Depth")
plt.ylabel("Accuracy")
plt.show()

