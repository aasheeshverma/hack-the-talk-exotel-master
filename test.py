import numpy
from os import walk
import yaafelib as yaafe

from sklearn import neighbors
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.svm import NuSVC
from sklearn import linear_model
from sklearn.linear_model import SGDClassifier
from sklearn import tree
from sklearn.neighbors.nearest_centroid import NearestCentroid

yaafe.loadComponentLibrary('yaafe-io')
fp = yaafe.FeaturePlan(sample_rate=8000)
fp.loadFeaturePlan('./featureplan')
engine = yaafe.Engine()
engine.load(fp.getDataFlow())
afp = yaafe.AudioFileProcessor()
afp.setOutputFormat('csv', './outputs', {'Metadata': 'false', 'Precision': '6'})

emotions = ['angry', 'happy', 'neutral', 'unhappy']
feats = ['eng', 'lpc', 'lsf', 'ldd', 'mfc']

def getProperties(audiofile):
  props = []
  for feat in feats:
    lines = []
    outfile = "./outputs" + audiofile[1:] + "." + feat + ".csv"
    with open(outfile, 'r') as f:
      for line in f.readlines():
        lines.append(line.split(','))
    for j in range(0, len(lines[0])):
      arr = []
      for i in range(0, len(lines)):
        val = lines[i][j]
        if val.isdigit():
          arr.append(float(lines[i][j]))
        else:
          arr.append(float(0))
      diff = numpy.diff(arr)
      diff = numpy.absolute(diff)
      props.append(numpy.nanmin(arr))
      props.append(numpy.nanmax(arr))
      props.append(numpy.nanmean(arr))
      props.append(numpy.nanstd(arr))
      props.append(numpy.median(arr))
      props.append(numpy.ptp(arr))
      props.append(numpy.nanmin(diff))
      props.append(numpy.nanmax(diff))
    # endfor
  # print len(props)
  return props

data = []
target = []
with open('data', 'r') as f:
  for line in f.readlines():
    arr = line.split(',')
    arr2 = []
    for val in range (0, len(arr)-1):
      arr2.append(float(arr[val]))
    data.append(arr2)

with open('target', 'r') as f:
  for line in f.readlines():
    target.append(int(line))

X, y = data, target
svc = SVC(C=1000.0, gamma=1.0000000000000001e-05).fit(X, y)

def read_input():
  f = open('input.txt')
  files = f.read().split('\n')
  files = [f for f in files if f]
  return files

files = read_input()
for inputfile in files:
  inputfile = './' + inputfile
  p = afp.processFile(engine, inputfile)
  if p == 0:
    props = getProperties(inputfile)
    r = svc.predict(props)
    print emotions[r]
  else:
    print 'angry'
