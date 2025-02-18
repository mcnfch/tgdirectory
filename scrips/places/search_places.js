const fs = require('fs');
require('dotenv').config();

// Import the Places API v1 client library
const {PlacesClient} = require('@googlemaps/places').v1;

// Create a client
const client = new PlacesClient();

async function searchPlace(name, address, lat, lng) {
    try {
        // Construct the request
        const request = {
            textQuery: `${name} ${address}`,
            locationBias: {
                circle: {
                    center: {
                        latitude: lat,
                        longitude: lng
                    },
                    radius: 5000.0  // 5km radius
                }
            },
            includedType: 'restaurant',
            maxResultCount: 1
        };

        // Call the searchText API
        const [response] = await client.searchText(request);
        console.log('API Response:', JSON.stringify(response, null, 2));
        
        if (response && response.places && response.places.length > 0) {
            const place = response.places[0];
            
            // Get additional details
            const detailsRequest = {
                name: `places/${place.id}`,
                includedFields: {
                    paths: [
                        'id',
                        'displayName',
                        'formattedAddress',
                        'location',
                        'rating',
                        'userRatingCount',
                        'priceLevel',
                        'regularOpeningHours',
                        'websiteUri',
                        'formattedPhoneNumber',
                        'reviews'
                    ]
                }
            };
            
            const [details] = await client.getPlace(detailsRequest);
            
            return {
                name: place.displayName.text,
                google_place_id: place.id,
                address: place.formattedAddress,
                location: {
                    lat: place.location.latitude,
                    lng: place.location.longitude
                },
                rating: place.rating,
                total_ratings: place.userRatingCount,
                price_level: place.priceLevel,
                details: details
            };
        }
        return null;
    } catch (error) {
        console.error(`Error searching for ${name}:`, error);
        return null;
    }
}

async function main() {
    // Read the restaurants file
    const data = JSON.parse(fs.readFileSync('/opt/noogabites/Results/visitchat/restaurants_20250212_190317_final.json', 'utf8'));
    
    // Get first 3 restaurants
    const firstThree = data.restaurants.slice(0, 3);
    
    console.log('Searching for first 3 restaurants...\n');
    
    for (const restaurant of firstThree) {
        console.log(`Searching for ${restaurant.title}...`);
        const result = await searchPlace(
            restaurant.title,
            restaurant.address1,
            restaurant.latitude,
            restaurant.longitude
        );
        
        if (result) {
            console.log('Found on Google Places:');
            console.log(JSON.stringify(result, null, 2));
            
            // Save to individual file
            const filename = `/opt/noogabites/Results/places/${restaurant.title.toLowerCase().replace(/[^a-z0-9]/g, '_')}_${new Date().toISOString().split('T')[0]}.json`;
            fs.writeFileSync(filename, JSON.stringify({
                visit_chattanooga_data: restaurant,
                google_places_data: result
            }, null, 2));
            console.log(`Saved to ${filename}\n`);
        } else {
            console.log('Not found on Google Places\n');
        }
    }
}

// Create Results/places directory if it doesn't exist
if (!fs.existsSync('/opt/noogabites/Results/places')) {
    fs.mkdirSync('/opt/noogabites/Results/places', { recursive: true });
}

main().catch(console.error);
