
import streamlit as st
import json
import folium

class RunStreamlit:
        
    def load_data(self, json_path):
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)
        return data

    def main(self):
        st.title("Visited Cities on the way to the east")

        # Load data from the JSON file
        city_info = self.load_data('result_dict.json')

        if city_info is not None:
            st.write("### Coordinates for All Cities")

            # Create a folium map centered on the first city
            city_map = folium.Map(location=[list(city_info.values())[0][0], list(city_info.values())[0][1]], zoom_start=10)

            # Loop through all cities and add markers to the map
            for city, info in city_info.items():
                folium.Marker(
                    location=[info[0], info[1]],
                    popup=city,
                    icon=folium.Icon(color='blue', icon='info-sign')
                ).add_to(city_map)

            # Use iframe to display the Folium map
            st.components.v1.html(city_map._repr_html_(), height=600)

if __name__ == "__main__":
    run_streamlit_instance = RunStreamlit()
    run_streamlit_instance.main()
