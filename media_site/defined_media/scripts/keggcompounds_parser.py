import re

class KeggCompoundsParser(object):
    def __init__(self, kegg_fn):
        self.kegg_fn=kegg_fn

    def next(self):
        with open(self.kegg_fn) as f:
            for line in f:
                line=line.strip()
#                print 'line: %s' % line
                mg=re.search(r'^ENTRY\s+(C\d+)', line)
                if mg:
                    kegg_id=mg.group(1)
#                    print 'got kegg_id: %s' % kegg_id
                    continue
                mg=re.search(r'^FORMULA\s+(\w+)', line)
                if mg:
                    formula=mg.group(1)
                    try:
#                        print 'yielding %s, %s' % (kegg_id, formula)
                        yield kegg_id, formula
                    except NameError: # kegg_id
                        pass


    def __iter__(self):
        return self

if __name__=='__main__':
    kegg_fn='/home/ISB/vcassen/l/media-db/dumps/keggcompounds.txt'
    parser=KeggCompoundsParser(kegg_fn)
    for kegg_id, formula in parser.next():
#        print 'tup is %s' % (tup)
        print '%s, %s' % (kegg_id, formula)

    
