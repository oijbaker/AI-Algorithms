from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from random import randint
from math import sqrt, inf
import numpy as np
import matplotlib.pyplot as plt

def distance(a, b):
    """
    Return the distance between two vectors
    Parameters:
    a, b: n-dimensional vectors
    """
    return np.linalg.norm(b-a)

def average(a):
    """
    Return the average of a set of vectors
    Paramaters:
    a: list of n-dimensional vectors
    """
    count = len(a)
    n = len(a[0])
    
    sum_ = [0 for i in range(n)]
    
    for x in a:
        for i in range(n):
            sum_[i] += x[i]
    
    for i in range(n):
        sum_[i] /= count
    return sum_

def k_means(data, k, n):
    """
    The k-means clustering algorithm
    Parameters:
    data: the data to be analysed
    k: the number of clusters
    n: the number of iterations
    """
    # initialise a result dictionary
    result = {}
    
    # initialise k centroids
    for i in range(k):
        if centroid_type == "random":
            result[i] = [[randint(0,16) for j in range(64)], []]
        else:
            result[i] = [data[i], []]
    for i in range(n):
        # assign the data points to the closest cluster
        for x in data:
            distances = [distance(result[a][0], x) for  a in range(k)]
            minimum_index = distances.index(min(distances))
            result[minimum_index][1].append(x)
        # set the centroids to be the mean of the vectors assigned to it
        for cluster in result.keys():
            if len(result[cluster][1]) == 0:
                centroid = [randint(0,16) for i in range(64)]
                continue
            centroid = average(result[cluster][1])
            result[cluster][0] = centroid
    return result

def display_digit(digit):
    """
    graphically displays a 784x1 vector, representing a digit
    """
    image = digit
    plt.figure()
    fig = plt.imshow(image.reshape(8,8))
    fig.set_cmap('gray_r')
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.show()
    
def assign(point, digit_labels):
    """
    assign a point to a cluster
    """
    min_distance = inf
    best_digit = None
    
    for digit in digit_labels:
        new_distance = distance(point, digit_labels[digit])
        if new_distance < min_distance:
            min_distance = new_distance
            best_digit = digit
    return best_digit

def accuracy(frac):
    """
    calculate the accuracy of the k-means algorithm
    """
    
    digit_clusters = {}
    
    for i in range(10):
        result_labels = [labels[digits.data.tolist().index(list(result[i][1][n]))] for n in range(len(result[i][1]))]
        try:
            digit_clusters[max(set(result_labels), key=result_labels.count)] = result[i][0]
        except:
            for i in range(10):
                if i not in digit_clusters:
                    digit_clusters[i] = result[i][0]
                    break
    
    correct = 0
    total = 0
    for digit in digits.data[int(frac*len(digits.data)):]:
        guess = assign(digit, digit_clusters)
        if guess == labels[digits.data.tolist().index(list(digit))]:
            correct += 1
        total += 1
        
    return correct/total
    
    
# get the digits, and use 3/4 of them as training data for the k-means algorithm
digits = load_digits(return_X_y=False)
_, labels = load_digits(return_X_y=True)

# set to "random" for initial centroids to be random
centroid_type = "random"

# set to "centroids" to show the centroids, "clusters" to show clusters, or "accuracy" to show accuracy
display = "accuracy"

if display == "clusters":
    # display the clusters
    result = k_means(digits.data, 10, 30)
    
    centroids = [result[i][0] for i in range(10)]
    embedding = PCA(n_components=2)
    transformed = embedding.fit_transform(digits.data)
    centroids_transform = embedding.fit_transform(centroids)
        
    colors = ["blue", "purple", "green", "orange", "yellow", "pink", "black", "gray", "olive", "cyan"]

    plt.scatter([t[0] for t in transformed], [t[1] for t in transformed], c=digits.target, cmap="Paired")
    plt.scatter([t[0] for t in centroids_transform], [t[1] for t in centroids_transform], color="black")
    plt.colorbar()
    plt.show()

elif display == "accuracy":
    # find the accuracy for a number of fractions of data used as training data
    fractions = [1/3, 1/2, 2/3, 3/4, 4/5]
    accuracies = []

    for frac in fractions:
        result = k_means(digits.data[:int(frac*len(digits.data))], 10, 30)
        accuracies.append(accuracy(frac))

    plt.plot(fractions, accuracies)
    plt.xlabel("Fraction of data used as training data")
    plt.ylabel("Accuracy")
    plt.show()
    

elif display == "centroids":
    result = k_means(digits.data, 10, 30)
    
    centroids = [result[i][0] for i in range(10)]
    
    # display each centroid
    for centroid in centroids:
        display_digit(np.array(centroid))