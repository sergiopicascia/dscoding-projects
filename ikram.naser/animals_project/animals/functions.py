import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class data_import:
    def import_zoo(self):
        zoo = pd.read_csv('C:/Users/admin/Downloads/animal_DB/zoo.csv')
        return zoo.head()

    def import_class_types(self):
        class_types = pd.read_csv('C:/Users/admin/Downloads/animal_DB/class.csv')
        return class_types.head()


class Visualizations:

    def distribution_plot(self, animal_classes, n_of_animals):
        self.animal_classes = ('Mammal', 'Bird', 'Reptile', 'Fish', 'Amphibian', 'Bug', 'Invertebrate')
        self.n_of_animals = (41, 20, 5, 13, 4, 8, 10)
        plt.figure(figsize=(10, 6))
        plt.bar(animal_classes, n_of_animals, color='blue')
        plt.xlabel('Animal classes')
        plt.ylabel('Number of animals')
        plt.title('Animal Classes Distribution')
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
        wcss = []  # Within-Cluster Sum of Square,is the sum of the squared distance between each point and the centroid in a cluster

        # Try different values of k (number of clusters)
        for k in range(1,
                       11):  # iterates over different values of k (from 1 to 10) as an arbitrary range to explore a reasonable number of clusters
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


def kmeans(self):

    # Selecting the features for clustering
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
    plt.scatter(kmeans.cluster_centers_[:, 2], kmeans.cluster_centers_[:, 0], s=100, c='yellow', label='Centroids')

    # Set plot
    plt.title('Clustering of Animals Based on Features')
    plt.xlabel('eggs')
    plt.ylabel('hair')
    plt.legend()
    plt.show()
