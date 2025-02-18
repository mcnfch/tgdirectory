'use client';

import React, { useState } from 'react';
import { FilterOption, FilterType, SelectedFilters } from '@/types/filter';

interface FilterSection {
  id: FilterType;
  label: string;
  options: FilterOption[];
  selected: Set<string>;
}

interface FilterPaneProps {
  selectedFilters: SelectedFilters;
  onFilterChange: (type: FilterType, value: string, checked: boolean) => void;
  onReset: () => void;
}

// Filter data
const filterCategories = [
  { id: 'american_restaurant', label: 'American Restaurant', count: 94 },
  { id: 'bar', label: 'Bar', count: 140 },
  { id: 'cafe', label: 'Cafe', count: 76 },
  { id: 'coffee_shop', label: 'Coffee Shop', count: 68 },
  { id: 'italian_restaurant', label: 'Italian Restaurant', count: 45 },
  { id: 'mexican_restaurant', label: 'Mexican Restaurant', count: 38 },
  { id: 'pizza_restaurant', label: 'Pizza Restaurant', count: 32 },
  { id: 'seafood_restaurant', label: 'Seafood Restaurant', count: 28 },
];

const filterDistricts = [
  { id: 'downtown', label: 'Downtown Chattanooga', count: 85 },
  { id: 'north_shore', label: 'North Shore', count: 45 },
  { id: 'southside', label: 'Southside', count: 38 },
  { id: 'east_ridge', label: 'East Ridge', count: 25 },
  { id: 'red_bank', label: 'Red Bank', count: 20 },
  { id: 'lookout_mountain', label: 'Lookout Mountain', count: 15 },
  { id: 'ooltewah', label: 'Ooltewah', count: 12 },
];

const filterPriceRanges = [
  { id: '1', label: '$', count: 120 },
  { id: '2', label: '$$', count: 180 },
  { id: '3', label: '$$$', count: 45 },
  { id: '4', label: '$$$$', count: 15 },
];

const filterFeatures = [
  { id: 'takeout', label: 'Takeout', count: 350 },
  { id: 'delivery', label: 'Delivery', count: 280 },
  { id: 'outdoor_seating', label: 'Outdoor Seating', count: 175 },
  { id: 'wheelchair_accessible', label: 'Wheelchair Accessible', count: 410 },
  { id: 'reservations', label: 'Reservations', count: 145 },
  { id: 'live_music', label: 'Live Music', count: 65 },
  { id: 'happy_hour', label: 'Happy Hour', count: 85 },
];

const FilterSection: React.FC<{
  section: FilterSection;
  onFilterChange: (type: FilterType, value: string, checked: boolean) => void;
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
            <span className="text-sm text-gray-600 flex-1 group-hover:text-gray-900">{option.label}</span>
            <span className="text-xs text-gray-500 group-hover:text-gray-700">({option.count})</span>
          </label>
        ))}
      </div>
      {section.options.length > 5 && (
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="mt-3 text-sm text-blue-600 hover:text-blue-800 flex items-center gap-1 transition-colors duration-150"
        >
          {isExpanded ? (
            <>Show Less <i className="fas fa-chevron-up ml-1" /></>
          ) : (
            <>Show All ({section.options.length}) <i className="fas fa-chevron-down ml-1" /></>
          )}
        </button>
      )}
    </div>
  );
};

export function FilterPane({
  selectedFilters,
  onFilterChange,
  onReset,
}: FilterPaneProps) {
  const [isMobileOpen, setIsMobileOpen] = useState(false);

  const sections: FilterSection[] = [
    {
      id: 'categories' as FilterType,
      label: 'Categories',
      options: filterCategories,
      selected: selectedFilters.categories,
    },
    {
      id: 'districts' as FilterType,
      label: 'Districts',
      options: filterDistricts,
      selected: selectedFilters.districts,
    },
    {
      id: 'priceRanges' as FilterType,
      label: 'Price',
      options: filterPriceRanges,
      selected: selectedFilters.priceRanges,
    },
    {
      id: 'features' as FilterType,
      label: 'Features',
      options: filterFeatures,
      selected: selectedFilters.features,
    },
  ];

  const totalFiltersSelected = 
    selectedFilters.categories.size +
    selectedFilters.districts.size +
    selectedFilters.priceRanges.size +
    selectedFilters.features.size;

  return (
    <>
      {/* Mobile Toggle Button */}
      <button 
        onClick={() => setIsMobileOpen(true)}
        className="md:hidden fixed left-4 bottom-4 bg-blue-600 text-white px-4 py-2 rounded-full shadow-lg z-50 flex items-center gap-2"
      >
        <i className="fas fa-filter" />
        Filters
        {totalFiltersSelected > 0 && (
          <span className="bg-white text-blue-600 text-sm px-2 py-0.5 rounded-full">
            {totalFiltersSelected}
          </span>
        )}
      </button>

      {/* Filter Panel */}
      <div className={`
        fixed md:static inset-0 bg-white md:bg-transparent
        transform ${isMobileOpen ? 'translate-x-0' : '-translate-x-full'} md:translate-x-0 
        transition-transform duration-300 ease-in-out
        w-80 md:w-72 h-full md:h-auto
        overflow-y-auto
        p-4 md:p-6
        shadow-xl md:shadow-md
        z-50 md:z-auto
        rounded-none md:rounded-lg
        border-r md:border md:border-gray-200
      `}>
        {/* Mobile Header */}
        <div className="flex justify-between items-center mb-4 md:hidden">
          <h2 className="text-lg font-semibold text-gray-900">Filters</h2>
          <button 
            onClick={() => setIsMobileOpen(false)}
            className="text-gray-500 hover:text-gray-700 p-1"
          >
            <i className="fas fa-times text-xl" />
          </button>
        </div>

        {/* Filter Sections */}
        <div className="space-y-1">
          {sections.map((section) => (
            <FilterSection
              key={section.id}
              section={section}
              onFilterChange={onFilterChange}
            />
          ))}
        </div>

        {/* Reset Button */}
        {totalFiltersSelected > 0 && (
          <button
            onClick={onReset}
            className="mt-6 w-full py-2 px-4 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors duration-150 flex items-center justify-center gap-2"
          >
            <i className="fas fa-times-circle" />
            Clear All Filters
          </button>
        )}
      </div>

      {/* Mobile Overlay */}
      {isMobileOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-25 md:hidden z-40"
          onClick={() => setIsMobileOpen(false)}
        />
      )}
    </>
  );
};
