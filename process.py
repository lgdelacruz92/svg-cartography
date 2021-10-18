import os

if __name__ == '__main__':
    os.system('npx shp2json cb_2019_12_tract_500k.shp -o fl.json')
    os.system("geoproject 'd3.geoConicConformal().parallels([29 + 35 / 60, 30 + 45 / 60]).rotate([84 + 30 / 60, 0]).fitSize([960, 960], d)' < fl.json > fl-albers.json")
    os.system('''
    npx ndjson-split 'd.features' \
        < fl-albers.json \
        > fl-albers.ndjson
    ''')
    os.system('''
    geo2topo -n \
        tracts=fl-albers.ndjson \
        > fl-tracts-topo.json
    '''
    )
    os.system('''
    toposimplify -p 1 -f \
        < fl-tracts-topo.json \
        > fl-simple-topo.json
    ''')
    os.system('''
    topoquantize 1e5 \
        < fl-simple-topo.json \
        > fl-quantized-topo.json
    ''')
    os.system('''
    topomerge -k 'd.properties.GEOID.slice(2, 5)' counties=tracts \
        < fl-quantized-topo.json \
        > fl-merge-topo.json
    ''')
    os.system('''
    topo2geo counties=- \
        < fl-merge-topo.json > fl-counties-topo.json
    ''')
    os.system('''
    ndjson-split 'd.features' \
        < fl-counties-topo.json \
        > fl-counties-topo.ndjson
    ''')
    os.system('''
    geo2svg -n -p 1 -w 960 -h 960 \
        < fl-counties-topo.ndjson \
        > fl-counties-topo.svg
    ''')