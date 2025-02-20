'use client';

import React, { useState } from 'react';

interface FilterOption {
  id: string;
  label: string;
  count: number;
}

interface FilterSection {
  id: string;
  label: string;
  options: FilterOption[];
  selected: Set<string>;
}

interface FilterPaneProps {
  selectedFilters: {
    categories: Set<string>;
    districts: Set<string>;
    priceRanges: Set<string>;
    features: Set<string>;
  };
  onFilterChange: (type: string, value: string, checked: boolean) => void;
  onReset: () => void;
  items: DirectoryItem[];
  searchTerm: string;
  onSearchChange: (term: string) => void;
}

// Helper function to count occurrences
const countOccurrences = (items: DirectoryItem[], key: keyof DirectoryItem, value: string): number => {
  return items.filter(item => {
    if (Array.isArray(item[key])) {
      return (item[key] as string[]).includes(value);
    } else if (key === 'priceLevel') {
      return item[key].toString() === value;
    }
    return false;
  }).length;
};

const FilterSection: React.FC<{
  section: FilterSection;
  onFilterChange: (type: string, value: string, checked: boolean) => void;
}> = ({ section, onFilterChange }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const visibleOptions = isExpanded ? section.options : section.options.slice(0, 5);

  return (
    <div className="py-4 border-b border-gray-200 last:border-0">
      <h3 className="text-lg font-medium text-gray-900 mb-2">{section.label}</h3>
      <div className="space-y-2">
        {visibleOptions.map((option) => (
          <label key={option.id} className="flex items-center space-x-3 group cursor-pointer">
            <input
              type="checkbox"
              className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              checked={section.selected.has(option.id)}
              onChange={(e) => onFilterChange(section.id, option.id, e.target.checked)}
            />
            <span className="text-gray-700 group-hover:text-gray-900">
              {option.label}
              <span className="text-gray-500 ml-1">({option.count})</span>
            </span>
          </label>
        ))}
        {section.options.length > 5 && (
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            {isExpanded ? 'Show Less' : 'Show More'}
          </button>
        )}
      </div>
    </div>
  );
};

export const FilterPane: React.FC<FilterPaneProps> = ({
  selectedFilters,
  onFilterChange,
  onReset,
  items,
  searchTerm,
  onSearchChange
}) => {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    onSearchChange(value);
  };

  // Calculate counts dynamically
  const filterCategories = [
    { id: 'restaurant', label: 'Restaurant', count: countOccurrences(items, 'categories', 'restaurant') },
    { id: 'coffee_shop', label: 'Coffee Shop', count: countOccurrences(items, 'categories', 'coffee_shop') },
    { id: 'bar', label: 'Bar', count: countOccurrences(items, 'categories', 'bar') },
    { id: 'pizza_restaurant', label: 'Pizza Restaurant', count: countOccurrences(items, 'categories', 'pizza_restaurant') },
    { id: 'american_restaurant', label: 'American Restaurant', count: countOccurrences(items, 'categories', 'american_restaurant') },
    { id: 'italian_restaurant', label: 'Italian Restaurant', count: countOccurrences(items, 'categories', 'italian_restaurant') },
    { id: 'barbecue_restaurant', label: 'BBQ Restaurant', count: countOccurrences(items, 'categories', 'barbecue_restaurant') },
    { id: 'steak_house', label: 'Steak House', count: countOccurrences(items, 'categories', 'steak_house') },
    { id: 'mexican_restaurant', label: 'Mexican Restaurant', count: countOccurrences(items, 'categories', 'mexican_restaurant') },
    { id: 'cafe', label: 'Cafe', count: countOccurrences(items, 'categories', 'cafe') },
    { id: 'ice_cream_shop', label: 'Ice Cream Shop', count: countOccurrences(items, 'categories', 'ice_cream_shop') },
    { id: 'fast_food_restaurant', label: 'Fast Food', count: countOccurrences(items, 'categories', 'fast_food_restaurant') },
    { id: 'seafood_restaurant', label: 'Seafood Restaurant', count: countOccurrences(items, 'categories', 'seafood_restaurant') },
    { id: 'sandwich_shop', label: 'Sandwich Shop', count: countOccurrences(items, 'categories', 'sandwich_shop') },
    { id: 'mediterranean_restaurant', label: 'Mediterranean', count: countOccurrences(items, 'categories', 'mediterranean_restaurant') },
    { id: 'breakfast_restaurant', label: 'Breakfast Restaurant', count: countOccurrences(items, 'categories', 'breakfast_restaurant') },
    { id: 'bar_and_grill', label: 'Bar & Grill', count: countOccurrences(items, 'categories', 'bar_and_grill') },
    { id: 'bakery', label: 'Bakery', count: countOccurrences(items, 'categories', 'bakery') },
    { id: 'thai_restaurant', label: 'Thai Restaurant', count: countOccurrences(items, 'categories', 'thai_restaurant') },
    { id: 'sushi_restaurant', label: 'Sushi Restaurant', count: countOccurrences(items, 'categories', 'sushi_restaurant') },
    { id: 'pub', label: 'Pub', count: countOccurrences(items, 'categories', 'pub') },
    { id: 'juice_shop', label: 'Juice Shop', count: countOccurrences(items, 'categories', 'juice_shop') },
    { id: 'japanese_restaurant', label: 'Japanese Restaurant', count: countOccurrences(items, 'categories', 'japanese_restaurant') },
    { id: 'chinese_restaurant', label: 'Chinese Restaurant', count: countOccurrences(items, 'categories', 'chinese_restaurant') },
    { id: 'brunch_restaurant', label: 'Brunch Restaurant', count: countOccurrences(items, 'categories', 'brunch_restaurant') },
    { id: 'brazilian_restaurant', label: 'Brazilian Restaurant', count: countOccurrences(items, 'categories', 'brazilian_restaurant') },
    { id: 'vegan_restaurant', label: 'Vegan Restaurant', count: countOccurrences(items, 'categories', 'vegan_restaurant') },
    { id: 'korean_restaurant', label: 'Korean Restaurant', count: countOccurrences(items, 'categories', 'korean_restaurant') },
    { id: 'greek_restaurant', label: 'Greek Restaurant', count: countOccurrences(items, 'categories', 'greek_restaurant') },
    { id: 'french_restaurant', label: 'French Restaurant', count: countOccurrences(items, 'categories', 'french_restaurant') },
    { id: 'donut_shop', label: 'Donut Shop', count: countOccurrences(items, 'categories', 'donut_shop') },
    { id: 'dessert_shop', label: 'Dessert Shop', count: countOccurrences(items, 'categories', 'dessert_shop') },
    { id: 'deli', label: 'Deli', count: countOccurrences(items, 'categories', 'deli') },
    { id: 'chocolate_shop', label: 'Chocolate Shop', count: countOccurrences(items, 'categories', 'chocolate_shop') },
    { id: 'asian_restaurant', label: 'Asian Restaurant', count: countOccurrences(items, 'categories', 'asian_restaurant') }
  ].filter(cat => cat.count > 0);

  const filterDistricts = [
    { id: 'downtown_chattanooga', label: 'Downtown Chattanooga', count: countOccurrences(items, 'districts', 'downtown_chattanooga') },
    { id: 'north_chattanooga', label: 'North Chattanooga', count: countOccurrences(items, 'districts', 'north_chattanooga') },
    { id: 'south_chattanooga', label: 'South Chattanooga', count: countOccurrences(items, 'districts', 'south_chattanooga') },
    { id: 'brainerd', label: 'Brainerd', count: countOccurrences(items, 'districts', 'brainerd') },
    { id: 'northgate', label: 'Northgate', count: countOccurrences(items, 'districts', 'northgate') },
    { id: 'lookout_valley', label: 'Lookout Valley', count: countOccurrences(items, 'districts', 'lookout_valley') },
    { id: 'amnicola', label: 'Amnicola', count: countOccurrences(items, 'districts', 'amnicola') },
    { id: 'utc', label: 'UTC Area', count: countOccurrences(items, 'districts', 'utc') },
    { id: 'ridgedale', label: 'Ridgedale', count: countOccurrences(items, 'districts', 'ridgedale') },
    { id: 'riverview', label: 'Riverview', count: countOccurrences(items, 'districts', 'riverview') }
  ].filter(dist => dist.count > 0);

  const filterFeatures = [
    { id: 'dine_in', label: 'Dine In', count: countOccurrences(items, 'features', 'dine_in') },
    { id: 'takeout', label: 'Takeout', count: countOccurrences(items, 'features', 'takeout') },
    { id: 'delivery', label: 'Delivery', count: countOccurrences(items, 'features', 'delivery') },
    { id: 'outdoor_seating', label: 'Outdoor Seating', count: countOccurrences(items, 'features', 'outdoor_seating') },
    { id: 'reservations', label: 'Reservations', count: countOccurrences(items, 'features', 'reservations') },
    { id: 'curbside_pickup', label: 'Curbside Pickup', count: countOccurrences(items, 'features', 'curbside_pickup') },
    { id: 'good_for_groups', label: 'Good for Groups', count: countOccurrences(items, 'features', 'good_for_groups') },
    { id: 'good_for_watching_sports', label: 'Sports Viewing', count: countOccurrences(items, 'features', 'good_for_watching_sports') },
    { id: 'wheelchair_accessible', label: 'Wheelchair Accessible', count: countOccurrences(items, 'features', 'wheelchair_accessible') }
  ].filter(feat => feat.count > 0);

  const filterPriceRanges = [
    { id: '1', label: '$', count: items.filter(item => item.priceLevel === 1).length },
    { id: '2', label: '$$', count: items.filter(item => item.priceLevel === 2).length },
    { id: '3', label: '$$$', count: items.filter(item => item.priceLevel === 3).length },
    { id: '4', label: '$$$$', count: items.filter(item => item.priceLevel === 4).length }
  ].filter(price => price.count > 0);

  const sections: FilterSection[] = [
    {
      id: 'categories',
      label: 'Categories',
      options: filterCategories,
      selected: selectedFilters.categories,
    },
    {
      id: 'districts',
      label: 'Districts',
      options: filterDistricts,
      selected: selectedFilters.districts,
    },
    {
      id: 'priceRanges',
      label: 'Price Range',
      options: filterPriceRanges,
      selected: selectedFilters.priceRanges,
    },
    {
      id: 'features',
      label: 'Features',
      options: filterFeatures,
      selected: selectedFilters.features,
    },
  ];

  return (
    <>
      {/* Mobile drawer tab */}
      <button 
        onClick={() => setIsDrawerOpen(true)}
        className={`fixed left-4 top-4 bg-white shadow-lg rounded-lg p-2 z-50 md:hidden ${isDrawerOpen ? 'hidden' : 'block'}`}
        aria-label="Open filters"
      >
        <div className="flex items-center space-x-1">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          <span className="text-sm font-medium text-gray-700">Filters</span>
        </div>
      </button>

      {/* Overlay for mobile */}
      {isDrawerOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
          onClick={() => setIsDrawerOpen(false)}
        />
      )}

      {/* Filter pane content */}
      <div className={`
        fixed md:static top-0 left-0 h-full md:h-auto
        transform ${isDrawerOpen ? 'translate-x-0' : '-translate-x-full'} md:translate-x-0
        transition-transform duration-300 ease-in-out
        w-64 bg-white shadow-lg md:shadow-none rounded-lg p-4 space-y-6
        z-50 overflow-y-auto
      `}>
        {/* Close button for mobile */}
        <button 
          onClick={() => setIsDrawerOpen(false)}
          className="absolute top-4 right-4 md:hidden text-gray-500 hover:text-gray-700"
          aria-label="Close filters"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        {/* Search input */}
        <div className="relative">
          <input
            type="text"
            placeholder="Search..."
            value={searchTerm}
            onChange={handleSearchChange}
            className="w-full px-4 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-black"
          />
          {searchTerm ? (
            <button
              onClick={() => onSearchChange('')}
              className="absolute right-10 top-2.5 h-5 w-5 text-gray-400 hover:text-gray-600"
              aria-label="Clear search"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </button>
          ) : null}
          <svg
            className="absolute right-3 top-2.5 h-5 w-5 text-gray-400"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fillRule="evenodd"
              d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
              clipRule="evenodd"
            />
          </svg>
        </div>

        {/* Reset button */}
        <div className="flex justify-between items-center">
          <h2 className="text-lg font-medium text-gray-900">Filters</h2>
          <button
            onClick={onReset}
            className="text-sm text-blue-600 hover:text-blue-800"
          >
            Reset all
          </button>
        </div>

        {/* Filter sections */}
        {sections.map((section) => (
          <FilterSection
            key={section.id}
            section={section}
            onFilterChange={onFilterChange}
          />
        ))}
      </div>
    </>
  );
};
