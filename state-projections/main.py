import os
if __name__ == "__main__":
    year = '2019'
    fip = '02'
    os.system(f'curl "https://www2.census.gov/geo/tiger/GENZ{year}/shp/cb_{year}_{fip}_tract_500k.zip" -o cb_{year}_{fip}_tract_500k.zip')
    os.system(f'unzip cb_{year}_{fip}_tract_500k.zip')