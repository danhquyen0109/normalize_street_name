import osmium as osm

class OSMHandler(osm.SimpleHandler):
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.primary_nodes = []

    def way(self, o):
        if o.tags.get('highway') in ['primary', 'secondary', 'tertiary', 'trunk'] and 'name' in o.tags:
            name = o.tags['name'].strip()
            if not o.tags['name'].strip().lower().startswith("đường") and not o.tags['name'].strip().lower().startswith("phố "):
                name = "Đường " + name
            temp = []
            for n in o.nodes:
                temp.append(n.ref)
            self.primary_nodes.append({'name': name, 'nodes': temp})
        if o.tags.get('highway') == 'residential' and 'name' in o.tags:
            if o.tags['name'].strip().lower().startswith("đường") or o.tags['name'].strip().lower().startswith("phố "):
                temp = []
                for n in o.nodes:
                    temp.append(n.ref)
                self.primary_nodes.append({'name': o.tags['name'].strip(), 'nodes': temp})