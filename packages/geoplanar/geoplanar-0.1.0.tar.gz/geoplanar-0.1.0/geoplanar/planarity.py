"""
GeoPlanar

A module for handling planar enforcement for polygon geoseries.
"""

from geoplanar.overlap import trim_overlap, is_overlapping


import geopandas
import libpysal
import numpy
import pandas
from collections import defaultdict
from shapely.geometry import box, LineString, Polygon
from shapely.ops import split

def non_planar_edges(gdf):
    w = libpysal.weights.Queen.from_dataframe(gdf)
    intersections = gdf.sindex.query_bulk(gdf.geometry, predicate='intersects').T
    w1 = defaultdict(list)
    for i,j in intersections:
        if i != j:
            w1[i].append(j)
    missing = defaultdict(set)
    for key in w.neighbors:
        if set(w.neighbors[key]) != set(w1[key]):
            for value in w1[key]:
                pair = [key, value]
                pair.sort()
                l, r = pair
                missing[l] = missing[l].union([r])
    return missing

def holes(gdf):
    """Find holes in a geodataframe"""


    # get box
    b = box(*gdf.total_bounds)

    # form unary union
    u = gdf.unary_union

    # diff of b and u
    dbu = geopandas.GeoDataFrame(geometry=[b.difference(u)])

    # explode
    _holes = dbu.explode()

    # hull
    hull = gdf.dissolve().convex_hull

    # return holes
    _holes =  _holes[_holes.within(hull.geometry[0])]

    return _holes


def fill_holes(gdf):
    h = holes(gdf)
    for index, row in h.iterrows():
        #print(row.geometry.area)
        rdf = geopandas.GeoDataFrame(geometry=[row.geometry])
        neighbors = geopandas.sjoin(left_df=gdf,
                                   right_df=rdf,
                                   how='inner',
                                   op='intersects')
        largest = neighbors[neighbors.area==neighbors.area.max()]
        tmpdf = pandas.concat([largest, rdf]).dissolve()
        gdf.geometry[largest.index] = tmpdf.geometry[0]
        #print(largest.head())
    return gdf

def planar_enforce(gdf):
    uu = gdf.unary_union
    geoms = [uu.intersection(row.geometry) for index, row in gdf.iterrows()]
    return geopandas.GeoDataFrame(geometry=geoms)

def is_planar_enforced(gdf):
    if is_overlapping(gdf):
        return False
    if non_planar_edges(gdf):
        return False
    _holes = holes(gdf)
    if _holes.shape[0] > 0:
        return False
    return True

def check_validity(gdf):
    results = {}

    _edges = non_planar_edges(gdf)
    if _edges:
        results['edges'] = _edges

    return results

def fix_npe_edges(gdf):
    "Fix all npe intersecting edges in geoseries"
    edges = non_planar_edges(gdf)
    print(edges)
    for key in edges:
        poly_a = gdf.iloc[key].geometry
        for j in edges[key]:
            poly_b = gdf.iloc[j].geometry
            new_a, new_b = insert_intersections(poly_a, poly_b)
            poly_a = new_a
            gdf.geometry[key] = new_a
            gdf.geometry[j] = new_b
    return gdf

def insert_intersections(poly_a, poly_b):
    """Correct two npe intersecting polygons by inserting intersection points on intersecting edges
    """
    lin_a = LineString(list(poly_a.exterior.coords))
    lin_b = LineString(list(poly_b.exterior.coords))
    new_polys = []
    pts = lin_a.intersection(lin_b)
    for lin in [lin_a, lin_b]:
        splits = split(lin, pts)
        coords = [list(zip(*line.coords.xy)) for line in list(splits)]
        new_poly = coords[0]
        for coord in coords[1:]:
            if coord[0] == new_poly[-1]:
                new_poly.extend(coord[1:])
            else:
                new_poly.extend(coord)
        new_polys.append(Polygon(new_poly))
    return new_polys
