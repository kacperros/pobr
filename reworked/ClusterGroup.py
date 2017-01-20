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

    def is_biedronka(self):
        if 1 > len(self.clusters) > 2:
            return False
        if len(self.clusters) == 2:
            return self.__reds_overlap() and self.__blacks_are_dots() \
                   and self.__head_is_one_half_of_body() and self.__width_proportions_ok()
        else:
            if self.__blacks_are_dots() and self.__head_is_one_half_of_body():
                self.clean_cluster()
                return True
            else:
                return False

    def clean_cluster(self):
        if len(self.clusters) == 1:
            red = self.clusters[0].red
            red.set_col_min(red.col_min - int(red.get_width()/2))
            red.set_row_min(red.row_min - int(red.get_height()/2))
        elif len(self.clusters) == 2:
            l_cluster = self.clusters[0]
            r_cluster = self.clusters[1]
            if l_cluster.red.col_min > r_cluster.red.col_min:
                l_cluster = self.clusters[1]
                r_cluster = self.clusters[0]
            self.__adjust_left(l_cluster)
            self.__adjust_right(r_cluster)

    def __adjust_left(self, cluster):
        red = cluster.red
        current_min = 1000000
        for black in cluster.blacks:
            current_min = min(current_min, black.col_min)
        red.set_col_min(current_min)

    def __adjust_right(self, cluster):
        red = cluster.red
        current_max = 0
        for black in cluster.blacks:
            current_min = max(current_max, black.col_max)
        red.set_col_max(current_max)

    def box_cluster(self):
        boxes = self.get_boxes()
        bounding = self.initial_cluster.white
        for box in boxes:
            bounding = bounding.combine(box)
        return bounding

    def __reds_overlap(self):
        return self.clusters[0].red.distance(self.clusters[1].red) == 0

    def __blacks_are_dots(self):
        non_blacks = len(self.clusters)
        for cluster in self.clusters:
            for black in cluster.blacks:
                if not 0.7 <= len(black.pixel_coords) / black.get_box_area() <= 1.0:
                    non_blacks -= 1
        return non_blacks >= 0

    def __head_is_one_half_of_body(self):
        for cluster in self.clusters:
            if cluster.red.get_height() > cluster.white.get_height() * 2.5:
                return False
        return True

    def __width_proportions_ok(self):
        for cluster in self.clusters:
            if cluster.red.get_width() > cluster.white.get_width() * 2:
                return False
            return True
