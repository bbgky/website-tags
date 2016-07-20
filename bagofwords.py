# run in directory with wordcount files ending in .w.txt (created by bagofwords.sh)

import pandas
import os
import pprint
import argparse
import matplotlib.pylab as plt
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction import DictVectorizer
from sklearn.cluster import KMeans
import webbrowser

# script takes number of pages and number of clusters as arguments
parser = argparse.ArgumentParser(description='Imports wordcounts from webpages and clusters them')
parser.add_argument('num_pages', help='How many webpages to analyze and cluster (max of 500)')
parser.add_argument('num_clusters', help='How many clusters to group pages into')
args = parser.parse_args()

# Convert wordcount files to list of dictionaries for each page
wordcounts_f = [f for f in os.listdir('.') if f.endswith('.w.txt')]
wordcounts_f.sort(reverse=True) # makes sure labeled pages are present by default
wordcounts_f = wordcounts_f[0:int(args.num_pages)]

wordcounts = []
for fl in wordcounts_f:
	wc_dict = dict()
	for line in open(fl, 'r'):
		count = line.strip().partition(' ')
		if count[2]: # drop empty lines
			wc_dict[count[2]] = int(count[0])
	wordcounts.append(wc_dict)

# Use DictVectorizer to convert the dictionaries to a sparse array like sklearn wants
word_features = DictVectorizer().fit_transform(wordcounts).toarray()

# k-means clustering
clusters = KMeans(n_clusters=int(args.num_clusters)).fit_predict(word_features)
clustered_pages = zip(clusters,wordcounts_f)
clustered_pages.sort(key=lambda x: x[0])
pprint.pprint(clustered_pages)

# Plot clusters
plt.scatter(range(1,len(clusters)+1), clusters)
plt.show()

# Display pages from a given cluster in the broswer (best with few pages!)
target_cluster = ''
while target_cluster != 'q':
	target_cluster = raw_input("Which cluster do you want to open pages of? (q to quit):")
	if target_cluster != 'q':
		print ("Pages in cluster {}:".format(target_cluster))
		for cl,page in clustered_pages:
			if cl == int(target_cluster):
				print page.partition('.')[0]+'.html'
				webbrowser.open(page.partition('.')[0]+'.html', new=2) #open in new tab

