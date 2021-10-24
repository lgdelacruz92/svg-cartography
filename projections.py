# proper projection methods for each state
import requests
import pprint
from bs4 import BeautifulSoup

if __name__ == "__main__":
    # get the stateplanes
    state_plane_readme_html_req = requests.get('https://github.com/veltman/d3-stateplane')
    # pprint.pprint(state_plane_readme_html_req.headers['content-type'])
    html = state_plane_readme_html_req.text

    # html parser
    soup = BeautifulSoup(html, 'html.parser')
    readme_content = soup.find_all(attrs={"data-target": 'readme-toc.content'})[0]
    state_planes = readme_content.article.find_all(recursive=False)[7:25]
    for i in range(0, len(state_planes), 2):
        print(state_planes[i].text, state_planes[i+1].name)
        print(state_planes[i+1].text.replace('var projection = ', ''))

    # for tag in soup.find_all():
    #     if tag.has_attr('data-target') and tag.attrs.get('readme-toc.content'):
    #         print(tag)