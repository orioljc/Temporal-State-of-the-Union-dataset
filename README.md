# Temporal-State-of-the-Union-dataset
Bag of words dataset with the State of the Union addresses contained between:
- George Washington, State of the Union Address, January 8, 1790
- George W. Bush, State of the Union Address, January 31, 2006

Included folders: 
- bag_of_words: contains each of the addresses in bag-of-words format
- make_bag-of-words: contains the Python code used for transforming the original text to the bag-of-words format
- original_file: contains the original file that originated the dataset
- R_functions: contains R code for splitting the dataset in training and testing sets
- splited_data: contains each address in bag_of_words but splitted in two sets (training and testing sets)

The format of each bag-of-words address is:

docID wordID count 

docID wordID count 

docID wordID count 

docID wordID count 

... 

docID wordID count 

docID wordID count 

docID wordID count 
