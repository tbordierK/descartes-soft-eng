import numpy as np
from earthquakes.tools import get_haversine_distance
from earthquakes.tools import EARTH_RADIUS


def test_get_haversine_distance_same_point():
    point1 = (28, 12)
    point2 = (28, 12)
    expected_distance = 0
    assert get_haversine_distance(*point1, *point2) == expected_distance


def test_get_haversine_distance_antipodal_points():
    point1 = (0, 0)
    point2 = (0, 180)
    expected_distance = EARTH_RADIUS * np.pi
    np.testing.assert_allclose(
        get_haversine_distance(*point1, *point2), expected_distance, atol=1e-5
    )


def test_get_haversine_distancen_quarter_rotation_points():
    expected_distance = EARTH_RADIUS * np.pi * 90 / 180

    point1 = (90, 0)
    point2 = (0, 0)
    np.testing.assert_allclose(
        get_haversine_distance(*point1, *point2), expected_distance, atol=1e-5
    )

    point1 = (0, 90)
    point2 = (0, 0)
    np.testing.assert_allclose(
        get_haversine_distance(*point1, *point2), expected_distance, atol=1e-5
    )

    point1 = (0, 0)
    point2 = (90, 0)
    np.testing.assert_allclose(
        get_haversine_distance(*point1, *point2), expected_distance, atol=1e-5
    )

    point1 = (0, 0)
    point2 = (0, 90)
    np.testing.assert_allclose(
        get_haversine_distance(*point1, *point2), expected_distance, atol=1e-5
    )


def test_get_haversine_distance_fullrotation_points():
    expected_distance = 0
    point1 = (0, 0)
    point2 = (0, 360)
    np.testing.assert_allclose(
        get_haversine_distance(*point1, *point2), expected_distance, atol=1e-5
    )

