# Script: PortalDependenciesVisualization
**Creator:** Tanner Hammond 

**Date:** June 2024

**Script Version:** 1.0

**Built With:** Python (v`3.9.18`), ArcGIS Pro (v`3.2`*), ArcGIS Enterprise (v`10.3`)

**\*** See *Potential Errors* if using ArcGIS Pro version 3.2. Previous and later versions should run this script without issue.

# Purpose
This script aims to pull details about all items in an organization's ArcGIS Portal and create a list of dependencies for each item that can be used for geospatial data management. This script also includes a method for converting this data into a `networkX` connection graph, which is then converted to ArcGIS feature classes, used to visualize data in ArcGIS Pro or in an online ArcGIS Dashboard. An alternative method to this would involve using ArcGIS Knowledge.

# Input Parameters
## portal
**type:** string

**Description:** The URL of the ArcGIS Portal you will be logging into and retrieving data from. Format: `https://webpage.ext/portal`.

## GISuser
**type:** string

**Description:** Username used to login to the ArcGIS Portal. Note that this account will host any exported features and will be used for queries. Preferably use an admin account with the ability to view other accounts' private items as well as shared ones.

## GISpass
**type:** string

**Description:** Password of account used to login to the ArcGIS Portal.

## filterType
**type:** string

**Description:** Filtering method used for Portal item types. Use `Exclude` to remove any item types listed in `itemFilter`, `Include` to only keep item types in `itemFilter`, or `empty string` to apply no filter.

**Accepted Inputs:** `Exclude`,`Include`,`empty string`

## itemFilter
**type:** list

**Description:** List of item types to filter for.

Accepted Inputs: `empty list` or any combination of: `360 VR Experience`,`CityEngine Web Scene`,`Map Area`,`Pro Map`,`Web Map`,`Web Scene`,`Feature Collection`,`Feature Collection Template`,`Feature Service`,`Geodata Service`,`Group Layer`,`Image Service`,`KML`,`KML Collection`,`Map Service`,`OGCFeatureServer`,`Oriented Imagery Catalog`,`Relational Database Connection`,`3DTilesService`,`Scene Service`,`Vector Tile Service`,`WFS`,`WMS`,`WMTS`,`Geometry Service`,`Geocoding Service`,`Geoprocessing Service`,`Network Analysis Service`,`Workflow Manager Service`,`AppBuilder Extension`,`AppBuilder Widget Package`,`Code Attachment`,`Dashboard`,`Data Pipeline`,`Deep Learning Studio Project`,`Esri Classification Schema`,`Excalibur Imagery Project`,`Experience Builder Widget`,`Experience Builder Widget Package`,`Form`,`GeoBIM Application`,`GeoBIM Project`,`Hub Event`,`Hub Initiative`,`Hub Initiative Template`,`Hub Page`,`Hub Project`,`Hub Site Application`,`Insights Workbook`,`Insights Workbook Package`,`Insights Model`,`Insights Page`,`Insights Theme`,`Insights Data Engineering Workbook`,`Insights Data Engineering Model`,`Investigation`,`Knowledge Studio Project`,`Mission`,`Mobile Application`,`Notebook`,`Notebook Code Snippet Library`,`Native Application`,`Native Application Installer`,`Ortho Mapping Project`,`Ortho Mapping Template`,`Solution`,`StoryMap`,`Web AppBuilder Widget`,`Web Experience`,`Web Experience Template`,`Web Mapping Application`,`Workforce Project`,`Administrative Report`,`Apache Parquet`,`CAD Drawing`,`Color Set`,`Content Category Set`,`CSV`,`Document Link`,`Earth configuration`,`Esri Classifier Definition`,`Export Package`,`File Geodatabase`,`GeoJson`,`GeoPackage`,`GML`,`Image`,`iWork Keynote`,`iWork Numbers`,`iWork Pages`,`Microsoft Excel`,`Microsoft Powerpoint`,`Microsoft Word`,`PDF`,`Report Template`,`Service Definition`,`Shapefile`,`SQLite Geodatabase`,`Statistical Data Collection`,`StoryMap Theme`,`Style`,`Symbol Set`,`Visio Document`,`ArcPad Package`,`Compact Tile Package`,`Explorer Map`,`Globe Document`,`Layout`,`Map Document`,`Map Package`,`Map Template`,`Mobile Basemap Package`,`Mobile Map Package`,`Mobile Scene Package`,`Project Package`,`Project Template`,`Published Map`,`Scene Document`,`Task File`,`Tile Package`,`Vector Tile Package`,`Explorer Layer`,`Image Collection`,`Layer`,`Layer Package`,`Pro Report`,`Scene Package`,`3DTilesPackage`,`Desktop Style`,`ArcGIS Pro Configuration`,`Deep Learning Package`,`Geoprocessing Package`,`Geoprocessing Package (Pro version)`,`Geoprocessing Sample`,`Locator Package`,`Raster function template`,`Rule Package`,`Pro Report Template`,`ArcGIS Pro Add In`,`Code Sample`,`Desktop Add In`,`Desktop Application`,`Desktop Application Template`,`Explorer Add In`,`Survey123 Add In`,`Workflow Manager Package` OR other item types as per [Items and Item Types (ArcGIS Developers)](https://developers.arcgis.com/rest/users-groups-and-items/items-and-item-types/).

## generateNodes
**type:** boolean

**Description:** Determines if the network geometry is created for dependencies. If `True`, geometry is created using `networkx` which can be converted to feature classes. If `False`, no geometry is created.

Accepted Inputs: `True`, `False`

## exportType
**type:** string

**Description:** Type of item to export as. Data can be converted to CSV files, feature classes (`Features`), geodatabase tables (`Geo Table`), all types (`All`), or not exported (`empty string`). An exception will be raised if `generateNodes` is `False` and exportType is `Features` due to feature classes requiring geometry.

Accepted Inputs: `Features`, `CSV`, `Geo Table`, `All`, `empty string`

## pointName
**type:** string

**Description:**  Name of the outputted point feature class or CSV. If no geometry is created, this name is still used for CSVs. Ensure that this name does not conflict with other items in the user's Portal.

## lineName
**type:** string

**Description:** Name of the outputted line feature class or CSV. If no geometry is created, this name is still used for CSVs. Ensure that this name does not conflict with other items in the user's Portal.

## portalUpload
**type:** boolean

**Description:** If items are uploaded to Portal. 

Accepted Inputs: `True`, `False`

## outPath
**type:** string

**Description:** Directory where CSV files will be stored if `exportType` is `CSV` or `Both`. If not specified, CSV files will be put in the parent folder of the geodatabase.

## workspace
**type:** string

**Description:** Path to the geodatabase used when running this script. To store features in memory, set this to `Memory` or `memory`.If not specified, path is recieved from `arcpy.env.workspace`.

**Accepted Inputs:** `Memory`,`memory`, file paths

## portalItemTypes
**type:** list

**Description:** List of all item types possible in Portal. Only used if more than 500 items are returned in a query for a user.

Accepted Inputs: `empty list` or any combination of: `360 VR Experience`,`CityEngine Web Scene`,`Map Area`,`Pro Map`,`Web Map`,`Web Scene`,`Feature Collection`,`Feature Collection Template`,`Feature Service`,`Geodata Service`,`Group Layer`,`Image Service`,`KML`,`KML Collection`,`Map Service`,`OGCFeatureServer`,`Oriented Imagery Catalog`,`Relational Database Connection`,`3DTilesService`,`Scene Service`,`Vector Tile Service`,`WFS`,`WMS`,`WMTS`,`Geometry Service`,`Geocoding Service`,`Geoprocessing Service`,`Network Analysis Service`,`Workflow Manager Service`,`AppBuilder Extension`,`AppBuilder Widget Package`,`Code Attachment`,`Dashboard`,`Data Pipeline`,`Deep Learning Studio Project`,`Esri Classification Schema`,`Excalibur Imagery Project`,`Experience Builder Widget`,`Experience Builder Widget Package`,`Form`,`GeoBIM Application`,`GeoBIM Project`,`Hub Event`,`Hub Initiative`,`Hub Initiative Template`,`Hub Page`,`Hub Project`,`Hub Site Application`,`Insights Workbook`,`Insights Workbook Package`,`Insights Model`,`Insights Page`,`Insights Theme`,`Insights Data Engineering Workbook`,`Insights Data Engineering Model`,`Investigation`,`Knowledge Studio Project`,`Mission`,`Mobile Application`,`Notebook`,`Notebook Code Snippet Library`,`Native Application`,`Native Application Installer`,`Ortho Mapping Project`,`Ortho Mapping Template`,`Solution`,`StoryMap`,`Web AppBuilder Widget`,`Web Experience`,`Web Experience Template`,`Web Mapping Application`,`Workforce Project`,`Administrative Report`,`Apache Parquet`,`CAD Drawing`,`Color Set`,`Content Category Set`,`CSV`,`Document Link`,`Earth configuration`,`Esri Classifier Definition`,`Export Package`,`File Geodatabase`,`GeoJson`,`GeoPackage`,`GML`,`Image`,`iWork Keynote`,`iWork Numbers`,`iWork Pages`,`Microsoft Excel`,`Microsoft Powerpoint`,`Microsoft Word`,`PDF`,`Report Template`,`Service Definition`,`Shapefile`,`SQLite Geodatabase`,`Statistical Data Collection`,`StoryMap Theme`,`Style`,`Symbol Set`,`Visio Document`,`ArcPad Package`,`Compact Tile Package`,`Explorer Map`,`Globe Document`,`Layout`,`Map Document`,`Map Package`,`Map Template`,`Mobile Basemap Package`,`Mobile Map Package`,`Mobile Scene Package`,`Project Package`,`Project Template`,`Published Map`,`Scene Document`,`Task File`,`Tile Package`,`Vector Tile Package`,`Explorer Layer`,`Image Collection`,`Layer`,`Layer Package`,`Pro Report`,`Scene Package`,`3DTilesPackage`,`Desktop Style`,`ArcGIS Pro Configuration`,`Deep Learning Package`,`Geoprocessing Package`,`Geoprocessing Package (Pro version)`,`Geoprocessing Sample`,`Locator Package`,`Raster function template`,`Rule Package`,`Pro Report Template`,`ArcGIS Pro Add In`,`Code Sample`,`Desktop Add In`,`Desktop Application`,`Desktop Application Template`,`Explorer Add In`,`Survey123 Add In`,`Workflow Manager Package` OR other item types as per [Items and Item Types (ArcGIS Developers)](https://developers.arcgis.com/rest/users-groups-and-items/items-and-item-types/).

# Resources and Added Info
## Runtime
The speed that this script is able to run depends mainly on how fast `testLink` can run with how slow checking webpages is. This is dependent on (1) the number of total items queried from the portal and more importantly (2) the amount of overlap in their dependencies. 


## Links
- [List of Portal Item Types](https://developers.arcgis.com/rest/users-groups-and-items/items-and-item-types/)
- [NetworkX drawing functions](https://networkx.org/documentation/stable/reference/drawing.html) (if spring method is insufficient)

## ESRI Functions
`dependent_to`
- Currently does not work: throws no error but does not progress.
- Code for `dependent_to` is included here as if it works, but is commented out.
- The following line was added to keep the same fields present in the final dataset regardless of if `dependent_to` is functional:
`itemInfo['totalDepends'] = '0'`.
- If `dependent_to` is functional, remove the above line and uncomment the three other lines related to the function.


`gis.content.search`
- This function has very weird behavior that is not well [documented](https://developers.arcgis.com/python/guide/accessing-and-creating-content/#about-search). 
- Only a maximum of 500 items can be returned regardless of what value is used in the  `max_items` arguement (default: `10`).
- Unless otherwise specified, `gis.content.search` will return code attachments, making the number of items found with this method different from that of a Portal's content page.
- Queries such as `type: Web Map` will return other item types that include 'Web Map' unless written as `type: "Web Map"`.
    - `OR` operator only seems to work with quotations.
- When querying, there is a specific order different parts of the query must be in. 
  - `owner:` cannot be used as the first part if multiple parts are being used. 
  - When using `title:`, `type:`, and `owner:` together in a query, they must be in this order or the query will not return anything.

`gis.content.advanced_search` 
- **Do not use this. It will lie to you.**
- The limit for `max_items` is 10,000. 
- Most blank query methods do not work and return 0 items.

`gis.users.search`
- Using a blank string or wildcard as a query here will cause an error unlike `gis.content.search`.
- There is no apparent maximum number of items that this function can return unlike `gis.content.search`.
- This function never returns items owned by accounts in a Portal created by ESRI unlike `gis.content.search`.

## Potential Errors
### AttributeError: module 'scipy.sparse' has no attribute 'coo_array'

This error can sometimes appear if your ArcGIS Python environment is not up to date. The error is caused by version conficts between the `networkx` and `scipy` packages. To trouble shoot: try using `!pip upgrade-- networkx scipy` to update the packages, update ArcGIS Pro, and update the ArcGIS Pro Python environment.

If you are using ArcGIS Pro version 3.2 and cannot update to a new version, try replacing your `networkx` package files with those of version 2.6. ArcGIS will not allow you to change package versions for `networkx` and blocks installation through conda (anaconda), so follow these steps:

1. Create a clone environment in ArcGIS Pro's package manager and note its file path.
2. Install a secondary ('ArcGIS-free') Python environment on your machine or use another machine without ArcGIS Pro.
3.  Navigate to command prompt and install/upgrade `networkx` version 2.6 with the following command:
    >py -m pip install --upgrade networkx==2.6
    - Note: you will need to navigate to the correct (non-ArcGIS) Python environment if doing this on the same machine.
4. Navigate to the Python installation with `networkx` 2.6:
    > C:\Users\YOURUSER\AppData\Local\Programs\Python\PythonXXX
5. Copy all folders relating to `networkx` to a secondary location or to your clipboard to paste later. These will be:
    ```
    ~\PythonXXX\Lib\site-packages\networkx
    ~\PythonXXX\Lib\site-packages\networkx-2.6.dist-info
    ~\PythonXXX\share\doc\networkx-2.6
    ```
6. Navigate to the cloned environment you created earlier using the copied path.
7. Copy the `networkx` folders from before to the same relative locations, deleting any other `networkx` folders found in the same directory.
8. Run the script in ArcGIS Pro. Pro will not recognize the version change in Package Manager, but this error should be resolved.