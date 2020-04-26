import osmium as osm

class OSMHandler(osm.SimpleHandler):
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.primary_nodes = []

    def way(self, o):
        if o.tags.get('highway') in ['primary', 'secondary', 'tertiary', 'trunk'] and 'name' in o.tags:
            temp = []
            for n in o.nodes:
                temp.append(n.ref)
            self.primary_nodes.append({'name': o.tags['name'].strip(), 'nodes': temp})