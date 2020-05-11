import osmium as osm
import get_way_nodes

class StreetNormalizer(osm.SimpleHandler):

    def __init__(self):
        super(StreetNormalizer, self).__init__()
        self.osmhandler = get_way_nodes.OSMHandler()
        self.osmhandler.apply_file("/home/likk/data/vietnam.osm.pbf")
        self.street_nodes = self.osmhandler.primary_nodes

    def normalize(self, o):
        # new tags should be kept in a list so that the order is preserved
        newtags = []
        # pyosmium is much faster writing an original osmium object than
        # a osmium.mutable.*. Therefore, keep track if the tags list was
        # actually changed.
        modified = False
        for t in o.tags:
            if t.k != 'name':
                newtags.append(t)

        # Edit primary street's name
        if o.tags.get('highway') in ['primary', 'secondary', 'tertiary', 'trunk'] and 'name' in o.tags:
            if not o.tags['name'].strip().lower().startswith("đường") and not o.tags['name'].strip().lower().startswith("phố "):
                temp = "Đường " + o.tags['name']
                newtags.append(('name', temp))
                modified = True
            else:
                newtags.append(('name', o.tags['name']))
        # edit residential street's name
        elif o.tags.get('highway') == 'residential' and 'name' in o.tags:
            if not o.tags['name'].strip().lower().startswith("đường") and not o.tags['name'].strip().lower().startswith("phố "):
                temp = o.tags['name']
                if not o.tags['name'].strip().lower().startswith("ngõ") and not o.tags['name'].strip().lower().startswith("ngách") and not o.tags['name'].strip().lower().startswith("hẻm") and not o.tags['name'].strip().lower().startswith("đường") and not o.tags['name'].strip().lower().startswith("phố "):
                    temp = "Ngõ " + temp
                for each_street in self.street_nodes:
                    if o.nodes[0].ref in each_street['nodes'] and not o.tags['name'].strip().lower().endswith(each_street['name'].lower()):
                        temp = temp + " " + each_street['name']
                        break

                    # elif o.nodes[len(o.nodes) - 1].ref in each_street['nodes'] and not o.tags['name'].strip().lower().endswith(each_street['name'].lower()):
                    #     temp = temp + " " + each_street['name']
                    #     break
                newtags.append(('name', temp))
                modified = True
                
            else:
                newtags.append(('name', o.tags['name']))

        elif 'name' in o.tags:
            newtags.append(('name', o.tags['name']))
                
        if modified:
            # We have changed tags. Create a new object as a copy of the
            # original one with the tag list replaced.
            return o.replace(tags=newtags)
        else:
            return o

#     def node(self, o):
#         self.writer.add_node(o)

#     def way(self, o):
#         self.writer.add_way(self.normalize(o))

#     def relation(self, o):
#         self.writer.add_relation(o)


# if __name__ == '__main__':

#     # path to the output file (OSM or PBF)
#     # writer = osm.SimpleWriter("/home/likk/data/vietnam1.osm.pbf")
#     writer = osm.SimpleWriter("/home/likk/data/vietnam1.osm.pbf")
#     # path to the input file (PBF)
#     StreetNormalizer(writer).apply_file("/home/likk/data/vietnam.osm.pbf")
#     writer.close()
