import streamlit as st
from travel_project.data import TravelData
from travel_project.methods import TravelGraphBidirectional, TravelGraphRight, TravelGraphLeft
from travel_project.plotting import Plotting


# Function to create a bidirectional graph
def create_bidirectional_graph(df):
    return TravelGraphBidirectional(df)


# Function to create an only right graph
def create_right_graph(df):
    return TravelGraphRight(df)


# Function to create an only left graph
def create_left_graph(df):
    return TravelGraphLeft(df)


# Path to the dataset
path = r"C:\Users\cibei\Downloads\worldcities.xlsx"

# Sidebar
page_options = ["Bidirectional Graph", "Right Graph", "Left Graph", "Dataset Info"]
page_selection = st.sidebar.selectbox("Select a page", page_options)

# Title of the web app
st.title("Travel Data Web App")

# Create an instance of the TravelData class to load and preprocess the dataset
travel_data = TravelData(path=path,
                         admin=True,
                         primary=True,
                         minor=False,
                         num=300
                         )
df_city = travel_data.df

# Create an instance of the Plotting class for visualizations
plotting = Plotting(df_city)

# Determine which graph type to use based on the selected page
if page_selection == "Bidirectional Graph":
    travel_graph = create_bidirectional_graph(df_city)
elif page_selection == "Right Graph":
    travel_graph = create_right_graph(df_city)
elif page_selection == "Left Graph":
    travel_graph = create_left_graph(df_city)
else:
    travel_graph = None

# Main content based on the selected page
if travel_graph is not None:
    st.header("Select the starting and target cities")

    # Select the starting and target cities
    city_names = df_city['city_ascii'].tolist()
    starting_city = st.selectbox("Select the starting city", city_names)
    target_city = st.selectbox("Select the target city", city_names)
    speed = st.slider("Select the speed (km/h)", 0, 1000, 100)

    # Calculate the shortest path and travel time
    result_short_path = travel_graph.shortest_path(source_city_name=starting_city,
                                                   target_city_name=target_city
                                                   )
    result_time = travel_graph.travel_time(path=result_short_path,
                                           speed=speed
                                           )
    st.subheader("Shortest Path Result")

    # Display the shortest path and travel time
    if result_short_path:
        st.write(f"The shortest path between {starting_city} and {target_city} is: ")
        st.write(result_short_path)
        st.write(result_time)
        st.subheader("3D Globe Plot of the Path")

        # Create a 3D globe plot of the path
        mapping = plotting.map_3d(cities_path=result_short_path)
        st.plotly_chart(mapping)
    else:
        st.sidebar.warning("Please select valid starting and target cities.")
else:
    st.header("Some info about the dataset")

    # Slider to select the number of countries to plot
    num_countries = st.slider("Select the number of countries to plot", 0, 20, 10)

    # Visualizations related to the dataset
    plot1 = plotting.plot_top_countries(n=num_countries)
    st.plotly_chart(plot1)

    plot2 = plotting.plot_population_by_continent()
    st.plotly_chart(plot2)

    plot3 = plotting.plot_population_by_country()
    st.plotly_chart(plot3)

    plot4 = plotting.plot_density_map()
    st.plotly_chart(plot4)
