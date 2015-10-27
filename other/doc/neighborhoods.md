Hack Oregon Data API
# Neighborhood Service

Using this API, you can query the neighborhood boundaries in the City of Portland. The neighborhoods are returned as polygon spatial features formatted as GeoJSON suitable for drawing on a map.

### Purpose:

### Usage:

### Methods:
- <a href="#getNeighborhoods">Get neighborhood boundaries</a> - Fetch the neighborhood boundary polygons in the City of Portland.

### API Reference:
All parameters are passed in the URL query string and must be correctly URL encoded.
---
<a name="getNeighborhoods"></a>
#### Method: Get Neighborhood Boundaries:
Returns: A GeoJSON feature collection of neighborhood boundaries that satisfy the query. Each neighborhood is returned as a Polygon or MultiPolygon feature representing the area shape of the corresponding neighborhood and the following attributes: 
- id (unique record identifier)
- name (name of neighborhood)

### Data Sources:

### Appropriate Uses:

### Examples:

