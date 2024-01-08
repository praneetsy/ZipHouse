import csv
from math import radians, sin, cos, sqrt, atan2

class RealEstateListing:
    def __init__(self, address, price, bedrooms, bathrooms, area, latitude, longitude):
        self.address = address
        self.price = price
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.area = area
        self.latitude = latitude
        self.longitude = longitude

    def calculate_distance(self, target_latitude, target_longitude):
        R = 6371  # Radius of the Earth in kilometers
        lat1, lon1 = radians(self.latitude), radians(self.longitude)
        lat2, lon2 = radians(target_latitude), radians(target_longitude)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance_km = R * c
        distance_miles = distance_km * 0.621371  # Conversion factor from kilometers to miles
        return distance_miles

class RealEstateAgency:
    def __init__(self):
        self.listings = []

    def add_listing(self, listing):
        self.listings.append(listing)

    def display_listings(self):
        if not self.listings:
            print("No listings available.")
        else:
            print("Real Estate Listings:")
            for idx, listing in enumerate(self.listings, start=1):
                print(f"{idx}. Address: {listing.address}, Price: ${listing.price}, Bedrooms: {listing.bedrooms}, Bathrooms: {listing.bathrooms}, Area: {listing.area} sqft")

    def filter_by_price_and_distance(self, price_option, distance_option):
        if price_option == 1:
            max_price = 100000
        elif price_option == 2:
            max_price = 500000
        else:
            max_price = float('inf')  # No price limit

        if distance_option == 1:
            max_distance = 20  # within 20 miles
        elif distance_option == 2:
            max_distance = 50  # within 50 miles
        else:
            max_distance = 100  # within 100 miles

        filtered_listings = [listing for listing in self.listings if listing.price <= max_price and listing.calculate_distance(listing.latitude, listing.longitude) <= max_distance]
        return filtered_listings

def read_csv_data(filename):
    listings = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            address = row['Address_consolidated']
            price = float(row['Price'])
            bedrooms = int(row['Beds'])
            bathrooms = int(row['Bathrooms'])
            area = int(row['Area'])
            latitude, longitude = float(row['Latitude_consolidated']), float(row['Longitude_consolidated'])
            listing = RealEstateListing(address, price, bedrooms, bathrooms, area, latitude, longitude)
            listings.append(listing)
    return listings

def read_attractions_data(filename):
    attractions = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            latitude, longitude = float(row['Latitude']), float(row['Longitude'])
            attraction_name = row['Title']
            address = row['Address']
            attractions.append({'latitude': latitude, 'longitude': longitude, 'name': attraction_name, 'address': address})
    return attractions

def get_nearby_attractions(latitude, longitude, attractions):
    nearby_attractions = []
    for attraction in attractions:
        attraction_latitude, attraction_longitude = attraction['latitude'], attraction['longitude']
        distance = calculate_distance(latitude, longitude, attraction_latitude, attraction_longitude)
        if distance <= 1:  # Search within 1 mile
            name = attraction['name']
            address = attraction['address']
            nearby_attractions.append(f"{name} - {address} (Distance: {distance:.2f} miles)")
    return nearby_attractions

def calculate_distance(lat1, lon1, lat2, lon2):
    # Function to calculate distance in miles between two sets of latitude and longitude coordinates
    R = 6371  # Radius of the Earth in kilometers
    lat1, lon1 = radians(lat1), radians(lon1)
    lat2, lon2 = radians(lat2), radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance_km = R * c
    distance_miles = distance_km * 0.621371  # Conversion factor from kilometers to miles
    return distance_miles

def display_listings_by_criteria(agency, price_option, distance_option):
    filtered_listings = agency.filter_by_price_and_distance(price_option, distance_option)
    if filtered_listings:
        print("\nListings within the specified criteria:")
        for idx, listing in enumerate(filtered_listings, start=1):
            print(f"{idx}. Address: {listing.address}, Price: ${listing.price}")
    else:
        print("No listings found within the specified criteria.")

def main():
    filename_listings = 'housingData.csv'
    filename_attractions = 'historical_attractions.csv'

    listings_data = read_csv_data(filename_listings)
    attractions_data = read_attractions_data(filename_attractions)

    agency = RealEstateAgency()
    for listing_data in listings_data:
        agency.add_listing(listing_data)

    while True:
        print("\nMenu:")
        print("1. View Listings")
        print("2. Filter Listings by Price and Offense Miles")
        print("3. Explore Nearby Historical Attractions")
        print("4. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            agency.display_listings()
        elif choice == "2":
            print("\nPrice Options:")
            print("1. Less than $100000")
            print("2. $10000 to $500000")
            print("3. Above $500000")
            price_option = int(input("Enter your price option: "))

            print("\nOffense Miles Options:")
            print("1. Within 20 miles")
            print("2. Within 50 miles")
            print("3. Within 100 miles")
            distance_option = int(input("Enter your distance option: "))

            display_listings_by_criteria(agency, price_option, distance_option)
        elif choice == "3":
            listing_number = int(input("Enter the number of the listing you want to explore: ")) - 1
            if 0 <= listing_number < len(agency.listings):
                listing = agency.listings[listing_number]
                attractions = get_nearby_attractions(listing.latitude, listing.longitude, attractions_data)
                print(f"\nHistorical Attractions near {listing.address}:")
                if attractions:
                    for attraction in attractions:
                        print(attraction)
                else:
                    print("No attractions found within 5 miles.")
            else:
                print("Invalid listing number. Please try again.")
        elif choice == "4":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
