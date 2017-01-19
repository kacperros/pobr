import numpy as np


class ClustersHandler:
    def __init__(self):
        self.clusters = []
        self.cluster_groups = []

    def add_cluster(self, cluster):
        self.clusters.append(cluster)

    def add_clusters(self, clusters):
        self.clusters.extend(clusters)

    def handle_clusters(self):
        self.__filter_out_bad_clusters()
        self.__group_clusters()
        return self.cluster_groups

    def __filter_out_bad_clusters(self):
        clusters = []
        for cluster in self.clusters:
            red = cluster[0]
            white = cluster[2][0]
            if red.distance(white) > np.sqrt((white.get_height()/3) ** 2 + (white.get_width()/3) ** 2):
                continue
            if red.get_width() * red.get_height() * 1.2 < white.get_width() * white.get_height():
                continue
            if len(cluster[1]) > 5:
                continue
            clusters.append(cluster)
        self.clusters = clusters

    def __group_clusters(self):
        self.cluster_groups = self.clusters

