# PROJECT - WEATHER DATA
___
*Luca Sangiovanni <luca.sangiovanni.2001@gmail.com>*
___

This project aims to show the change of temperatures from various cities around the world, through charts and maps that intuitively allow the user to understand these informations, also by interacting with a web app.

---

### PACKAGES USED

The libraries I used in the project, as stated in the ._toml_ file, are the following:
- **Numpy**: used to handle some data; in particular, I used a lot the random generation functions provided by this library.
- **Pandas**: strongly used to handle datasets.
- **Matplotlib**: used to create charts.
- **Seaborn**: used to create charts.
- **Geopandas**: used to handle geospatial data of the cities.
- **Plotly-express**: used to create maps.
- **Streamlit**: used to create the interface of the web app.
- **Requests**: used to get the link for the images used in the streamlit app.

Other used functions include _CountryInfo_ (from the countryinfo package), _Image_ (from the PIL package), _geodesic_ (from the geopy.distance package), _option_menu_ (from the streamlit_option_menu package) and _OpenCageGeocode_ (from opencage.geocoder).
Unfortunately, some packages are not present in the _.toml_ file; however, this file contains all the packages that have been used.

---

### PROJECT FILES

The file that contain pieces of code are the following:
- `visualization.py`: this python file contains all the classes and functions related to the creation of charts and maps.
- `utils.py`:  this file contains the imported data and a function I used to convert the coordinates of the cities (doesn't have to be run, it's just to show how I did it).
- `notebook.ipynb`: this notebook file contains the project itself, with blocks containing the call to other functions, used to show the data, the charts and the maps. You can run the code block by block, and see the outputs; if you are not able to run the web app, this is the way to see the project.
- `web_app.py`: this python file contains the code which allows to see the interface created with the package streamlit. It must be opened from the terminal, using the _streamlit run _ function; once opened, the user will be able to see a web page with different pages insde, where it is possible to interact by pushing buttons and selecting things, in order to show what the user want.

---

### HOW TO RUN THE CODE

As mentioned above, there are two possible ways of running the code:
1. _(Preferred way)_: Run the streamlit web app. To do so, all you have to do is go to the terminal and write this:
   > streamlit run web_app.py
   
2.  _(Alternative way)_: Use the jupyter notebook file and run cell by cell the code.

