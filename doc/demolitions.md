Hack Oregon Data API
# Demolitions Service

Using this API, you can query demolitions data for Portland. This data may be moved into the Permits API in the future.

### Purpose:

### Usage:

### Methods:
- <a href="#getBuildingDemolitions">Get Demolitions</a> - Query residential demolitions in the City of Portland.

### API Reference:
Currently, we only have residential demolition data for Portland. We may be able to offer commercial data soon at some time in the future. This means that when you want spatial data returned, you must always set the **option** parameter to 'residential'.

All parameters are passed in the URL query string and must be correctly URL encoded.
---
<a name="getBuildingDemolitions"></a>
#### Method: Get Demolitions:
Returns: A GeoJSON feature collection of demolition permits that satisfy the query. Each permit is returned with a Point feature representing the location (in long/lat decimal degrees) of the corresponding building and the following attributes: 
- id (unique record identifier)
- address (street address of the parcel)
- demolition_date (date of demolition permit?)
- neighborhood (name of Portland neigborhood)
Response type: use the following file extensions:
- .geojson - return result as a GeoJSON feature collection

HTTP method: GET
URL endpoint: /services/demolitions

Parameters:
- **type** (required):
   - specify which type of permits to include in the result.
   - valid format: 'residential' 
   - example: `type=residential`
- **bounds** (optional):
   - bounding box of the query. Only permits that are located within this rectangle will be included in the result. The search bounding box is formatted as (x1, y1, x2, y2) in geographic coordinates (longitude, latitude). You should be able pass the output of Leaflet's  `Map.getBounds().toBBoxString()` method. Supply the coordinates as a clockwise oriented rectangle.
   - valid format: 2 comma delimited longitude & latitude pairs representing the lower left & upper right corners of the query rectangle: x1, y1, x2, y2
   - example: `bounds=-122.6,45.5,-122.58,45.51`
   - if not supplied, all permits will be returned. Be aware that this may return a lot of data.
- **startdate** (optional):
   - the starting permit issue date. The result will only contain permits that were issued on or after this date (inclusive).
   - valid format: ISO formatted date (yyyy-mm-dd)
   - example: `startdate=2005-01-01` - return all permits issued on or after Jan 1st, 2005
- **enddate** (optional):
   - the ending permit issue date. The result will only contain permits that were issued on or before this date (inclusive).
   - valid format: ISO formatted date (yyyy-mm-dd)
   - example: `enddate=2005-06-01` - return all permits issued on or before Jun 1st, 2005
- **neighborhood** (optional):
   - a comma delimited list of neighborhoods. The result will contain permits located only in the specified neighborhood(s).
   - example: `neighborhood=richmond,overlook`
   - note: since this limits the spatial extent of the query, be careful when combining this option with the **bounds** option as a permit must be both within the bounds and in one of the specified neighborhoods to be in the result.
   
### Data Sources:
Residential building permits: City of Portland...

### Appropriate Uses:

### Examples:
