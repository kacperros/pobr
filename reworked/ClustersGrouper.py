from reworked.ClusterGroup import ClusterGroup


class ClustersGrouper:
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
            if cluster.is_biedronka_cluster():
                clusters.append(cluster)
        self.clusters = clusters

    def __group_clusters(self):
        cluster_groups = {}
        for cluster in self.clusters:
            if cluster_groups.get(id(cluster.white)) is None:
                cluster_groups[id(cluster.white)] = ClusterGroup(cluster)
            else:
                cluster_groups[id(cluster.white)].add_cluster(cluster)
        self.cluster_groups = cluster_groups.values()
