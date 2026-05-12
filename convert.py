import json
import sys

with open('package/states-albers-10m.json') as f:
    topo = json.load(f)

transform = topo.get('transform')
scale = transform['scale']
translate = transform['translate']
arcs_raw = topo['arcs']

def decode_arc(arc):
    x = 0; y = 0; pts = []
    for dx, dy in arc:
        x += dx; y += dy
        pts.append((x * scale[0] + translate[0], y * scale[1] + translate[1]))
    return pts

decoded_arcs = [decode_arc(a) for a in arcs_raw]

def arc_points(idx):
    return decoded_arcs[idx] if idx >= 0 else list(reversed(decoded_arcs[~idx]))

def ring_points(ring_idxs):
    points = []
    for i, idx in enumerate(ring_idxs):
        pts = arc_points(idx)
        if i == 0:
            points.extend(pts)
        else:
            points.extend(pts[1:])
    return points

def polygon_centroid(ring):
    # signed-area centroid of a closed ring
    A = 0.0; Cx = 0.0; Cy = 0.0
    n = len(ring)
    for i in range(n):
        x0, y0 = ring[i]
        x1, y1 = ring[(i+1) % n]
        cross = x0 * y1 - x1 * y0
        A += cross
        Cx += (x0 + x1) * cross
        Cy += (y0 + y1) * cross
    A *= 0.5
    if A == 0:
        # fallback to bbox center
        xs = [p[0] for p in ring]; ys = [p[1] for p in ring]
        return ((min(xs)+max(xs))/2, (min(ys)+max(ys))/2)
    return (Cx / (6*A), Cy / (6*A))

def polygon_area(ring):
    A = 0.0; n = len(ring)
    for i in range(n):
        x0, y0 = ring[i]; x1, y1 = ring[(i+1) % n]
        A += x0 * y1 - x1 * y0
    return abs(A) / 2.0

fips_to_usps = {
    '01':'AL','02':'AK','04':'AZ','05':'AR','06':'CA','08':'CO','09':'CT','10':'DE',
    '11':'DC','12':'FL','13':'GA','15':'HI','16':'ID','17':'IL','18':'IN','19':'IA',
    '20':'KS','21':'KY','22':'LA','23':'ME','24':'MD','25':'MA','26':'MI','27':'MN',
    '28':'MS','29':'MO','30':'MT','31':'NE','32':'NV','33':'NH','34':'NJ','35':'NM',
    '36':'NY','37':'NC','38':'ND','39':'OH','40':'OK','41':'OR','42':'PA','44':'RI',
    '45':'SC','46':'SD','47':'TN','48':'TX','49':'UT','50':'VT','51':'VA','53':'WA',
    '54':'WV','55':'WI','56':'WY'
}

def fmt(n):
    return f"{round(n, 1):g}"

out = {}
centroids = {}

for geom in topo['objects']['states']['geometries']:
    fips = geom['id']
    code = fips_to_usps.get(fips)
    if not code:
        continue
    name = geom['properties']['name']
    if geom['type'] == 'Polygon':
        polygons = [geom['arcs']]
    elif geom['type'] == 'MultiPolygon':
        polygons = geom['arcs']
    else:
        continue
    paths = []
    largest_area = 0
    largest_centroid = None
    for poly in polygons:
        outer_pts = ring_points(poly[0])
        if not outer_pts:
            continue
        area = polygon_area(outer_pts)
        if area > largest_area:
            largest_area = area
            largest_centroid = polygon_centroid(outer_pts)
        for ring in poly:
            pts = ring_points(ring)
            if not pts:
                continue
            d = f"M{fmt(pts[0][0])},{fmt(pts[0][1])}"
            for p in pts[1:]:
                d += f"L{fmt(p[0])},{fmt(p[1])}"
            d += "Z"
            paths.append(d)
    out[code] = {'n': name, 'd': "".join(paths)}
    if largest_centroid:
        centroids[code] = [round(largest_centroid[0], 1), round(largest_centroid[1], 1)]

with open('paths.json', 'w') as f:
    json.dump({'paths': out, 'centroids': centroids}, f, separators=(',',':'))

import os
print(f'states: {len(out)}, file: {os.path.getsize("paths.json")} bytes', file=sys.stderr)
