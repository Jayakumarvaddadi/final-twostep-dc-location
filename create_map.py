import pandas as pd
import folium
import random

# Load files
stores = pd.read_excel('saavu2.xlsx')
stores.columns = stores.columns.str.lower()

dcs = pd.read_excel('final_dcs.xlsx')
dcs.columns = dcs.columns.str.lower()

mapping = pd.read_excel('store_dc_mapping.xlsx')

# Create map
map_india = folium.Map(location=[22.5, 78.9], zoom_start=5)

# Color list
colors = ['red', 'blue', 'green', 'purple', 'orange',
          'darkred', 'cadetblue', 'darkgreen']

# Plot stores
for idx, row in mapping.iterrows():

    store_idx = int(row['store_index'])
    dc_idx = int(row['dc_index'])

    store = stores.iloc[store_idx]

    color = colors[dc_idx % len(colors)]

    folium.CircleMarker(
        location=[store['lat'], store['long']],
        radius=4,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(map_india)

# Plot DCs
for idx, row in dcs.iterrows():

    color = colors[idx % len(colors)]

    folium.Marker(
        location=[row['lat'], row['long']],
        popup=f'DC {idx}',
        icon=folium.Icon(color=color, icon='star')
    ).add_to(map_india)

# Save map
map_india.save("index.html")

print("Colored cluster map created")