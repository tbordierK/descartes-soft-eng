from datetime import datetime
import numpy as np

EARTH_RADIUS = 6378

TIME_COLUMN = "time"
PAYOUT_COLUMN = "payout"
MAGNITUDE_COLUMN = "mag"
DISTANCE_COLUMN = "distance"
LATITUDE_COLUMN = "latitude"
LONGITUDE_COLUMN = "longitude"


def get_haversine_distance(earthquake_latitudes,
                           earthquake_longitudes,
                           asset_latitude,
                           asset_longitude):
    earthquake_latitudes_rad = earthquake_latitudes * np.pi / 180
    earthquake_longitudes_rad = earthquake_longitudes * np.pi / 180
    asset_latitude_rad = asset_latitude * np.pi / 180
    asset_longitude_rad = asset_longitude * np.pi / 180

    h = (np.sin((earthquake_latitudes_rad - asset_latitude_rad) / 2)) ** 2 \
        + np.cos(earthquake_latitudes_rad) * np.cos(asset_latitude_rad) * (
            np.sin((earthquake_longitudes_rad - asset_longitude_rad) / 2)) ** 2

    haversine_distance = 2 * EARTH_RADIUS * np.arcsin(np.sqrt(h))
    return haversine_distance


def compute_payouts(earthquake_data, payout_structure):
    payouts = []
    for _, event in earthquake_data.iterrows():
        radius_condition = event.distance <= payout_structure.Radius
        magnitude_condition = event.mag >= payout_structure.Magnitude
        payout = payout_structure[radius_condition & magnitude_condition].Payout.values
        payout = np.max(payout, initial=0)
        payouts.append(payout)

    earthquake_data['payout'] = payouts
    earthquake_data['year'] = [
        datetime.strptime(w, "%Y-%m-%dT%H:%M:%S.%f%z").year for w in earthquake_data.time
    ]
    payout_per_year = earthquake_data[['year', 'payout']].groupby('year').max()
    return payout_per_year


def compute_burning_cost(payouts, start_year, end_year):
    return np.sum(payouts.loc[start_year:end_year]) / (end_year - start_year + 1)
