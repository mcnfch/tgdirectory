'use client';

import { DirectoryList } from '@/components/DirectoryListing/DirectoryList';
import { FilterPane } from '@/components/DirectoryListing/FilterPane';
import { DirectoryItem } from '@/types/directory';
import rawData from '@/data/static/live_data.json';
import { useCallback, useMemo, useState } from 'react';

interface Restaurant {
  basic_info: {
    name: string;
    id: string;
    types: string[];
    primary_type: string;
    phone: {
      local: string;
      international: string;
    };
    website: string;
    rating: number;
    rating_count: number;
    description: string;
    district: string;
    district_description: string;
    coordinates: number[];
    price_level?: {
      value: string;
      numeric: number;
    };
  };
  service_options: {
    dine_in: boolean;
    takeout: boolean;
    delivery: boolean;
    curbside_pickup: boolean;
    reservations: boolean;
    outdoor_seating: boolean;
  };
  accessibility: {
    wheelchair_accessible_parking: boolean;
    wheelchair_accessible_entrance: boolean;
    wheelchair_accessible_restroom: boolean;
    wheelchair_accessible_seating: boolean;
  };
  amenities: {
    restroom: boolean;
    good_for_groups: boolean;
    good_for_watching_sports: boolean;
    live_music?: boolean;
    happy_hour?: boolean;
  };
  photos?: Array<{
    name: string;
    widthPx: number;
    heightPx: number;
    authorAttributions: any[];
  }>;
  seo_description: string;
}

type RestaurantData = {
  [key: string]: Restaurant;
}

export default function Home() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFilters, setSelectedFilters] = useState<{
    categories: Set<string>;
    districts: Set<string>;
    priceRanges: Set<string>;
    features: Set<string>;
    searchQuery: string;
  }>({
    categories: new Set(),
    districts: new Set(),
    priceRanges: new Set(),
    features: new Set(),
    searchQuery: '',
  });

  // Transform raw data into DirectoryItems
  const items: DirectoryItem[] = useMemo(() => {
    return Object.values(rawData.restaurants).map((restaurant: any) => ({
      id: restaurant.basic_info?.id,
      title: restaurant.basic_info?.name,
      slug: restaurant.basic_info?.id,
      image: restaurant.photos?.[0]?.name || '',
      address: restaurant.basic_info?.district,
      featured: false,
      rating: restaurant.basic_info?.rating || 0,
      reviewCount: restaurant.basic_info?.rating_count || 0,
      website: restaurant.basic_info?.website || '',
      categories: restaurant.basic_info?.types || [],
      districts: [],
      features: restaurant.amenities || [],
      priceLevel: restaurant.basic_info?.price_level?.numeric || 1,
      hours: null // We'll need to add this data later
    }));
  }, []);

  const handleFilterChange = useCallback((filters: {
    categories: Set<string>;
    districts: Set<string>;
    priceRanges: Set<string>;
    features: Set<string>;
    searchQuery: string;
  }) => {
    setSelectedFilters(filters);
  }, []);

  const handleReset = useCallback(() => {
    setSelectedFilters({
      categories: new Set(),
      districts: new Set(),
      priceRanges: new Set(),
      features: new Set(),
      searchQuery: '',
    });
  }, []);

  // Calculate category counts
  const categoryCounts = Object.values(rawData.restaurants as unknown as RestaurantData).reduce((acc, restaurant) => {
    const types = restaurant.basic_info?.types || [];
    types.forEach(type => {
      if (type) {
        acc[type] = (acc[type] || 0) + 1;
      }
    });
    return acc;
  }, {} as Record<string, number>);

  // Update categoryFilters with actual counts and correct IDs from live data
  const categoryFilters = [
    { id: 'american_restaurant', label: 'American', count: categoryCounts['american_restaurant'] || 0 },
    { id: 'mexican_restaurant', label: 'Mexican', count: categoryCounts['mexican_restaurant'] || 0 },
    { id: 'italian_restaurant', label: 'Italian', count: categoryCounts['italian_restaurant'] || 0 },
    { id: 'asian_restaurant', label: 'Asian', count: categoryCounts['asian_restaurant'] || 0 },
    { id: 'barbecue_restaurant', label: 'BBQ', count: categoryCounts['barbecue_restaurant'] || 0 },
    { id: 'pizza_restaurant', label: 'Pizza', count: categoryCounts['pizza_restaurant'] || 0 },
    { id: 'seafood_restaurant', label: 'Seafood', count: categoryCounts['seafood_restaurant'] || 0 },
    { id: 'steak_house', label: 'Steakhouse', count: categoryCounts['steak_house'] || 0 },
    { id: 'sushi_restaurant', label: 'Sushi', count: categoryCounts['sushi_restaurant'] || 0 },
    { id: 'vegetarian_restaurant', label: 'Vegetarian', count: categoryCounts['vegetarian_restaurant'] || 0 }
  ];

  // Calculate district counts
  const districtCounts = Object.values(rawData.restaurants as unknown as RestaurantData).reduce((acc, restaurant) => {
    const district = restaurant.basic_info?.district;
    if (district) {
      acc[district] = (acc[district] || 0) + 1;
    }
    return acc;
  }, {} as Record<string, number>);

  // Update filterDistricts with actual counts
  const filterDistricts = [
    { id: 'North Chattanooga', label: 'North Chattanooga', count: districtCounts['North Chattanooga'] || 0 },
    { id: 'South Chattanooga', label: 'South Chattanooga', count: districtCounts['South Chattanooga'] || 0 },
    { id: 'Downtown Chattanooga', label: 'Downtown Chattanooga', count: districtCounts['Downtown Chattanooga'] || 0 },
    { id: 'Northgate', label: 'Northgate', count: districtCounts['Northgate'] || 0 },
    { id: 'Hickory Valley', label: 'Hickory Valley', count: districtCounts['Hickory Valley'] || 0 },
    { id: 'Tyner', label: 'Tyner', count: districtCounts['Tyner'] || 0 },
    { id: 'Amnicola', label: 'Amnicola', count: districtCounts['Amnicola'] || 0 },
    { id: 'University of Tennessee at Chattanooga', label: 'UTC', count: districtCounts['University of Tennessee at Chattanooga'] || 0 },
    { id: 'Rock City', label: 'Rock City', count: districtCounts['Rock City'] || 0 },
    { id: 'Brainerd', label: 'Brainerd', count: districtCounts['Brainerd'] || 0 },
    { id: 'Bushtown', label: 'Bushtown', count: districtCounts['Bushtown'] || 0 },
    { id: 'Mountain Creek', label: 'Mountain Creek', count: districtCounts['Mountain Creek'] || 0 },
    { id: 'Ridgedale', label: 'Ridgedale', count: districtCounts['Ridgedale'] || 0 },
    { id: 'Manchester Park', label: 'Manchester Park', count: districtCounts['Manchester Park'] || 0 },
    { id: 'Lansdell Park', label: 'Lansdell Park', count: districtCounts['Lansdell Park'] || 0 },
    { id: 'Woodmore', label: 'Woodmore', count: districtCounts['Woodmore'] || 0 },
    { id: 'Walnut Hills', label: 'Walnut Hills', count: districtCounts['Walnut Hills'] || 0 },
    { id: 'Lookout Valley', label: 'Lookout Valley', count: districtCounts['Lookout Valley'] || 0 }
  ];

  // Calculate feature counts
  const featureCounts = Object.values(rawData.restaurants as unknown as RestaurantData).reduce((acc, restaurant) => {
    const service_options = restaurant.service_options || {};
    const accessibility = restaurant.accessibility || {};

    if (service_options.takeout) acc.takeout = (acc.takeout || 0) + 1;
    if (service_options.delivery) acc.delivery = (acc.delivery || 0) + 1;
    if (service_options.outdoor_seating) acc.outdoor_seating = (acc.outdoor_seating || 0) + 1;
    if (service_options.reservations) acc.reservations = (acc.reservations || 0) + 1;
    
    // Count as wheelchair accessible if it has at least two accessibility features
    if ((accessibility.wheelchair_accessible_entrance === true && 
         accessibility.wheelchair_accessible_parking === true) || 
        (accessibility.wheelchair_accessible_entrance === true && 
         accessibility.wheelchair_accessible_restroom === true) || 
        (accessibility.wheelchair_accessible_parking === true && 
         accessibility.wheelchair_accessible_restroom === true) || 
        (accessibility.wheelchair_accessible_entrance === true && 
         accessibility.wheelchair_accessible_parking === true && 
         accessibility.wheelchair_accessible_restroom === true)) {
      acc.wheelchair_accessible = (acc.wheelchair_accessible || 0) + 1;
    }
    
    return acc;
  }, {} as Record<string, number>);

  // Update filterFeatures with actual counts
  const filterFeatures = [
    { id: 'takeout', label: 'Takeout', count: featureCounts.takeout || 0 },
    { id: 'delivery', label: 'Delivery', count: featureCounts.delivery || 0 },
    { id: 'outdoor_seating', label: 'Outdoor Seating', count: featureCounts.outdoor_seating || 0 },
    { id: 'wheelchair_accessible', label: 'Wheelchair Accessible', count: featureCounts.wheelchair_accessible || 0 },
    { id: 'reservations', label: 'Reservations', count: featureCounts.reservations || 0 }
  ];

  // Calculate price range counts
  const priceRangeCounts = Object.values(rawData.restaurants as unknown as RestaurantData).reduce((acc, restaurant) => {
    const priceLevel = restaurant.basic_info?.price_level?.numeric?.toString();
    if (priceLevel) {
      acc[priceLevel] = (acc[priceLevel] || 0) + 1;
    }
    return acc;
  }, {} as Record<string, number>);

  // Update priceRangeFilters with actual counts
  const priceRangeFilters = [
    { id: '1', label: '$', count: priceRangeCounts['1'] || 0 },
    { id: '2', label: '$$', count: priceRangeCounts['2'] || 0 },
    { id: '3', label: '$$$', count: priceRangeCounts['3'] || 0 },
    { id: '4', label: '$$$$', count: priceRangeCounts['4'] || 0 }
  ];

  // Filter restaurants based on selected filters
  const filteredRestaurants = Object.entries(rawData.restaurants as unknown as RestaurantData)
    .filter(([_, restaurant]) => {
      const categoryArray = Array.from(selectedFilters.categories);
      const districtArray = Array.from(selectedFilters.districts);
      const priceArray = Array.from(selectedFilters.priceRanges);
      const featureArray = Array.from(selectedFilters.features);

      // Apply search filter
      if (selectedFilters.searchQuery) {
        const searchLower = selectedFilters.searchQuery.toLowerCase();
        const name = restaurant.basic_info?.name?.toLowerCase() || '';
        const description = restaurant.basic_info?.description?.toLowerCase() || '';
        const types = restaurant.basic_info?.types?.map(t => t.toLowerCase()) || [];
        const district = restaurant.basic_info?.district?.toLowerCase() || '';
        
        const matchesSearch = 
          name.includes(searchLower) ||
          description.includes(searchLower) ||
          types.some(type => type.includes(searchLower)) ||
          district.includes(searchLower);
        
        if (!matchesSearch) return false;
      }

      // Check categories
      if (categoryArray.length) {
        const restaurantTypes = restaurant.basic_info?.types || [];
        if (!restaurantTypes.some(type => categoryArray.includes(type))) {
          return false;
        }
      }
      
      // Check district
      if (districtArray.length) {
        if (!restaurant.basic_info?.district) return false;
        if (!districtArray.includes(restaurant.basic_info.district)) {
          return false;
        }
      }
      
      // Check price range
      if (priceArray.length && !priceArray.includes(restaurant.basic_info?.price_level?.numeric?.toString() || '')) {
        return false;
      }
      
      // Check features
      if (featureArray.length) {
        const hasAllSelectedFeatures = featureArray.every(feature => {
          switch (feature) {
            case 'takeout':
            case 'delivery':
            case 'outdoor_seating':
            case 'reservations':
              return restaurant.service_options?.[feature] === true;
            case 'wheelchair_accessible':
              const accessibility = restaurant.accessibility || {};
              return (accessibility.wheelchair_accessible_entrance === true && 
                     accessibility.wheelchair_accessible_parking === true) || 
                     (accessibility.wheelchair_accessible_entrance === true && 
                     accessibility.wheelchair_accessible_restroom === true) || 
                     (accessibility.wheelchair_accessible_parking === true && 
                     accessibility.wheelchair_accessible_restroom === true) || 
                     (accessibility.wheelchair_accessible_entrance === true && 
                     accessibility.wheelchair_accessible_parking === true && 
                     accessibility.wheelchair_accessible_restroom === true);
            default:
              return false;
          }
        });
        if (!hasAllSelectedFeatures) return false;
      }
      
      return true;
    })
    .map(([_, restaurant]) => ({
      id: restaurant.basic_info?.id || '',
      title: restaurant.basic_info?.name || '',
      slug: restaurant.basic_info?.id || '',
      image: restaurant.photos?.[0]?.name || '',
      address: restaurant.basic_info?.district || '',
      featured: false,
      rating: restaurant.basic_info?.rating || 0,
      reviewCount: restaurant.basic_info?.rating_count || 0,
      website: restaurant.basic_info?.website || '',
      categories: restaurant.basic_info?.types || [],
      districts: [restaurant.basic_info?.district || ''],
      features: Object.entries(restaurant.amenities || {})
        .filter(([_, value]) => value === true)
        .map(([key]) => key),
      priceLevel: restaurant.basic_info?.price_level?.numeric || 1,
      hours: null,
      service_options: restaurant.service_options,
      accessibility: restaurant.accessibility,
      amenities: restaurant.amenities,
      basic_info: restaurant.basic_info
    }));

  const transformedRestaurants = useMemo(() => {
    return filteredRestaurants.map(restaurant => {
      const serviceOpts = restaurant.service_options || {
        takeout: false,
        delivery: false,
        outdoor_seating: false,
        reservations: false,
        dine_in: false,
        curbside_pickup: false
      };
      
      const accessibilityOpts = restaurant.accessibility || {
        wheelchair_accessible_entrance: false,
        wheelchair_accessible_parking: false,
        wheelchair_accessible_restroom: false,
        wheelchair_accessible_seating: false
      };

      const basicInfo = restaurant.basic_info || {
        district: '',
        types: [],
        price_level: {
          value: 'PRICE_LEVEL_MODERATE',
          numeric: 2
        }
      };
      
      // Collect all active features
      const activeFeatures = [];
      
      // Add service options
      if (serviceOpts.takeout) activeFeatures.push('takeout');
      if (serviceOpts.delivery) activeFeatures.push('delivery');
      if (serviceOpts.outdoor_seating) activeFeatures.push('outdoor_seating');
      if (serviceOpts.reservations) activeFeatures.push('reservations');
      
      // Add wheelchair accessibility if it meets criteria
      if ((accessibilityOpts.wheelchair_accessible_entrance && 
           accessibilityOpts.wheelchair_accessible_parking) || 
          (accessibilityOpts.wheelchair_accessible_entrance && 
           accessibilityOpts.wheelchair_accessible_restroom) || 
          (accessibilityOpts.wheelchair_accessible_parking && 
           accessibilityOpts.wheelchair_accessible_restroom) || 
          (accessibilityOpts.wheelchair_accessible_entrance && 
           accessibilityOpts.wheelchair_accessible_parking && 
           accessibilityOpts.wheelchair_accessible_restroom)) {
        activeFeatures.push('wheelchair_accessible');
      }

      return {
        ...restaurant,
        features: activeFeatures,
        districts: [basicInfo.district].filter(Boolean),
        categories: basicInfo.types
      };
    });
  }, [filteredRestaurants]);

  return (
    <main className="flex min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col md:flex-row gap-8">
          <FilterPane
            categoryFilters={categoryFilters}
            districtFilters={filterDistricts}
            featureFilters={filterFeatures}
            priceRangeFilters={priceRangeFilters}
            onFilterChange={handleFilterChange}
            onReset={handleReset}
          />
          <div className="flex-1">
            <DirectoryList 
              items={transformedRestaurants}
              selectedFilters={selectedFilters}
            />
          </div>
        </div>
      </div>
    </main>
  );
}
