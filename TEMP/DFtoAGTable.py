#------------------ WORKING EXAMPLE -----------------------------
import pandas as pd
from arcgis.features import GeoAccessor, GeoSeriesAccessor, FeatureSet
from arcgis.gis import GIS

# Create a sample DataFrame
data = {
    'name': ['Location1', 'Location2', 'Location3'],
    'latitude': [34.0522, 36.1699, 40.7128],
    'longitude': [-118.2437, -115.1398, -74.0060]
}
df = pd.DataFrame(data)

# Ensure latitude and longitude are of type float
df['latitude'] = df['latitude'].astype(float)
df['longitude'] = df['longitude'].astype(float)

# Create a Spatially Enabled DataFrame
sdf = pd.DataFrame.spatial.from_xy(df, x_column='longitude', y_column='latitude')

# Convert the spatial DataFrame to a feature set (in-memory)
feature_set = sdf.spatial.to_featureset()

# Print the feature set to verify
print(feature_set)

# Convert the feature set back to a pandas DataFrame if needed
features = feature_set.features
features_list = [f.attributes for f in features]
in_memory_table = pd.DataFrame(features_list)

# Print the in-memory table
print(in_memory_table)
