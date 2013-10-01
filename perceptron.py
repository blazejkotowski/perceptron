import random
import sys

class Data(object):
  '''
  Data generator class
  '''

  def __init__(self, N = 10):
    '''
    The constructor - creates data object with random line dividing
    input area and random points of input area with related correct
    f(x) values

    N - number of random points generated
    '''

    self.line = ((),())
    self.points = []
    random.seed()
    self._generate_line()
    self._generate_points(N)

  def _generate_line(self):
    '''
    Generates random line in dimensions
    [-1,1] x [-1,1] and saves it to object
    '''

    self.line = (
        (random.uniform(1,-1), random.uniform(1,-1)),
        (random.uniform(1,-1), random.uniform(1,-1))
    )

  def _value(self, point):
    '''
    Returns real value of f(point)

    point - tuple of variables related to point
    return
      1 if point is on one side of line
      -1 if it's on another side
    '''

    line = self.line
    v1 = (line[1][0]-line[0][0], line[1][1]-line[0][1])
    v2 = (line[1][0]-point[0], line[1][1]-point[1])
    cross = v1[0]*v2[1] - v1[1]*v2[0]
    if cross > 0:
      return 1
    else:
      return -1

  def _generate_points(self, n):
    '''
    Generates list of random points and values
    of f(x) related to points given by _value function

    n - number of points to generate
    '''

    self.points = []
    for i in range(n):
      point = (random.uniform(1,-1), random.uniform(1,-1))
      self.points.append((point, self._value(point)))
  
  def get_points(self):
    '''
    Getter function for points list

    return - list of points
    '''

    return self.points


class Perceptron(object):
  def __init__(self, d=2, random_weights=False):
    self.weights = [0]*(d+1)
    if random_weights:
      self.weights = []
      random.seed()
      for i in range(d):
        self.weights.append(random.uniform(-1,1))

  def learn(self, data):
    mi = 1
    iterations = 0
    while(mi > 0):
      iterations += 1
      misclassified = []
      for point,value in data:
        if(self._value(point) != value):
          misclassified.append((point, value))
      if(len(misclassified) > 0):
        mp, value = random.choice(misclassified)
        self._update_weights(mp,value)
      mi = float(len(misclassified)) / float(len(data))
    
    return iterations

  def _update_weights(self, mp, value):
    mp = (1,) + mp
    for i, w in enumerate(self.weights):
      self.weights[i] = w + value * mp[i]

  def _value(self, point):
    s = 0
    for i, x in enumerate((1,) + point):
      s += self.weights[i] * x
    if s < 0:
      return -1
    else:
      return 1

  def probability(self, data):
    mistaken = 0
    for point,value in data:
      if self._value(point) != value:
        mistaken+=1
    return mistaken/float(len(data))

  def get_weights(self):
    return self.weights
   

if __name__ == '__main__':
  for n in [10,100]:
    iterations = []
    probabilities = []
    for i in range(1000):
      data = Data(n)
      p = Perceptron()
      
      # iterations counting
      iters = p.learn(data.get_points())
      iterations.append(iters)

      # probability computing
      pdata = Data(1000).get_points()
      probabilities.append(p.probability(pdata))

    print "For {0} known data points".format(n)
    print "\tAveragely it takes {0} iterations to find function".format(sum(iterations)/float(len(iterations)))
    print "\tAverage mistake probability is equal to {0}\n".format(sum(probabilities)/float(len(probabilities)))

