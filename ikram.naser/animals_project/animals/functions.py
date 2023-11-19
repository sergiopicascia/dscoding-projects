import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

zoo = pd.read_csv('C:/Users/admin/Downloads/animal_DB/zoo.csv')
class_types = pd.read_csv('C:/Users/admin/Downloads/animal_DB/class.csv')
# animal_classes = class_types.iloc[:, 2]
# n_of_animals = class_types.iloc[:, 1]

def distribution_plot(self):
    animal_classes = ('Mammal', 'Bird', 'Reptile', 'Fish', 'Amphibian', 'Bug', 'Invertebrate')
    n_of_animals = (41, 20, 5, 13, 4, 8, 10)
    plt.figure(figsize=(10, 6))  # width of 10 inches and a height of 6 inches
    plt.bar(animal_classes, n_of_animals, color='blue')
    plt.xlabel('Animal classes')
    plt.ylabel('Number of animals')
    plt.title('Animal Class Types Distribution')
    plt.show()



def correlation_plot(self):
        zoo = pd.read_csv('C:/Users/admin/Downloads/animal_DB/zoo.csv')
        plt.subplots(figsize=(10, 5))  # 1000x500
        ax = plt.axes()
        ax.set_title('Correlation matrix')
        corr = zoo.iloc[:, 1:].corr()
        sns.heatmap(corr, annot=True, xticklabels=corr.columns.values, yticklabels=corr.columns.values)

def kmeans(self, n_clusters, kmeans):
    zoo = pd.read_csv('C:/Users/admin/Downloads/animal_DB/zoo.csv')
    animal_features = zoo[['hair', 'feathers', 'eggs', 'milk', 'airborne',
                            'aquatic', 'predator', 'toothed', 'backbone', 'breathes',
                            'venomous', 'fins', 'legs', 'tail', 'domestic', 'catsize']]
    num_clusters = 4
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    self.n_cluster = n_clusters
    self.kmeans = kmeans
#def elbow_plot(self):
        wcss = []  # Within-Cluster Sum of Square,is the sum of the squared distance between each point and the centroid in a cluster
       # for i in range(1, 11):
          kmeans = KMeans(n_clusters=i, random_state=42)
          kmeans.fit(animal_features)
        wcss.append(kmeans.inertia_)
        plt.plot(range(1, 11), wcss)
        plt.title('The Elbow Method')
        plt.xlabel('Number of clusters')
        plt.ylabel('WCSS')
        plt.show()
def splitting_data(self):
    zoo = pd.read_csv('C:/Users/admin/Downloads/animal_DB/zoo.csv')
    self.X = zoo.iloc[:, 1:17]  # only the features
    self.Y = zoo.iloc[:, 17]  # only the label
    return X, Y

def scaling(self):
    sc = StandardScaler()
    self.sc = sc
    return X_train = sc.fit_transform(X_train)
    return X_test = sc.transform(X_test)

