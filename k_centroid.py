import pandas as pd
import numpy as np
from pprint import pprint
from collections import Counter
#import re
#from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
#from sklearn.preprocessing import OneHotEncoder

interest_group_centroids = []                               # cluster centriods on which the interest groups are formed
interest_groups = []                                        # Most similar items for each centroid in the interest group
data = pd.read_csv('lastfm.csv')                            # Reading the CSV file
#print(data)

# Create a new dataframe without the user ids.
data_items = data.drop('user', 1)                           # Drop the user column for item-item similarity calculation
print('Dimension of loaded data is:', np.ndim(data_items))  #Dimension of the loaded data
items_len = len(data_items.columns)                         #lengh of the items in the dataset
length = []                                                 #stores the index of the centroids


print('\n\n#########################################CENTROIDS#####################################################\n\n')

p = (items_len-1) // 5
r = p
length.append(p)

for index in range(0, 4):
    items_len = int(round(r + p))
    r = items_len
    length.append(items_len)
print(length)


for index in length:
    centroids = data_items.columns.values[index]
    interest_group_centroids.append(centroids)
print('The Centroids are = ', interest_group_centroids, '\n\n')


'############SIMILARITY#################'


'# As a first step we normalize the user vectors to unit vectors.'

magnitude = np.sqrt(np.square(data_items).sum(axis=1))
data_items = data_items.divide(magnitude, axis='index')

'#print(data_items.head(5))'


def calculate_similarity(data_items):
    data_sparse = sparse.csr_matrix(data_items)
    similarities = cosine_similarity(data_sparse.transpose())
    #print(similarities)
    sim = pd.DataFrame(data=similarities, index=data_items.columns, columns=data_items.columns)
    return sim
'# Build the similarity matrix'
data_matrix = calculate_similarity(data_items)
'# Lets get the top 11 similar artists for Beyonce'


print('##############INTEREST GROUPS##################\n\n')


for i in interest_group_centroids:
    Interest_group = data_matrix.loc[i].nlargest(p).index.values
    print('Interest group', interest_group_centroids.index(i), ' = ', Interest_group, '\n')
    interest_groups.append(Interest_group)
#print(interest_groups)

print('###############USERS###################\n\n')


user = 19695                                           # The id of the user for whom we want to generate recommendations
user_index = data[data.user == user].index.tolist()[0] # Get the frame index
#print('user index is: ', user_index)
known_user_likes = data_items.ix[user_index]
known_user_likes = known_user_likes[known_user_likes > 0].index.values

print('user', user_index, 'likes', known_user_likes, '\n')

print('###############USERS ASSOCIATION###################\n\n')

for i in interest_groups:
    a_vals = Counter(i)
    b_vals = Counter(known_user_likes)

    # convert to word-vectors
    words = list(a_vals.keys() | b_vals.keys())
    a_vect = [a_vals.get(word, 0) for word in words]
    b_vect = [b_vals.get(word, 0) for word in words]
    # find cosine
    len_a = sum(av * av for av in a_vect) ** 0.5
    len_b = sum(bv * bv for bv in b_vect) ** 0.5
    dot = sum(av * bv for av, bv in zip(a_vect, b_vect))
    cosine = dot / (len_a * len_b)

    if cosine == 0:
        pass
    else:
        print('User:', user_index, 'is associated to the Interest group with similarity:', cosine)





# def jaccard_similarity_score(df):
# #     """Calculate the column-wise cosine similarity for a sparse
# #     matrix. Return a new dataframe matrix with similarities.
# #     """
#       data_sparse = sparse.csr_matrix(df)
#       similarities = jaccard_similarity_score(data_sparse.transpose())
#       similarities = 1 - pairwise_distances(df.T, metric='hamming')
#       sim = pd.DataFrame(data=similarities, index=df.columns, columns=df.columns)
#       return sim
# #
# data_matrix2 = jaccard_similarity_score(df)
# print(data_matrix2)
# # #print(data_matrix.loc['aerosmith'].nlargest(6))



# kmeans = KMeans(n_clusters=2, n_init=20, n_jobs=2)
# kmeans.fit(data_matrix)
# # We look at 3 the clusters generated by k-means.
# common_words = kmeans.cluster_centers_[:1]
# print(common_words)
#     #for num, centroid in enumerate(common_words):
#     #print("Interest group", str(num) + ' : ' + ', '.join(words[word] for word in centroid))