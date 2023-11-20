import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
import seaborn as sns
from sklearn.cluster import KMeans

#importing datasets
zoo = pd.read_csv('C:/Users/admin/Downloads/animal_DB/zoo.csv')
class_types = pd.read_csv('C:/Users/admin/Downloads/animal_DB/class.csv')
df=pd.merge(zoo,class_types,how='left',left_on='class_type',right_on='Class_Number')

#visualizing the animals distribution
animal_classes = class_types.iloc[:,2]
n_of_animals = class_types.iloc[:,1]
animals_distribution = dict(zip(animal_classes, n_of_animals))

plt.figure(figsize=(10, 6))
plt.bar(animal_classes, n_of_animals, color='blue')
plt.xlabel('Animal classes')
plt.ylabel('Number of animals')
plt.title('Animal Class Types Distribution')
plt.show()

#data preprocessing
X = zoo.iloc[:, 1:17]
Y = zoo.iloc[:, 17]
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3, random_state = 42, stratify = Y)
np.array(X_train)
np.array(X_test) #to check if I can put everything in one bracket

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

#K Nearest Neighbor
classifier_knn = KNeighborsClassifier()
classifier_knn.fit(X_train, Y_train)

Y_pred_knn = classifier_knn.predict(X_test)
print("Test Accuracy : ",classifier_knn.score(X_test,Y_test))
print("Train Accuracy : ",classifier_knn.score(X_train,Y_train))

tmp_knn = pd.DataFrame(zoo)
pred_knn = pd.DataFrame(Y_pred_knn,dtype=int, index=Y_test.index)
tmp_knn['prediction'] = pred_knn
tmp_knn = tmp_knn.dropna()

for i in range(tmp_knn.shape[0]):
    if tmp_knn.iloc[i][17] != tmp_knn.iloc[i][18]:
        print('  '+str(tmp_knn.iloc[i][0]))
        print('class type: '+str(tmp_knn.iloc[i][17]))
        print('prediction: '+str(tmp_knn.iloc[i][18]))

#Decision Tree
classifier_dt = DecisionTreeClassifier()
classifier_dt.fit(X_train, Y_train)

y_pred_tree = classifier_dt.predict(X_test)
print("Test Accuracy : ",classifier_dt.score(X_test,Y_test))
print("Train Accuracy : ",classifier_dt.score(X_train,Y_train))

tmp_tree = pd.DataFrame(zoo)
pred_dt = pd.DataFrame(y_pred_tree,dtype=int, index=Y_test.index)
tmp_tree['prediction'] = pred_dt
tmp_tree = tmp_tree.dropna()

for i in range(tmp_tree.shape[0]):
    if tmp_tree.iloc[i][17] != tmp_tree.iloc[i][18]:
        print('  '+str(tmp_tree.iloc[i][0]))
        print('class type: '+str(tmp_tree.iloc[i][17]))
        print('prediction: '+str(tmp_tree.iloc[i][18]))

#Random Forest
classifier_RF = RandomForestClassifier()
classifier_RF.fit(X_train, Y_train)

y_pred_forest = classifier_RF.predict(X_test)
print("Test Accuracy : ",classifier_RF.score(X_test,Y_test))
print("Train Accuracy : ",classifier_RF.score(X_train,Y_train))

tmp_forest = pd.DataFrame(zoo)
pred_forest = pd.DataFrame(y_pred_forest,dtype=int, index=Y_test.index)
tmp_forest['prediction'] = pred_forest
tmp_forest = tmp_forest.dropna()

for i in range(tmp_forest.shape[0]):
    if tmp_forest.iloc[i][17] != tmp_forest.iloc[i][18]:
        print('  '+str(tmp_forest.iloc[i][0]))
        print('class type: '+str(tmp_forest.iloc[i][17]))
        print('prediction: '+str(tmp_forest.iloc[i][18]))

#Support Vector Machine
classifier_svm = svm.SVC()
classifier_svm.fit(X_train, Y_train)

y_pred_svm = classifier_svm.predict(X_test)
print("Test Accuracy : ",classifier_svm.score(X_test,Y_test))
print("Train Accuracy : ",classifier_svm.score(X_train,Y_train))

tmp_svm = pd.DataFrame(zoo)
pred_svm = pd.DataFrame(y_pred_svm,dtype=int, index=Y_test.index)
tmp_svm['prediction'] = pred_svm
tmp_svm = tmp_svm.dropna()

for i in range(tmp_svm.shape[0]):
    if tmp_svm.iloc[i][17] != tmp_svm.iloc[i][18]:
        print('  '+str(tmp_svm.iloc[i][0]))
        print('class type: '+str(tmp_svm.iloc[i][17]))
        print('prediction: '+str(tmp_svm.iloc[i][18]))


#Naive Bayes
classifier_nb = GaussianNB()
classifier_nb.fit(X_train, Y_train)

y_pred_NB = classifier_nb.predict(X_test)
print("Test Accuracy : ",classifier_nb.score(X_test,Y_test))
print("Train Accuracy : ",classifier_nb.score(X_train,Y_train))

tmp_NB = pd.DataFrame(zoo)
pred_NB = pd.DataFrame(y_pred_NB,dtype=int, index=Y_test.index)
tmp_NB['prediction'] = pred_NB
tmp_NB = tmp_NB.dropna()

for i in range(tmp_NB.shape[0]):
    if tmp_NB.iloc[i][17] != tmp_NB.iloc[i][18]:
        print('  '+str(tmp_NB.iloc[i][0]))
        print('class type: '+str(tmp_NB.iloc[i][17]))
        print('prediction: '+str(tmp_NB.iloc[i][18]))

#Comparing algorithms
algorithms = pd.DataFrame({
    'Model': ["K Neighbors", "Decision Tree",
     "Random Forest", "SVM ", "Naive Bayes"],
    'Score': [classifier_knn.score(X_test,Y_test),
     classifier_dt.score(X_test,Y_test),
     classifier_RF.score(X_test,Y_test),
     classifier_svm.score(X_test,Y_test),
     classifier_nb.score(X_test,Y_test)]})

algorithms.sort_values(by='Score', ascending=False)

#Correlation analysis
plt.subplots(figsize=(10,5))
ax = plt.axes()
ax.set_title('Correlation matrix')
corr = zoo.iloc[:, 1:].corr()
sns.heatmap(corr, annot=True, xticklabels=corr.columns.values, yticklabels=corr.columns.values)

#which feature(s) are relevant to efficiently classify the animals?
print(corr[corr != 1][abs(corr)> 0.65].dropna(how='all', axis=1).dropna(how='all', axis=0))
df.iloc[:, 1:19].groupby("Class_Number").mean()

#K Means Clustering
##elbow method
animal_features = zoo[['hair', 'feathers', 'eggs', 'milk', 'airborne',
                        'aquatic', 'predator', 'toothed', 'backbone', 'breathes',
                        'venomous', 'fins', 'legs', 'tail', 'domestic', 'catsize']]
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters = i, random_state = 42)
    kmeans.fit(animal_features)
    wcss.append(kmeans.inertia_)
plt.plot(range(1, 11), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

num_clusters = 4
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
y_kmeans = kmeans.fit_predict(animal_features)

# Visualize the clusters
plt.figure(figsize=(10, 6))
for cluster_num in range(num_clusters):
    cluster_data = zoo[y_kmeans == cluster_num]
    plt.scatter(cluster_data['eggs'], cluster_data['hair'], label=f'Cluster {cluster_num}')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s = 200, c = 'yellow', label = 'Centroids')
plt.title('Clustering of Animals Based on Features')
plt.xlabel('eggs')
plt.ylabel('hair')
plt.legend()
plt.show()








