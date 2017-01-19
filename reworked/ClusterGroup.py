class ClusterGroup:
    def __init__(self, initial_cluster):
        self.clusters = [initial_cluster]
        self.initial_cluster = initial_cluster
        self.bounding_box = None

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

    def clean_cluster(self):
        reds = [cluster.red for cluster in self.clusters]
        white = self.initial_cluster.white
        for red in reds:
            if red.col_max > white.col_max and red.col_min < white.col_min:
                red.set_col_max(white.col_max)
                continue
            if red.get_width() / 2 > white.get_width() \
                    and white.col_max >= red.col_max >= white.col_min > red.col_min:
                red.set_col_min(int(white.col_min - white.get_width()))