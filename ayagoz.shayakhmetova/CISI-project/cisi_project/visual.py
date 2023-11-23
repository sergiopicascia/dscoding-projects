import matplotlib.pyplot as plt
import pandas as pd

class VisualData:
    def __init__(self, file_path):
        self.dataset = pd.read_csv(file_path)

    def create_line_chart(self):
        plt.figure(figsize=(10, 6))
        data_counts = self.dataset['release_date_duplicate'].value_counts().sort_index()
        plt.plot(data_counts.index, data_counts.values, marker='o')
        plt.xlabel('Release Date Duplicate')
        plt.ylabel('Number of movies')
        plt.grid(True)
        return plt.gcf()
    
    def create_pie_chart_runtime(self):
        runtime_intervals = ['< 90', '90-120', '120-150', '> 150']
        runtime_counts = pd.cut(self.dataset['runtime'], bins=[0, 90, 120, 150, float('inf')], labels=runtime_intervals, right=False).value_counts()
        plt.figure(figsize=(8, 8))
        plt.pie(runtime_counts, labels=runtime_counts.index, autopct=lambda p: '{:.0f}'.format(p * sum(runtime_counts)/100), startangle=140)
        plt.axis('equal')
        return plt.gcf()
    
    def create_scatter_plot(self):
        plt.figure(figsize=(10, 6))
        plt.scatter(self.dataset['vote_count'], self.dataset['vote_average'], alpha=0.5)
        plt.xlabel('Vote Count')
        plt.ylabel('Vote Average')
        plt.grid(True)
        return plt.gcf()    
