import os
import argparse
from bs4 import BeautifulSoup
import requests

parser = argparse.ArgumentParser(description='Project state')
parser.add_argument('-y', '--year', help='Year of the census.',required=True)
parser.add_argument('-f', '--fips', help='State fips.',required=True)

args = parser.parse_args()

import requests
import pprint
from bs4 import BeautifulSoup

def get_projections():
    state_plane_readme_html_req = requests.get('https://github.com/veltman/d3-stateplane')
    html = state_plane_readme_html_req.text

    # html parser
    soup = BeautifulSoup(html, 'html.parser')
    readme_content = soup.find_all(attrs={"data-target": 'readme-toc.content'})[0]
    state_planes = readme_content.article.find_all(recursive=False)[3:]
    projections = []
    for i in range(0, len(state_planes), 2):
        projection = state_planes[i+1].text.replace('var projection = ', '').replace('\n','').replace(' ', '').replace(';','')
        projections.append(projection)
    return (state_planes[i].text, projections)

def create_topojson_and_geojson(year, fips):
    os.system(f'npx shp2json cb_{year}_{fips}_tract_500k.shp -o geoData.json')

    # TODO: this needs adjusting to be general
    alaska_projections = get_projections()

    for i, projection in enumerate(alaska_projections):
        print('processing', i)
        os.system(f'geoproject "{projection}.fitSize([960, 960], d)" < geoData.json > geo-albers-{i}.json')

        os.system('''
            ndjson-split 'd.features' \
                < geo-albers-%d.json \
                > geo-albers-%d.ndjson
        ''' % (i, i))

        os.system('''
            ndjson-map 'd.id = d.properties.GEOID.slice(0, 5), d' \
                < geo-albers-%d.ndjson \
                > geo-albers-id-%d.ndjson
        ''' % (i, i))

        os.system('''
            ndjson-reduce \
                < geo-albers-id-%d.ndjson \
                | ndjson-map '{type: "FeatureCollection", features: d}' \
                > geo-albers-%d.json
        ''' % (i, i))

        os.system('''
            npx ndjson-split 'd.features' \
                < geo-albers-%d.json \
                > geo-albers-%d.ndjson
        ''' % (i, i))

        os.system('''
            geo2topo -n \
                tracts=geo-albers-%d.ndjson \
                > geo-tracts-topo-%d.json
            ''' % (i, i)
        )

        os.system('''
            toposimplify -p 1 -f \
                < geo-tracts-topo-%d.json \
                > geo-simple-topo-%d.json
        ''' % (i, i))

        os.system('''
            topoquantize 1e5 \
                < geo-simple-topo-%d.json \
                > geo-quantized-topo-%d.json
        ''' % (i,i))

        os.system('''
            topomerge -k 'd.id' counties=tracts \
                < geo-quantized-topo-%d.json \
                > geo-county-min-topojson-%d.json
        ''' % (i, i))

        os.system('''
            topo2geo counties=- \
                < geo-county-min-topojson-%d.json > geo-county-min-%d.json
        ''' % (i, i))

    # clean up (comment out for debugging)
    os.system('rm *.ndjson')
    os.system('rm *topo-*.json')
    os.system('rm *albers*.json')
    os.system('rm geoData.json')

if __name__ == '__main__':
    pass
    # os.system('''
    # ndjson-split 'd.features' \
    #     < fl-counties-topo.json \
    #     > fl-counties-topo.ndjson
    # ''')
    # os.system('''
    # geo2svg -n -p 1 -w 960 -h 960 \
    #     < fl-counties-topo.ndjson \
    #     > fl-counties-topo.svg
    # ''')
    # os.system("curl 'https://api.census.gov/data/2019/acs/acs5/profile?get=DP05_0006PE&for=county:*&in=state:12' -o census-20-to-24.json")
    # os.system('''
    # ndjson-cat census-20-to-24.json \
    #     | ndjson-split 'd.slice(1)' \
    #     | ndjson-map '{id: d[1] + d[2], percent: d[0]}' \
    #     > census-20-to-24.ndjson
    # ''')
    # os.system('''
    #     ndjson-join 'd.id' \
    #         fl-counties-topo.ndjson \
    #         census-20-to-24.ndjson \
    #         > fl-counties-census-join.ndjson
    # ''')
    # os.system('python3 main.py fl-counties-census-join.ndjson > fl-counties-census-color.ndjson')
    # os.system('''
    # geo2svg -n --stroke none -p 1 -w 960 -h 960 \
    #     < fl-counties-census-color.ndjson \
    #     > fl-counties-census-color.svg
    # ''')