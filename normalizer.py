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
        self.writer.add_way(street_normalizer.StreetNormalizer().normalize(o))

    def relation(self, o):
        self.writer.add_relation(o)

if __name__ == '__main__':

    # path to the output file (OSM or PBF)
    # writer = osm.SimpleWriter("/home/likk/data/vietnam1.osm.pbf")
    writer = osm.SimpleWriter("/home/likk/data/xuanthuy1.osm")
    # path to the input file (PBF)
    Normalizer(writer).apply_file("/home/likk/data/xuanthuy.osm.pbf")
    writer.close()