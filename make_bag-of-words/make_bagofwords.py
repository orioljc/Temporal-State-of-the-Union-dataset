import nltk
import logging

from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import SpaceTokenizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet

nltk.download('punkt')
#nltk.download()

import cStringIO

#python debugger
import pdb

#manage sorted lists
import bisect

def load_text_corpus(path):
	# RegEx or list of file names
	files = ".*\.txt"
	from nltk.tokenize import RegexpTokenizer
	#tok = RegexpTokenizer(r'\w+|\$[\d\.]+|\S^:+|[*]+')
	#tok = RegexpTokenizer(r'\b(?![0-9])\w+|\S^:+|[*]+')
	tok = RegexpTokenizer(r'\w+|\S^:+|[*]+')
	corpus0 = PlaintextCorpusReader(path + "/", files, word_tokenizer=tok)
	corpus  = nltk.Text(corpus0.paras())
 
	return corpus


def separate_addresses(corpus):
	count = 0
	first = True
	aux = None
	addresses = []
	for item1 in corpus:
		#pdb.set_trace()
		if item1[0][0].encode('latin_1') == "***":
			if first:
				first = False
			else:
				if addresses is None:
					addresses = aux
				else:
					addresses.append(aux)
				aux = None
				#remove description of each state of the union (first paragraph)
				addresses[-1].pop(0)
		else:
			if aux is None:
				aux = item1
			else:
				aux.append(item1)
		#pdb.set_trace()

	return addresses

def devide_each_address(corpus):
	l = len(corpus)
	addresses = [None]*l
	aux = None
	for i in range(0, l):
		count = 1
		for item2 in corpus[i]:
			if aux is None:
				aux = item2
			else:
				aux.append(item2)
			if (count % 3) == 0:
				if addresses[i] is None:
					addresses[i] = [aux]
				else:
					addresses[i] = addresses[i]+[aux]
				aux = None
			count += 1
		#end of address and last paragraphs not saved yet
		if (count % 3) != 1:
			if addresses[i] is None:
				addresses[i] = [aux]
			else:
				addresses[i] = addresses[i]+[aux]
			aux = None
	return addresses




	#print(item1.encode('latin_1'))


#Stemming
def stem_words_array(words_array):
	stemmer = nltk.PorterStemmer();
	stemmed_words_array = [];
	for word in words_array:
		stem = stemmer.stem(word);
		stemmed_words_array.append(stem);
	return stemmed_words_array;

#Lemmatization
def lemmatize_words_array(words_array):
	lemmatizer = nltk.stem.WordNetLemmatizer()
	lemmatized_words_array = [];
	for word in words_array:
		lemma = lemmatizer.lemmatize(word)
		lemmatized_words_array.append(lemma)
	return lemmatized_words_array

def create_list_addresses(addresses):
	#given the list of lists containing the addresses devided by documents returns a two dimensional list
	#(corresponding to the two dimensons {address, document}) and containing a simple list with the corresponding words
	l = len(addresses)
	addresses_words = [None]*l
	for i in range(0,l):
		addresses_words[i] = []
		j = 0
		addresses_words[i] = []
		for document in addresses[i]:
			#addresses_words[i].append(create_list_general(document))
			aux = []
			create_list_general(document, aux)
			addresses_words[i].append(aux)
			j += 1
	#pdb.set_trace()
	return addresses_words

def create_list_general(the_list, new_list):
	#given a list of lists (no limit in levels of sublists) returns a single list with all the elements
	
	#check for numbers
	def contains_numbers(d):
		return bool(d.isdigit())

	for each_item in the_list:
		#pdb.set_trace()
		if isinstance(each_item, list):
			create_list_general(each_item, new_list)
		else:
			#eliminate numbers except those that are probably years
			if contains_numbers(each_item):
				if( float(each_item) in range(1600, 2050)):
					new_list.append(each_item.lower())
			else:
				new_list.append(each_item.lower())
	#pdb.set_trace()
	#return new_list

# def eliminate_numbers(the_list):
# 	#given a list of lists (no limit in levels of sublists) returns a single list with all the elements
# 	_numbers = re.compile('\d')
# 	def contains_numbers(d):
# 		return bool(_numbers.search(d))
# 	for each_item in the_list:
# 		#pdb.set_trace()
# 		if isinstance(each_item, list):
# 			eliminate_numbers(each_item)
# 		else:
# 			if contains_numbers(each_item)



# def create_vocabulary(the_list, vocabulary):
# 	#given a list of lists (no limit in levels of sublists) returns a single list with all the elements
# 	for each_item in the_list:
# 		#pdb.set_trace()
# 		if isinstance(each_item, list):
# 			create_vocabulary(each_item, vocabulary)
# 		else:
# 			#pdb.set_trace()
# 			vocabulary[each_item] = 0

def create_vocabulary(corpus):
    unique_vocabulary = {}
    for term in corpus:
        unique_vocabulary[term] = 0;
    return unique_vocabulary;

def add_pairs_vocabulary(pairs, vocabulary):
    for sample in pairs:
        vocabulary[sample[0]+"_"+sample[1]] = 0;


# def create_vocabulary(corpus):
# 	new_list = []
# 	for each_item in corpus:
# 		if isinstance(each_item, list):
# 			aux = create_list_general(each_item)

# 			bisect.insort(new_list, )
# 		else:
# 			if( binary_search(new_list, each_item) == -1 ): 
# 				bisect.insort(new_list, each_item)
# 	#pdb.set_trace()
# 	return new_list

from bisect import bisect_left
def binary_search(a, x, lo=0, hi=None):   # can't use a to specify default for hi
    hi = hi if hi is not None else len(a) # hi defaults to len(a)   
    pos = bisect_left(a,x,lo,hi)          # find insertion position
    return (pos if pos != hi and a[pos] == x else -1) # don't walk off the end

#read text file and tokenize it
print "Reading file..."
corpus = load_text_corpus("state-of-the-union/original_file")

#eliminate numbers
#print "Eliminating numbers..."



print "Read " + str(len(corpus)) + "words:" + str(corpus[0:10])

#separate the read text into the different addresses
print "Separating addresses..."
corpus = separate_addresses(corpus)

#devide each address into many different documents of no more than 3 paragraphs
print "Splitting each address..."
addresses = devide_each_address(corpus)

#arranges list that contains addresses and documents
addresses_words = create_list_addresses(addresses)

#stemming
# print "Stemming and lemmatizing..."
# for i in range(0, len(addresses_words)):
# 	for j in range(0, len(addresses_words[i])):
# 		addresses_words[i][j] = stem_words_array(addresses_words[i][j])
# 		addresses_words[i][j] = lemmatize_words_array(addresses_words[i][j])

#remove stopwords
print "Removing stopwords..."
stop_words = set(stopwords.words('english'))
for i in range(0, len(addresses_words)):
	for j in range(0, len(addresses_words[i])):
		temp = [w for w in addresses_words[i][j] if not w in stop_words]
		addresses_words[i][j] = temp


#create single list with with all the read text (after being already processed)
print "Creating single list with all the text..."
words_all = []
create_list_general(addresses_words, words_all)

#get frequent pairs of words
print "Getting frequent pairs of words..."
import nltk
from nltk.collocations import *
bigram_measures = nltk.collocations.BigramAssocMeasures()

bi_finder = BigramCollocationFinder.from_words(words_all)
bi_scored = bi_finder.score_ngrams(bigram_measures.raw_freq)
set(bigram for bigram, score in bi_scored) == set(nltk.bigrams(words_all))
pairs = sorted(bi_finder.nbest(bigram_measures.raw_freq, 50))

#eliminate some pairs which are not meaningful


##Create vocablary
print "Creating vocabulary..."
#create object with a unique vocabulary
vocabulary = {}
vocabulary = create_vocabulary(words_all)
#add pairs to vacabulary
add_pairs_vocabulary(pairs, vocabulary)
#create counts
vocabulary_list = []
for (a, b) in vocabulary.items():
	vocabulary_list.append(a)
vocabulary_list.sort()
print "vocabulary_list length: " + str(len(vocabulary_list))

#pdb.set_trace()
#count words on each address

l = len(addresses_words)
#l = 5

print "Counting words one each address..."
words_count = [None]*len(addresses_words)
for i in range(0,len(addresses_words)):
	words_count[i] = 0
	for item in addresses_words[i]:
		words_count[i] += len(item)


#printing vocabulary
print "Printing vocabulary..."
vocabulary_length = len(vocabulary_list)
my_file = open("state-of-the-union/bag_of_words/vocab.stateunion.txt", 'w')
my_file.truncate()	#erase file
for w in vocabulary_list:
	my_file.write(w + "\n")
my_file.close()

#pdb.set_trace()
##Counting word appearance
print "Counting word appearance..."
counts = [None]*l
#for i in range(0,l):
for i in range(0,l):
	print " ...processing address " + str(i) + "/" + str(l) 
	counts[i] = [None]*len(addresses_words[i])
	for j in range(0, len(addresses_words[i])):
		counts[i][j] = {}
		for w in addresses_words[i][j]:
			if w in vocabulary_list:
				ind = vocabulary_list.index(w)
				if counts[i][j].has_key(ind):
					counts[i][j][ind] += 1
				else:
					counts[i][j][ind] = 1
			else:
				#raise "Error: word %s not in the vocabulary" << w
				raise "Error: word not in the vocabulary"


#printing counts
docs_per_address = "state-of-the-union/bag_of_words/number_of_documents.txt"
dpa_file = open(docs_per_address, "w")
dpa_file.truncate()

#Number of addresses (used to allocate memory in C++)
# dpa_file.write(str(l)+"\n") 

for i in range(0,l):
	dpa_file.write(str(len(counts[i]))+"\n")

	print " ...printing addresses bag of words " + str(i) + "/" + str(l) 
	#pdb.set_trace()
	file_name = "state-of-the-union/bag_of_words/addresses/stateunion_"+str(i+1)+".txt"
	my_file = open(file_name, 'w')
	my_file.truncate()	#erase file
	l2 = len(addresses_words[i])
	#my_file.write(str(l2) + "\n")
	#my_file.write(str(vocabulary_length) + "\n")
	#my_file.write(str(words_count[i]) + "\n")
	for j in range(0, l2):
		for key in counts[i][j]:
			#write "document word frequency"
			my_file.write(str(j+1) + " " + str(key) + " " + str(counts[i][j][key]) + "\n")
	my_file.close()
dpa_file.close()




#Split training and testing datasets

# #Print number of documents
# docs_per_address = "state-of-the-union/bag_of_words/number_of_documents.txt"
# dpa_file.open(docs_per_address, "w")
# dpa_file.truncate()
# for address in addresses_words:
# 	dpa_file.write( str(len(address)) + "\n")
# dpa_file.close()

