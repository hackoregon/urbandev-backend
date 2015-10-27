Hack Oregon Data API
# Neighborhood Service

Using this API, you can query the neighborhood boundaries in the City of Portland. The neighborhoods are returned as polygon spatial features formatted as GeoJSON suitable for drawing on a map.

### Purpose:

### Usage:

### Methods:
- <a href="#getNeighborhoods">Get neighborhood boundaries</a> - Fetch the neighborhood boundary polygons in the City of Portland.
- <a href="#getNeighborhoodList">Get neighborhood list</a> - Fetch the list of neighborhoods 
- <a href="#getNeighborhoodsListBbx">Get neighborhood bounding areas</a> - Fetch the list of neighborhoods and their extents

### API Reference:
All parameters are passed in the URL query string and must be correctly URL encoded.
---
<a name="getNeighborhoods"></a>
#### Method: Get Neighborhood Boundaries:
Returns: A GeoJSON feature collection of neighborhood boundaries that satisfy the query. Each neighborhood is returned as a Polygon or MultiPolygon feature representing the area shape of the corresponding neighborhood and the following attributes: 
- id (unique record identifier)
- name (name of neighborhood)

HTTP method: GET
URL endpoint: /services/neighborhoods.geojson

<a name="getNeighborhoodList"></a>
#### Method: Get Neighborhood List:
Returns: A JSON formatted table listing neighborhoods. The table contains the following attributes:
- name (name of neighborhood)

HTTP method: GET
URL endpoint: /services/neighborhoods.json

Parameters:
- **query** (required):
   - valid format: 'list'
   - example: query=list
   
- **city** (optional):
   - specify which city's neighborhoods to include in the result. 
   - valid format: 'portland' 
   - example: `city=portland`
   - leaving this parameter off (or set to a value other that 'portland' will return all neighborhoods in the Metro Portland area.

<a name="getNeighborhoodsListBbx"></a>
#### Method: Get Neighborhood List with bounding areas:
Returns: A JSON formatted table listing neighborhoods. The table contains the following attributes:
- name (name of neighborhood)
- JSON array describing a rectangle representing the bounds of the neighborhood in long / lat format

HTTP method: GET
URL endpoint: /services/neighborhoods.json

Parameters:
- **query** (required):
   - valid format: 'listWithBBX'
   - example: query=listWithBBX
   
- **city** (optional):
   - specify which city's neighborhoods to include in the result. 
   - valid format: 'portland' 
   - example: `city=portland`
   - leaving this parameter off (or set to a value other that 'portland' will return all neighborhoods in the Metro Portland area.


### Data Sources:

### Appropriate Uses:

### Examples:
