from .config import *
# This file accesses the data
import osmnx as ox
import matplotlib.pyplot as plt
import math

def print_message():
    return 'access loaded'

def plot_city_map(place_name, latitude, longitude, box_size_km=2, poi_tags=None):
    """
    Plot a simple city map with area boundary, buildings, roads, nodes, and optional POIs.

    Parameters
    ----------
    place_name : str
        Name of the place (used for boundary + plot title).
    latitude, longitude : float
        Central coordinates.
    box_size_km : float
        Size of the bounding box in kilometers (default 2 km).
    poi_tags : dict, optional
        Tags dict for POIs (e.g. {"amenity": ["school", "restaurant"]}).
    """

    # convert km to degrees
    lat_offset = (box_size_km / 2) / 111
    lon_offset = (box_size_km / 2) / (111*math.cos(math.radians(latitude)))

    north = latitude + lat_offset
    south = latitude - lat_offset
    east  = longitude + lon_offset
    west  = longitude - lon_offset
    bbox = (west, south, east, north)

    # Query area boundary
    area = ox.geocode_to_gdf(place_name).to_crs(epsg=4326)

    # Buildings
    buildings = ox.features_from_bbox(bbox, tags={"building": True})

    # Road graph
    graph = ox.graph_from_bbox(bbox, network_type="all")
    nodes, edges = ox.graph_to_gdfs(graph)

    # Optional POIs
    pois = None
    if poi_tags:
        pois = ox.features_from_bbox(bbox, tags=poi_tags)

    # Plot
    fig, ax = plt.subplots(figsize=(6,6))
    area.plot(ax=ax, color="tan", alpha=0.5)
    if not buildings.empty:
        buildings.plot(ax=ax, facecolor="gray", edgecolor="gray")
    edges.plot(ax=ax, linewidth=1, edgecolor="black", column=None, alpha=0.3)
    nodes.plot(ax=ax, color="black", markersize=1, column=None, alpha=0.3)
    if pois is not None and not pois.empty:
        pois.plot(ax=ax, color="green", markersize=5, alpha=1)
    ax.set_xlim(west, east)
    ax.set_ylim(south, north)
    ax.set_title(place_name, fontsize=14)
    plt.show()
