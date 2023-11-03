from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


def convert(db, column):
    if column == 'Latitude':
        for x in range(len(db[column].index)):
            if db.at[x, column][-1] == 'N':
                db.at[x, column] = '+' + db.at[x, column][0:len(db.at[x, column]) - 1]
            elif db.at[x, column][-1] == 'S':
                db.at[x, column] = '-' + db.at[x, column][0:len(db.at[x, column]) - 1]

    elif column == 'Longitude':
        for x in range(len(db[column].index)):
            if db.at[x, column][-1] == 'E':
                db.at[x, column] = '+' + db.at[x, column][0:len(db.at[x, column]) - 1]
            elif db.at[x, column][-1] == 'W':
                db.at[x, column] = '-' + db.at[x, column][0:len(db.at[x, column]) - 1]

    return db


def create_map(ds, dw):
    # create a world map
    axis = dw.plot(color='grey', edgecolor='black')
    ds.plot(column='AverageTemperature', ax=axis, markersize=80, legend=True, legend_kwds={'shrink': 0.3})
    plt.title('Average Temperatures in World Major Cities ', fontsize=15)
    fig = plt.gcf()
    fig.set_size_inches(20, 16)
    fig.savefig('matplotlib.png', dpi=500, bbox_inches='tight')
    return plt.show()


def create_map_date(ds, dw, date):
    filtered_ds = ds[ds['dt'] == date]
    if not filtered_ds.empty:
        create_map(filtered_ds, dw)
    else:
        print('Data not available for the given date.')


def create_map_gif(ds, dw, dates):

    fig, ax = plt.subplots(figsize=(20, 16))
    axis = dw.plot(ax=ax, color='grey', edgecolor='black')

    def update(frame):
        current_date = dates[frame]
        filtered_cities = ds[ds['dt'] == current_date]
        scatter = filtered_cities.plot(column='AverageTemperature', ax=axis, markersize=80)
        plt.title(f'Average Temperatures in World Major Cities ({current_date})', fontsize=25)
        return scatter

    def init():
        # Create an empty colorbar with the appropriate colormap and normalization
        sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=-40, vmax=40))
        sm.set_array([])  # empty array for the data range
        # Add the colorbar to the figure
        cbar = plt.colorbar(sm, ax=ax, fraction=0.02, pad=0.04)
        cbar.ax.tick_params(labelsize=14)
        return cbar

    animation = FuncAnimation(fig, update, frames=len(dates), interval=250, init_func=init)
    animation.save('temperature_animation.gif', fps=1)


def date_map_gif(ds, dw, min_date, max_date):
    fig, ax = plt.subplots(figsize=(20, 16))
    axis = dw.plot(ax=ax, color='grey', edgecolor='black')
    panda_dates = ds[(ds['dt'] >= min_date) & (ds['dt'] <= max_date)]
    dates = panda_dates['dt'].tolist()

    def update(frame):
        current_date = dates[frame]
        filtered_cities = ds[ds['dt'] == current_date]
        scatter = filtered_cities.plot(column='AverageTemperature', ax=axis, markersize=80)
        plt.title(f'Average Temperatures in World Major Cities ({current_date})', fontsize=25)
        return scatter

    def init():
        # Create an empty colorbar with the appropriate colormap and normalization
        sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=-80, vmax=60))
        sm.set_array([])  # empty array for the data range
        # Add the colorbar to the figure
        cbar = plt.colorbar(sm, ax=ax, fraction=0.02, pad=0.04)
        cbar.ax.tick_params(labelsize=14)
        return cbar

    animation = FuncAnimation(fig, update, frames=len(dates), interval=250, init_func=init)
    animation.save('temperature_animation.gif', fps=1)


def create_map_range(ds, dw, start_date, end_date):
    # Filter data within the specified date range
    filtered_data = ds[(ds['dt'] >= start_date) & (ds['dt'] <= end_date)]

    # Calculate temperature range for each city within the specified date range
    city_temperature_ranges = filtered_data.groupby('City')['AverageTemperature'].agg(['min', 'max']).apply(
        lambda x: (x['min'], x['max']), axis=1)

    # Get top 5 cities with the highest temperature difference within the specified date range
    top_cities = city_temperature_ranges.apply(lambda x: x[1] - x[0]).nlargest(5).index

    # Filter data for top 5 cities within the specified date range
    top_cities_data = filtered_data[filtered_data['City'].isin(top_cities)]

    # Create a world map
    axis = dw.plot(color='grey', edgecolor='black')

    # Plot top 5 cities with the highest temperature range within the specified date range
    top_cities_data.plot(column='AverageTemperature', ax=axis, markersize=80)

    # Annotate the map with city names and temperature ranges
    i = -80
    for idx, (city, (min_temp, max_temp)) in enumerate(city_temperature_ranges[top_cities].items()):
        plt.text(0, i, f'{city}: {round(min_temp, 1)}°C to {round(max_temp, 1)}°C: {round(max_temp - min_temp, 1)}C°',
                 fontsize=24, horizontalalignment='center')
        i = i - 9
    plt.title('Top 5 Cities with Highest Temperature Range\n{} to {}'.format(start_date, end_date), fontsize=15)
    fig = plt.gcf()
    fig.set_size_inches(20, 16)
    fig.savefig('matplotlib.png', dpi=500, bbox_inches='tight')

    plt.show()
