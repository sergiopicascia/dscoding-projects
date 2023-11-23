
The Aim of this Project is to compare two data classification algorithm by classifying a dataset of zoo-animals into 7 different classes by considering their different traits (properties/ features). 
The project is cretated as part of a Lab Project for Data Science Course.

The project demonstrates the use of github for version control, usage of pandas, and numpy for data manipulation and computing. Further, matplotlib is used  for data visualization.

The project also demonstrates the use of two Machine Learning algorithms for data-classification.



ML Algorithms for comparison and testing - 
1. Affinity Propagation - Creating Exemplars and clustering all other points to the exemplars. It creates the clusters on its own, and doesn't require number of clusters as an Inpput. 
2. K-Means Algorithm - It takes input as the the number of clusters and clusters the data points as per the distance between a centroid-cluster points and points with minimum distance to the same cluster.

In Output, we print the Clsuter Created and the Count of Elements in Each Cluster. 
We also compare the Silhouette Score for both the clustering algorithms.


The main Project Files are 
ZooAnimals.py -> contains the classes used for data import.
main.py -> contains the main project code.
app.py -> contains the code for Streamlit instance for a brief display of data in browser.

Further, the animal data is imported from the zoo.xlsx file in the data folder.

References :

https://scikit-learn.org/stable/modules/clustering.html#affinity-propagation
https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AffinityPropagation.html
https://scikit-learn.org/stable/auto_examples/cluster/plot_affinity_propagation.html#sphx-glr-auto-examples-cluster-plot-affinity-propagation-py
https://www.youtube.com/shorts/qvtaazr6Ph0
https://scikit-learn.org/stable/auto_examples/cluster/plot_cluster_iris.html
https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_digits.html#sphx-glr-auto-examples-cluster-plot-kmeans-digits-py
ChatGPT


