import osmium as osm
import street_normalizer as street
import re
import unicodedata

class NodeNormalizer(osm.SimpleHandler):

    def __init__(self):
        super(NodeNormalizer, self).__init__()
        # self.writer = writer

    def normalize(self, o):
        # new tags should be kept in a list so that the order is preserved
        newtags = []
        # pyosmium is much faster writing an original osmium object than
        # a osmium.mutable.*. Therefore, keep track if the tags list was
        # actually changed.
        modified = False
        for t in o.tags:
            if t.k != 'addr:street' and t.k != 'addr:housenumber':
                newtags.append(t)
        
        if "addr:housenumber" in o.tags:

            # normalize string diacritics
            housenumber = o.tags['addr:housenumber'].strip().lower()
            normal = unicodedata.normalize('NFD', housenumber).encode('ASCII', 'ignore')
            housenumber = normal.decode('ASCII')
            
            # replace common vietnamese label
            housenumber = re.sub('nha so|ns|so nha|sn|lo so|day nha|dn', '', housenumber).strip()
            housenumber = re.sub('so|number|no|s|lo', '', housenumber).strip()

            # replace special characters except these "-/\|,:;"
            housenumber = re.sub('[!@#$%^&*()\[\]\{\}.<>?`~=_+]', '', housenumber).strip()

            # eg: 2-4-6 -> 4
            if re.match("^([0-9]+)([|-])([0-9]+)([|-])([0-9]+)$", housenumber):
                split = re.split("^([0-9]+)([|-])([0-9]+)([|-])([0-9]+)$", housenumber)
                newtags.append(('addr:housenumber', split[3]))
                modified = True
                if "addr:street" in o.tags:
                    street = o.tags['addr:street'].strip().lower()
                    if not street.startswith("ngõ") and not street.startswith("ngách") and not street.startswith("hẻm") and not street.startswith("đường") and not street.startswith("phố "):
                        temp = "Đường " + o.tags['addr:street']
                        newtags.append(('addr:street', temp))
                        modified = True
                    else:
                        newtags.append(('addr:street', o.tags['addr:street']))

            #eg: 2-4 -> 2
            elif re.match("^([0-9]+)([|-])([0-9]+)$", housenumber):
                split = re.split("^([0-9]+)([|-])([0-9]+)$", housenumber)
                newtags.append(('addr:housenumber', split[1]))
                modified = True

                if "addr:street" in o.tags:
                    street = o.tags['addr:street'].strip().lower()
                    if not street.startswith("ngõ") and not street.startswith("ngách") and not street.startswith("hẻm") and not street.startswith("đường") and not street.startswith("phố "):
                        temp = "Đường " + o.tags['addr:street']
                        newtags.append(('addr:street', temp))
                        modified = True
                    else:
                        newtags.append(('addr:street', o.tags['addr:street']))

            # eg: 2/4/6 -> housenumber = 2, street name = "ngõ 4/6"
            elif re.match("^([0-9]+)([\/])([0-9]+)([\/])([0-9]+)$", housenumber):
                split = re.split("^([0-9]+)([\/])([0-9]+)([\/])([0-9]+)$", housenumber)
                newtags.append(('addr:housenumber', split[1]))
                modified = True

                if "addr:street" not in o.tags:
                    temp = "Ngõ " + str(split[3]) +"/"+ str(split[5])
                    newtags.append(('addr:street', temp))
                    modified = True
                else:
                    street = o.tags['addr:street'].strip().lower()
                    if not street.startswith("ngõ") and not street.startswith("ngách") and not street.startswith("hẻm") and not street.startswith("đường") and not street.startswith("phố "):
                        temp =  "Ngõ " + str(split[3]) +"/"+ str(split[5]) + " đường " + o.tags['addr:street']
                        newtags.append(('addr:street', temp))
                        modified = True
                    elif street.startswith("đường") or street.startswith("phố "):
                        temp =  "Ngõ " + str(split[3]) +"/"+ str(split[5]) + " " + o.tags['addr:street']
                        newtags.append(('addr:street', temp))
                        modified = True
                    else:
                        newtags.append(('addr:street', o.tags['addr:street']))
            # eg: 2/4 -> housenumber = 2, street's name = "ngõ 4"
            elif re.match("^([0-9]+)([\/])([0-9]+)$", housenumber):
                split = re.split("^([0-9]+)([\/])([0-9]+)$", housenumber)
                newtags.append(('addr:housenumber', split[1]))
                modified = True    

                if "addr:street" not in o.tags:
                    temp = "Ngõ " + str(split[3])
                    newtags.append(('addr:street', temp))
                    modified = True
                else:
                    street = o.tags['addr:street'].strip().lower()
                    if not street.startswith("ngõ") and not street.startswith("ngách") and not street.startswith("hẻm") and not street.startswith("đường") and not street.startswith("phố "):
                        temp =  "Ngõ " + str(split[3]) + " đường " + o.tags['addr:street']
                        newtags.append(('addr:street', temp))
                        modified = True
                    elif street.startswith("đường") or street.startswith("phố "):
                        temp =  "Ngõ " + str(split[3]) + " " + o.tags['addr:street']
                        newtags.append(('addr:street', temp))
                        modified = True
                    else:
                        newtags.append(('addr:street', o.tags['addr:street']))

            else:
                newtags.append(('addr:housenumber', housenumber))
                modified = True

                if "addr:street" in o.tags:
                    street = o.tags['addr:street'].strip().lower()
                    if not street.startswith("ngõ") and not street.startswith("ngách") and not street.startswith("hẻm") and not street.startswith("đường") and not street.startswith("phố "):
                        temp = "Đường " + o.tags['addr:street']
                        newtags.append(('addr:street', temp))
                        modified = True
                    else:
                        newtags.append(('addr:street', o.tags['addr:street']))
        else:
            if "addr:street" in o.tags:
                street = o.tags['addr:street'].strip().lower()
                if not street.startswith("ngõ") and not street.startswith("ngách") and not street.startswith("hẻm") and not street.startswith("đường") and not street.startswith("phố "):
                    temp = "Đường " + o.tags['addr:street']
                    newtags.append(('addr:street', temp))
                    modified = True
                else:
                    newtags.append(('addr:street', o.tags['addr:street']))

        if modified:
            # We have changed tags. Create a new object as a copy of the
            # original one with the tag list replaced.
            return o.replace(tags=newtags)
        else:
            return o
        