hi, this is README
# Animal project presentation
This dataset consists of 101 animals from a zoo.
There are 16 variables with various traits to describe the animals.
The 7 Class Types are: Mammal, Bird, Reptile, Fish, Amphibian, Bug and Invertebrate
## Project goals

I was curious about how different algorithms could predict the class of an animal, so I implemented different classification algorithms in order to compare their accuracy and have a glimpse of which feature(s) were the most relevant to efficiently classify the animals.
Then I 'transfered' to an  unsupervised approach, that is, without observing the class of each animal species, I group the animal species in different clusters based on their features.

Comparing the result of each algorithm, show which clustering algorithm better approximates the classes provided by the dataset.

It is therefore required not only to define a methodology for comparing the clustering results with the expected classification, but also to briefly describe the distinguishing characteristics of each species cluster produced by the algorithm under evaluation.

# Table of contents
importing libraries and datasets

visualizing the class types distribution

preparing data for algorithms implementations
  - splitting data
  - feature scaling

algorthm implementation
 - K Nearest Neighbors
   - implementation 
   - prediction
   - accuracy
   - results comparison
 - Decision Tree
   - implementation 
   - prediction
   - accuracy
   - results comparison
 - Random Forest
   - implementation
   - prediction
   - accuracy
   - results comparison
 - Support Vector Machine
   - implementation
   - prediction
   - accuracy
   - results comparison
 - Naive Bayes
   - implementation
   - prediction
   - accuracy
   - results comparison 
 - algorithm comparison
 - correlation analysis
 - K Means Clustering
   - implementation
   - elbow method
   - visualization