Hack Oregon Data API
# Permits Service

Using this API, you can query building permits in the City of Portland. 

### Purpose:

### Usage:

### Methods:
- <a href="#getBuildingPermits">Get Building Permits</a> - Query building permits in the City of Portland.


### API Reference:
Currently, we only have residential permit data for Portland. We hope to be able to offer commercial permit data soon. This means that when you want spatial data returned, you must always set the **option** parameter to 'residential'.

All parameters are passed in the URL query string and must be correctly URL encoded.
---
<a name="getBuildingPermits"></a>
#### Method: Get Building Permits:
Returns: A table or GeoJSON feature collection of building permits that satisfy the query. Each permit is returned with a Point feature representing the location (in long/lat decimal degrees) of the corresponding parcel and the following attributes: 
- id (unique record identifier)
- address (street address of the parcel)
- issuedate (date the permit was issued
- nbrhood (name of Portland neigborhood)
Response type: use the following file extensions:
- .geojson - return result as a GeoJSON feature collection
- .json - return result as a JSON formatted table

HTTP method: GET
URL endpoint: /services/permits

Not all query types support both data formats.
Parameters:
- **type** (required):
   - specify which type of permits to include in the result.
   - valid format: 'residential' 
   - example: `type=residential`
- **bounds** (optional):
   - bounding box of the query. Only permits that are located within this rectangle will be included in the result. The search bounding box is formatted as (x1, y1, x2, y2) in geographic coordinates (longitude, latitude). You should be able pass the output of Leaflet's  `Map.getBounds().toBBoxString()` method. Supply the coordinates as a clockwise oriented rectangle.
   - valid format: 2 comma delimited longitude & latitude pairs representing the lower left & upper right corners of the query rectangle: x1, y1, x2, y2
   - example: `bounds=-122.6,45.5,-122.58,45.51`
   - if not supplied, all permits will be returned. Be aware that this will return upwards of 7Mb of data to your application (which could make your application slow down a lot).
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
- **query** (optional):
   - this parameter is used to return the results of a pre-built query. This specifies the name of query to use.
   - valid formats: 
      - 'perNeighborhoodPerYear': return a table of the number of permits grouped by neighborhood by year. You must use the .json file extension as the only currently supported resource this method returns is a JSON formatted table. The result is structured as a 'rows' object containing a single list of rows each of which is a 3 element array: [count, year, neighborhood-name]
      - example: /services/permits.json?&type=residential&query=perNeighborhoodPerYear
   
---

### Data Sources:
Residential building permits: City of Portland...

### Appropriate Uses:

### Examples:
<span>1.</span> Return a GeoJSON feature collection of all the residential building permits in the specified bounding box that were issued after Jan 1st, 2015:
```
/services/permits.geojson?type=residential&bounds=-122.6,45.5,-122.58,45.51&startdate=2015-01-01
```
<span>2.</span> Return a GeoJSON feature collection of all residential permits in the Richmond & Sunnyside neighborhoods issues since Jan 1st, 2015:
```
/services/permits.geojson?type=residential&startdate=2015-01-01&neighborhood=richmond,sunnyside
```


###### Documentation ToDo:
- add more JS examples
- add specific leaflet examples?

