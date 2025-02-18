'use client';

import React, { useState } from 'react';
import { FilterPane } from './FilterPane';

// Sample data
const mockCategories = [
  { id: 'american_restaurant', label: 'American Restaurant', count: 94 },
  { id: 'bar', label: 'Bar', count: 140 },
  { id: 'cafe', label: 'Cafe', count: 76 },
  { id: 'coffee_shop', label: 'Coffee Shop', count: 68 },
  { id: 'italian_restaurant', label: 'Italian Restaurant', count: 45 },
  { id: 'mexican_restaurant', label: 'Mexican Restaurant', count: 38 },
  { id: 'pizza_restaurant', label: 'Pizza Restaurant', count: 32 },
  { id: 'seafood_restaurant', label: 'Seafood Restaurant', count: 28 },
];

const mockDistricts = [
  { id: 'downtown', label: 'Downtown Chattanooga', count: 85 },
  { id: 'north_shore', label: 'North Shore', count: 45 },
  { id: 'southside', label: 'Southside', count: 38 },
  { id: 'east_ridge', label: 'East Ridge', count: 25 },
  { id: 'red_bank', label: 'Red Bank', count: 20 },
  { id: 'lookout_mountain', label: 'Lookout Mountain', count: 15 },
  { id: 'ooltewah', label: 'Ooltewah', count: 12 },
];

const mockPriceRanges = [
  { id: '1', label: '$', count: 120 },
  { id: '2', label: '$$', count: 180 },
  { id: '3', label: '$$$', count: 45 },
  { id: '4', label: '$$$$', count: 15 },
];

const mockFeatures = [
  { id: 'takeout', label: 'Takeout', count: 350 },
  { id: 'delivery', label: 'Delivery', count: 280 },
  { id: 'outdoor_seating', label: 'Outdoor Seating', count: 175 },
  { id: 'wheelchair_accessible', label: 'Wheelchair Accessible', count: 410 },
  { id: 'reservations', label: 'Reservations', count: 145 },
  { id: 'live_music', label: 'Live Music', count: 65 },
  { id: 'happy_hour', label: 'Happy Hour', count: 85 },
];

export default function DebugPage() {
  const [selectedFilters, setSelectedFilters] = useState({
    categories: new Set<string>(),
    districts: new Set<string>(),
    priceRanges: new Set<string>(),
    features: new Set<string>(),
  });

  const handleFilterChange = (type: string, value: string, checked: boolean) => {
    setSelectedFilters(prev => {
      const newFilters = { ...prev };
      const set = new Set(prev[type as keyof typeof prev]);
      
      if (checked) {
        set.add(value);
      } else {
        set.delete(value);
      }
      
      newFilters[type as keyof typeof prev] = set;
      return newFilters;
    });
  };

  const handleReset = () => {
    setSelectedFilters({
      categories: new Set<string>(),
      districts: new Set<string>(),
      priceRanges: new Set<string>(),
      features: new Set<string>(),
    });
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex gap-6">
          <FilterPane
            categories={mockCategories}
            districts={mockDistricts}
            priceRanges={mockPriceRanges}
            features={mockFeatures}
            selectedFilters={selectedFilters}
            onFilterChange={handleFilterChange}
            onReset={handleReset}
          />
          
          {/* Debug Panel */}
          <div className="flex-1 bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold mb-4">Selected Filters</h2>
            <pre className="bg-gray-50 p-4 rounded-lg overflow-auto">
              {JSON.stringify(selectedFilters, null, 2)}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}
