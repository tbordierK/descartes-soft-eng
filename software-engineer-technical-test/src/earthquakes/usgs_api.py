import urllib
from datetime import timedelta
import pandas as pd
import aiohttp


def get_earthquake_data(latitude, longitude, radius, minimum_magnitude, end_date):
    start_date = end_date - timedelta(days=(200 * 365))
    url = build_usgs_api_url(latitude, longitude, radius, minimum_magnitude, start_date, end_date)
    fcache = url.split('query?')[1] + '.csv'
    urllib.request.urlretrieve(url, fcache)
    earthquake_data = pd.read_csv(fcache)
    return earthquake_data


def build_api_url(endpoint, parameters):
    encoded_params = urllib.parse.urlencode(parameters)
    url = endpoint
    if encoded_params:
        url += "?" + encoded_params
    return url


def build_usgs_api_url(latitude, longitude, radius, minimum_magnitude, start_date, end_date):
    endpoint = 'https://earthquake.usgs.gov/fdsnws/event/1/query'
    parameters = {'format': 'csv',
                  'latitude': latitude,
                  'longitude': longitude,
                  'maxradiuskm': radius,
                  'minmagnitude': minimum_magnitude,
                  'starttime': str(start_date.date()),
                  'endtime': str(end_date.date())}
    url = build_api_url(endpoint, parameters)
    return url


async def get_earthquake_data_async(session, url):
    async with session.get(url) as response:
        filename = url.split('query?')[1] + '.csv'
        with open(filename, 'wb') as f_handle:
            while True:
                chunk = await response.content.read()
                if not chunk:
                    break
                f_handle.write(chunk)
        earthquake_data = pd.read_csv(filename)
        return earthquake_data


async def get_earthquake_data_for_multiple_locations(assets, radius, minimum_magnitude, end_date):
    start_date = end_date - timedelta(days=(200 * 365))
    urls = [build_usgs_api_url(lat, lon, radius, minimum_magnitude, start_date, end_date)
            for lat, lon in assets]
    multiple_data = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            single_earthquake_data = await get_earthquake_data_async(session, url)
            multiple_data.append(single_earthquake_data)
    return pd.concat(multiple_data).drop_duplicates()
