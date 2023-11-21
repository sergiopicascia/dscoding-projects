import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AffinityPropagation
from sklearn.metrics import silhouette_score
import seaborn as sns
from collections import Counter
from src.ZooAnimals import DataProcessor


def run_clustering(data, method, **kwargs):
    X_numeric = data.drop(['animal_name', 'class_type'], axis=1)

    if method == "affinity_propagation":
        af = AffinityPropagation(**kwargs)
        labels = af.fit_predict(X_numeric)
        cluster_centers = af.cluster_centers_
    elif method == "kmeans":
        kmeans = KMeans(**kwargs)
        labels = kmeans.fit_predict(X_numeric)
        cluster_centers = kmeans.cluster_centers_

    # Silhouette Score Calculation
    silhouette_avg_score = silhouette_score(X_numeric, labels)

    # Display clustering results
    result_df = pd.DataFrame({'animal_name': data['animal_name'], 'class_type': data['class_type'], 'cluster_label': labels})
    return result_df, silhouette_avg_score

# Streamlit App Main Code
def main():
    st.title("Animal Clustering and Clustering Algos Comparison")

    # Uploading the File with Data Points
    uploaded_file = st.file_uploader("Upload Excel File in '.xlsx' format only", type=["xlsx"])

    if uploaded_file:
        # Processing the uploaded file and clustering the data
        data_processor = DataProcessor(uploaded_file)
        data_processor.import_data()
        animal_feature_data = data_processor.data

        # Displaying the clustering options
        clustering_method = st.selectbox("Select Clustering Method", ["Affinity Propagation", "K-Means"])

        if clustering_method == "Affinity Propagation":
            damping = st.slider("Damping Factor", 0.5, 0.9999, 0.7)
            result, silhouette_avg_score = run_clustering(animal_feature_data, method="affinity_propagation", damping=damping)
        elif clustering_method == "K-Means":
            num_clusters = st.slider("Number of Clusters", 4, 10, 7)
            result, silhouette_avg_score = run_clustering(animal_feature_data, method="kmeans", n_clusters=num_clusters)

        # Silhoutte Scores

        st.write(f"Silhoutte Score for {clustering_method} is {silhouette_avg_score}")


        # Display the Clustering results 
        st.write("Clustering Results:")
        st.write(result)

        # Using matplotlib for plotting the Number of animals in each cluster
        fig, ax = plt.subplots(figsize=(10,10))
        sns.countplot(x='cluster_label', data=result, ax=ax)
        plt.title('Count of Animals in Each Cluster')
        st.pyplot(fig)

        # Plot for Count of Animals in Initial Categories
        plt.figure(figsize=(10,10))
        sns.countplot(x='class_type', data=result)
        plt.title("Count of Animals in Initial CAtegories")

        # Comparison of the CLusters with Initial Categories with animal names
        comparison_df = result.groupby(['animal_name', 'class_type', 'cluster_label']).size().reset_index(name='count')
        st.write("Comparison of Initial Categories with Clustered Data : ")
        st.write(comparison_df)

if __name__ == "__main__":
    main()