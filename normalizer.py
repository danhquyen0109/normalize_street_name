import osmium as osm
import street_normalizer
import node_normalizer

class Normalizer(osm.SimpleHandler):
    def __init__(self, writer):
        super(Normalizer, self).__init__()
        self.writer = writer

    def node(self, o):
        self.writer.add_node(node_normalizer.NodeNormalizer().normalize(o))
    
    def way(self, o):
        # polygons
        if "addr:street" in o.tags:
            self.writer.add_way(node_normalizer.NodeNormalizer().normalize(o))
        # streets
        else:
            self.writer.add_way(street_normalizer.StreetNormalizer().normalize(o))

    def relation(self, o):
        self.writer.add_relation(o)

if __name__ == '__main__':

    # path to the output file (OSM or PBF)
    # writer = osm.SimpleWriter("/home/likk/data/vietnam-normalizer.osm")
    writer = osm.SimpleWriter("/home/likk/data/vietnam-normalizer.osm.pbf")
    # path to the input file (PBF)
    Normalizer(writer).apply_file("/home/likk/data/vietnam.osm.pbf")
    writer.close()
    print('done!')