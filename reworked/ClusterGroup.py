class ClusterGroup:
    def __init__(self, initial_cluster):
        self.clusters = [initial_cluster]
        self.initial_cluster = initial_cluster

    def add_cluster(self, cluster):
        if id(self.initial_cluster.white) == id(cluster.white) and \
                        id(self.initial_cluster) != id(cluster):
            self.clusters.append(cluster)

    def add_clusters(self, clusters):
        for cluster in clusters:
            self.add_cluster(cluster)

    def get_id(self):
        return id(self.initial_cluster.white)

    def get_boxes(self):
        boxes = []
        for cluster in self.clusters:
            boxes.extend(cluster.get_boxes())
        return boxes
