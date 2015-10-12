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
afp.setOutputFormat('csv', './outputs', {'Metadata': 'false', 'Precision': '2'})

emotions = ['angry', 'happy', 'neutral', 'unhappy']
feats = ['eng', 'lpc', 'lsf', 'ldd', 'mfc']

def getProperties(audiofile):
  props = ""
  for feat in feats:
    lines = []
    outfile = "./outputs" + audiofile[1:] + "." + feat + ".csv"
    with open(outfile, 'r') as f:
      for line in f.readlines():
        lines.append(line.split(','))
    for j in range(0, len(lines[0])):
      arr = []
      for i in range(0, len(lines)):
        #val = lines[i][j]
        # if val.isdigit():
        arr.append(float(lines[i][j]))
        # else:
        #  arr.append(float(0))
      diff = numpy.diff(arr)
      diff = numpy.absolute(diff)
      props=props+(str(numpy.nanmin(arr))+',')
      props=props+(str(numpy.nanmax(arr))+',')
      props=props+(str(numpy.nanmean(arr))+',')
      props=props+(str(numpy.nanstd(arr))+',')
      props=props+(str(numpy.median(arr))+',')
      props=props+(str(numpy.ptp(arr))+',')
      props=props+(str(numpy.nanmin(diff))+',')
      props=props+(str(numpy.nanmax(diff))+',')
    # endfor
  # print len(props)
  return props

data = ""
target = ""
root = './training_dataset/'

for e in emotions:
  for (dirpath, dirnames, filenames) in walk(root + e):
    for afl in filenames:
      audiofile = dirpath + '/' + afl
      #p = afp.processFile(engine, audiofile)
      #if p == 0:
      props = getProperties(audiofile)
      data = data + str(props) + '\n'
      target = target + str(emotions.index(e)) + '\n'
      # endif
    break
  # endwalk
print target

f = open('data','w')
f.write(data)
f.close()

f = open('target','w')
f.write(target)
f.close()
