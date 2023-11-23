
import streamlit as st
import json
import folium

class RunStreamlit:
        
    def load_data(self, json_path):
        """
        Load data from a JSON file.

        Parameters:
        - json_path (str): The path to the JSON file.

        Returns:
        - dict: The loaded data from the JSON file.
        """
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)
        return data

    
    def main(self):
        """
        Main function is for the Streamlit application.

        Displays a title, loads city information from a JSON file, creates a Folium map,
        adds markers for each city, and displays the map in the Streamlit app.

        Parameters:
        - None

        Returns:
        - the map in the Streamlit app.
        """
        st.title("Visited Cities on the way to the east")

        # Load data from the JSON file
        city_info = self.load_data('result_dict.json')

        if city_info is not None:
            st.write("### Coordinates for All Cities")

            # Create a folium map centered on the first city
            city_map = folium.Map(location=[list(city_info.values())[0][0], list(city_info.values())[0][1]], zoom_start=10)

            # Loop through all cities and add markers to the map, city name as a popup
            for city, info in city_info.items():
                folium.Marker(
                    location=[info[0], info[1]],
                    popup=city,
                    icon=folium.Icon(color='blue', icon='info-sign')
                ).add_to(city_map)

            # Use iframe to display the Folium map as an HTML component in the Streamlit app 
            st.components.v1.html(city_map._repr_html_(), height=600)

#ensure that the main method is called only if the script is executed as the main program 
#create an instance of the RunStreamlit class and call its main method
if __name__ == "__main__":
    run_streamlit_instance = RunStreamlit()
    run_streamlit_instance.main()
