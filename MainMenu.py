# install tkinter


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk

xls = pd.ExcelFile('Python Data .xlsx')
datasets = {sheet: xls.parse(sheet) for sheet in xls.sheet_names if "FEMA" not in sheet}
housing_data = pd.read_csv('consolidated housing data.csv')

# get summary statistics for the housing data
summary_statistics = housing_data[["Price", "Area", "Beds", "Bathrooms", "Zipcode"]].describe()

print(summary_statistics)


def haversine(lat1, lon1, lat2, lon2):
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    r = 6371  # Radius of Earth in kilometers
    return c * r * 1000  # Convert to meters

def attraction_visualization(datasets, price_range, beds, baths):
    # Define the function to calculate distance between two coordinates (latitude, longitude)


    # Filter the zillow_scrap_cleaned dataset
    houses = datasets['zillow_scrap_cleaned'][
        (datasets['zillow_scrap_cleaned']['Price'].between(*price_range)) &
        (datasets['zillow_scrap_cleaned']['Beds'] == beds) &
        (datasets['zillow_scrap_cleaned']['Bathrooms'] == baths)
    ][['Latitude', 'Longitude']]

    attractions = datasets['City_Historical_Attractions_Cle'][['Latitude', 'Longitude']]
    
    if houses.empty or attractions.empty:
        messagebox.showinfo("No Data", "No attractions found for the specified criteria.")
        return
    
    dist_matrix_attractions = np.array([[haversine(lat1, lon1, lat2, lon2) for lat2, lon2 in zip(attractions['Latitude'], attractions['Longitude'])] for lat1, lon1 in zip(houses['Latitude'], houses['Longitude'])])
    attraction_counts = np.sum(dist_matrix_attractions <= 500, axis=1)
    
    if len(attraction_counts) > 0:
        house_counts_attractions = np.bincount(attraction_counts)
        x_values_attractions = np.arange(len(house_counts_attractions))
    
        # Plot the bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(x_values_attractions, house_counts_attractions, color='m', alpha=0.7)
        plt.xlabel('Number of Attractions Within 500m')
        plt.ylabel('Number of Houses')
        plt.title('Number of Houses vs Number of Nearby Attractions')
        plt.show()
    else:
        messagebox.showinfo("No Data", "No attractions found for the specified criteria.")


def crime_visualization(datasets, price_range, beds, baths):
    # Filter the zillow_scrap_cleaned dataset
    houses = datasets['zillow_scrap_cleaned'][
        (datasets['zillow_scrap_cleaned']['Price'].between(*price_range)) &
        (datasets['zillow_scrap_cleaned']['Beds'] == beds) &
        (datasets['zillow_scrap_cleaned']['Bathrooms'] == baths)
    ][['Latitude', 'Longitude']]
    
    incidents = datasets['Cleaned - Dallas Offense Incide'][['geocoded_column/latitude', 'geocoded_column/longitude']]
    
    if houses.empty or incidents.empty:
        messagebox.showinfo("No Data", "No properties found for the specified criteria.")
        return
    
    dist_matrix = np.array([[haversine(lat1, lon1, lat2, lon2) for lat2, lon2 in zip(incidents['geocoded_column/latitude'], incidents['geocoded_column/longitude'])] for lat1, lon1 in zip(houses['Latitude'], houses['Longitude'])])
    incident_counts = np.sum(dist_matrix <= 500, axis=1)
    if len(incident_counts) > 0:
        house_counts = np.bincount(incident_counts)
        x_values = np.arange(len(house_counts))
    
        # Plot the bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(x_values, house_counts, color='c', alpha=0.7)
        plt.xlabel('Number of Offense Incidents Within 500m')
        plt.ylabel('Number of Houses')
        plt.title('Number of Houses vs Number of Nearby Offense Incidents')
        plt.show()
    else:
        messagebox.showinfo("No Data", "No properties found for the specified criteria.")


def map_visualization(datasets, price_range, beds, baths):
    # Filter the zillow_scrap_cleaned dataset
    datasets['zillow_scrap_cleaned'] = datasets['zillow_scrap_cleaned'][
        (datasets['zillow_scrap_cleaned']['Price'].between(*price_range)) &
        (datasets['zillow_scrap_cleaned']['Beds'] == beds) &
        (datasets['zillow_scrap_cleaned']['Bathrooms'] == baths)
    ]
    
    # Define the latitude and longitude bounds
    lat_bounds = (32.2, 33.1)
    long_bounds = (-97.2, -96.2)
    
    # Define colors for each dataset
    colors = {
        'zillow_scrap_cleaned': 'black',
        'City_Historical_Attractions_Cle': 'blue',
        'Cleaned - Dallas Offense Incide': 'red'
    }
    
    # Correct the latitude and longitude column names
    lat_long_columns_corrected = {
        'zillow_scrap_cleaned': ('Latitude', 'Longitude'),
        'City_Historical_Attractions_Cle': ('Latitude', 'Longitude'),
        'Cleaned - Dallas Offense Incide': ('geocoded_column/latitude', 'geocoded_column/longitude')
    }
    
    # Define label names for each dataset
    labels = {
        'zillow_scrap_cleaned': 'Houses',
        'City_Historical_Attractions_Cle': 'Historical Attractions',
        'Cleaned - Dallas Offense Incide': 'Offense Incidents'
    }

    # Create a new plot
    plt.figure(figsize=(10, 10))

    # Iterate over datasets and plot the filtered locations
    for sheet, (lat_col, long_col) in lat_long_columns_corrected.items():
        # Filter data based on latitude and longitude bounds
        filtered_data = datasets[sheet][
            (datasets[sheet][lat_col].between(*lat_bounds)) &
            (datasets[sheet][long_col].between(*long_bounds))
            ]
        # Check if the dataset is zillow_scrap_cleaned and adjust the marker style and size
        if sheet == 'zillow_scrap_cleaned':
            plt.scatter(filtered_data[long_col], filtered_data[lat_col], color=colors[sheet], label=labels[sheet],
                        alpha=0.8, s=100, edgecolor='k', marker='D')
        else:
            plt.scatter(filtered_data[long_col], filtered_data[lat_col], color=colors[sheet], label=labels[sheet],
                        alpha=0.5)

    # Set plot labels and legend
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Locations Visualization on Map')
    plt.legend()
    
    # Show the plot
    plt.show()



"""attraction_visualization(datasets, price_range=(300000, 1000000), beds=2, baths=2)
crime_visualization(datasets, price_range=(300000, 1000000), beds=2, baths=2)
map_visualization(datasets, price_range=(300000, 1000000), beds=2, baths=2)"""

# to get a relationship between number of incidents near the house and the effect on housing price
incident_counts = housing_data.groupby('zpid').size().reset_index(name='incident_count')
merged_data = pd.merge(housing_data, incident_counts, on='zpid', how='left')
# make nan for any nonnumerical value
merged_data['Calculated Price Per Sqft'] = pd.to_numeric(merged_data['Calculated Price Per Sqft'], errors='coerce')

def generate_plot():

    plot_type = plot_dropdown.get()

    # you dont have to input anything for this function
    if plot_type == "Scatter Plot of Zillow Housing List":
        plt.figure(figsize=(12, 7))
        plt.scatter(merged_data['Calculated Price Per Sqft'], merged_data['incident_count'], alpha=0.6, edgecolors='w', linewidth=0.5)
        plt.title('Relationship between Price per Sqft and Number of Incidents')
        plt.xlabel('Price per Sqft')
        plt.ylabel('Number of Incidents')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.show()

    else:

        min_price = min_price_entry.get()
        max_price = max_price_entry.get()
        beds_value = beds_entry.get()
        baths_value = baths_entry.get()
        
        # Check if any value is empty or invalid and show an error message
        if not min_price or not max_price or not beds_value or not baths_value:
            messagebox.showerror("Error", "Please enter all required values.")
            return
        
        # Convert the string values to appropriate data types
        try:
            min_price = float(min_price)
            max_price = float(max_price)
            beds = int(beds_value)
            baths = int(baths_value)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid values.")
            return
        
        price_range = (min_price, max_price)

        # Based on user choice, call the corresponding visualization function
        if plot_type == "Attractions":
            # catch any error regarding a invalid price range or beds or baths, since some of the ranges may not exist in our dataset, same as below
            try:
                attraction_visualization(datasets, price_range, beds, baths)
            except Exception as e:
                print(f"An error occurred: {e}")
                # show an error message to the user
                messagebox.showerror("Error", f"An error occurred: {e}")

        elif plot_type == "Crime":
            try:
                crime_visualization(datasets, price_range, beds, baths)
            except Exception as e:
                print(f"An error occurred: {e}")
                # show an error message to the user
                messagebox.showerror("Error", f"An error occurred: {e}")

        elif plot_type == "Map":
            try:
                map_visualization(datasets, price_range, beds, baths)
            except Exception as e:
                print(f"An error occurred: {e}")
                # show an error message to the user
                messagebox.showerror("Error", f"An error occurred: {e}")


# Initialize main window
root = tk.Tk()
root.title("Ziphouse - Housing Data Visualization")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load the background image and resize it to fit the screen
background_image = Image.open("stockImage.jpeg")  # Replace "background.jpg" with your image file path
background_image = background_image.resize((screen_width, screen_height), Image.ANTIALIAS)
background_photo = ImageTk.PhotoImage(background_image)

# Create a label with the background image and place it at the top-left corner
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Prevent the image from being garbage collected (reference)
root.background_photo = background_photo

# Add "Ziphouse" label at the top
ziphouse_label = tk.Label(root, text="Ziphouse", font=("Helvetica", 60), bg="white")  # Customize font and background color
ziphouse_label.pack(pady=30)

plot_options = ["Attractions", "Crime", "Map", "Scatter Plot of Zillow Housing List"]

# Define a custom font for the options in the OptionMenu
custom_font = ("Helvetica", 25)  # You can adjust the font size (14 in this example)

# Create the OptionMenu with the custom font
plot_dropdown = tk.StringVar(root)
plot_dropdown.set(plot_options[0])  # set the default value
option_menu = tk.OptionMenu(root, plot_dropdown, *plot_options)
option_menu.config(font=custom_font)  # Set the custom font for the OptionMenu
option_menu.pack(pady=60)  # Pack the OptionMenu with the custom font


tk.Label(root, text="Min Price:", font=("Helvetica", 30)).pack(pady=20)  # Increase font size
min_price_entry = tk.Entry(root, width=30, font=("Helvetica", 30))  # Set font size
min_price_entry.pack()

tk.Label(root, text="Max Price:", font=("Helvetica", 30)).pack(pady=20)  # Increase font size
max_price_entry = tk.Entry(root, width=30, font=("Helvetica", 30))  # Set font size
max_price_entry.pack()

tk.Label(root, text="Number of Beds:", font=("Helvetica", 30)).pack(pady=20)  # Increase font size
beds_entry = tk.Entry(root, width=30, font=("Helvetica", 30))  # Set font size
beds_entry.pack()

tk.Label(root, text="Number of Baths:", font=("Helvetica", 30)).pack(pady=20)  # Increase font size
baths_entry = tk.Entry(root, width=30, font=("Helvetica", 30))  # Set font size
baths_entry.pack()

# Add button to generate plot with larger font size
tk.Button(root, text="Generate Plot", command=generate_plot, font=("Helvetica", 30)).pack(pady=30)  # Increase font size


# Run the GUI loop
root.mainloop()
