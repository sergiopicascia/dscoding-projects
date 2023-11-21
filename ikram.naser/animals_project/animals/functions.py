import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


class_types = pd.read_csv('C:/Users/admin/Downloads/animal_DB/class.csv')
animal_classes = class_types.iloc[:, 2]
n_of_animals = class_types.iloc[:, 1]
class data_import:
    def import_zoo(self):
        print(zoo = pd.read_csv('C:/Users/admin/Downloads/animal_DB/zoo.csv'))
    def import_class_types(self):
        print(class_types = pd.read_csv('C:/Users/admin/Downloads/animal_DB/class.csv'))

class Visualizations:
    def distribution_plot(self, animal_classes, n_of_animals):
        self.animal_classes = ('Mammal', 'Bird', 'Reptile', 'Fish', 'Amphibian', 'Bug', 'Invertebrate')
        self.n_of_animals = (41, 20, 5, 13, 4, 8, 10)
        plt.figure(figsize=(10, 6))
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

    def elbow_plot(self):
        zoo = pd.read_csv('C:/Users/admin/Downloads/animal_DB/zoo.csv')
        # Select relevant features for clustering
        animal_features = zoo[['hair', 'feathers', 'eggs', 'milk', 'airborne',
                               'aquatic', 'predator', 'toothed', 'backbone', 'breathes',
                               'venomous', 'fins', 'legs', 'tail', 'domestic', 'catsize']]
        # Standardize the features
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(animal_features)
        # Initialize an empty list to store the inertia values (within-cluster sum of squares)
        wcss = [] # Within-Cluster Sum of Square,is the sum of the squared distance between each point and the centroid in a cluster

        # Try different values of k (number of clusters)
        for k in range(1, 11):
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(scaled_features)
            wcss.append(kmeans.inertia_)

        # Plot the elbow curve
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, 11), wcss, marker='o')
        plt.title('The Elbow Method')
        plt.xlabel('Number of Clusters')
        plt.ylabel('WCSS')
        plt.show()

    def kmeans_plot(self, n_clusters, kmeans):
        self.n_clusters = 4
        self.kmeans = kmeans
        num_clusters = 4

        # Select the features for clustering
        zoo = pd.read_csv('C:/Users/admin/Downloads/animal_DB/zoo.csv')
        animal_features = zoo[['hair', 'feathers', 'eggs', 'milk', 'airborne',
                               'aquatic', 'predator', 'toothed', 'backbone', 'breathes',
                               'venomous', 'fins', 'legs', 'tail', 'domestic', 'catsize']]

        # Perform k-means clustering
        num_clusters = 4
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        y_kmeans = kmeans.fit_predict(animal_features)

        # Plot the clusters
        plt.figure(figsize=(10, 6))
        for cluster_num in range(num_clusters):
            cluster_data = zoo[y_kmeans == cluster_num]
            plt.scatter(cluster_data['eggs'], cluster_data['hair'], label=f'Cluster {cluster_num}')

        # Plot centroids
        plt.scatter(kmeans.cluster_centers_[:, 2], kmeans.cluster_centers_[:, 0], s=200, c='yellow', label='Centroids')

        # Set plot details
        plt.title('Clustering of Animals Based on Features')
        plt.xlabel('eggs')
        plt.ylabel('hair')
        plt.legend()
        plt.show()
class preprocessing():
    def splitting_data(self, X, Y):
        zoo = pd.read_csv('C:/Users/admin/Downloads/animal_DB/zoo.csv')
        self.X = zoo.iloc[:, 1:17]  #only the features
        self.Y = zoo.iloc[:, 17]    #only the label
        print(X, Y)
    def scaling(self, X_train, X_test):
        sc = StandardScaler()
        self.X_train = sc.fit_transform(X_train)
        self.X_test = sc.transform(X_test)
        return X_train, X_test