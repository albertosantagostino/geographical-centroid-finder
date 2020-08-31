#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sardinia centroid calculator

Input data: http://webgis2.regione.sardegna.it/catalogodati/card.jsp?uuid=R_SARDEG:QRHAF
Algorithm: geos::algorithm::Centroid
"""

import geopandas as gpd
import matplotlib.pyplot as plt

from pyproj import Transformer


def main():
    # Load file
    sardinia_df = gpd.read_file('data/lineaCostaPpr/lineaCostaPpr.shp')

    # Sort by area and get mainland shape
    sardinia_df['area'] = sardinia_df['geometry'].area
    mainland = sardinia_df.loc[sardinia_df['area'].idxmax()]['geometry']

    # Prepare figure and axes
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    # Get mainland shape (ignore some points at geoms[1])
    xs, ys = mainland.geoms[0].exterior.xy
    ax.fill(xs, ys, alpha=0.3, fc='b', ec='none')

    # Compute and plot the centroid
    centroid_x, centroid_y = mainland.geoms[0].centroid.x, mainland.geoms[0].centroid.y
    ax.plot(centroid_x, centroid_y, color='red', marker='o', markersize=2)

    # Convert coordinates from EPSG:3003
    transformer = Transformer.from_crs('epsg:3003', 'epsg:4326')
    centroid_lon, centroid_lat = transformer.transform(centroid_x, centroid_y)
    print(f"Centroid coordinates (lon, lat): {centroid_lon}, {centroid_lat}")

    # Show the figure
    plt.show()


if __name__ == '__main__':
    main()
