'use client';

import React, { useState, useCallback, useEffect } from 'react';

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
  onFilterChange: (filters: {
    categories: Set<string>;
    districts: Set<string>;
    priceRanges: Set<string>;
    features: Set<string>;
    searchQuery: string;
  }) => void;
  categoryFilters: FilterOption[];
  districtFilters: FilterOption[];
  featureFilters: FilterOption[];
  priceRangeFilters: FilterOption[];
  onReset: () => void;
}

export const FilterPane: React.FC<FilterPaneProps> = ({
  onFilterChange,
  categoryFilters,
  districtFilters,
  featureFilters,
  priceRangeFilters,
  onReset
}) => {
  const [selectedCategories, setSelectedCategories] = useState<Set<string>>(new Set());
  const [selectedDistricts, setSelectedDistricts] = useState<Set<string>>(new Set());
  const [selectedPriceRanges, setSelectedPriceRanges] = useState<Set<string>>(new Set());
  const [selectedFeatures, setSelectedFeatures] = useState<Set<string>>(new Set());
  const [searchQuery, setSearchQuery] = useState('');
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  const handleFilterChange = useCallback(() => {
    onFilterChange({
      categories: selectedCategories,
      districts: selectedDistricts,
      priceRanges: selectedPriceRanges,
      features: selectedFeatures,
      searchQuery
    });
  }, [onFilterChange, selectedCategories, selectedDistricts, selectedPriceRanges, selectedFeatures, searchQuery]);

  useEffect(() => {
    handleFilterChange();
  }, [handleFilterChange]);

  const handleCheckboxChange = (type: string, value: string, checked: boolean) => {
    let targetSet: Set<string>;
    let setFunction: React.Dispatch<React.SetStateAction<Set<string>>>;

    switch (type) {
      case 'categories':
        targetSet = selectedCategories;
        setFunction = setSelectedCategories;
        break;
      case 'districts':
        targetSet = selectedDistricts;
        setFunction = setSelectedDistricts;
        break;
      case 'priceRanges':
        targetSet = selectedPriceRanges;
        setFunction = setSelectedPriceRanges;
        break;
      case 'features':
        targetSet = selectedFeatures;
        setFunction = setSelectedFeatures;
        break;
      default:
        return;
    }

    const newSet = new Set(targetSet);
    if (checked) {
      newSet.add(value);
    } else {
      newSet.delete(value);
    }
    setFunction(newSet);
  };

  const handleReset = () => {
    setSelectedCategories(new Set());
    setSelectedDistricts(new Set());
    setSelectedPriceRanges(new Set());
    setSelectedFeatures(new Set());
    setSearchQuery('');
    onReset();
  };

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
        w-64 bg-white shadow-lg rounded-lg p-4 space-y-6
        z-50 md:z-auto
        overflow-y-auto
      `}>
        {/* Close button for mobile */}
        <button 
          onClick={() => setIsDrawerOpen(false)}
          className="absolute top-4 right-4 md:hidden"
          aria-label="Close filters"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <div className="space-y-6">
          <div className="relative">
            <input
              type="text"
              placeholder="Search restaurants..."
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                handleFilterChange();
              }}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-black placeholder-gray-500"
            />
          </div>

          <FilterSection
            title="Categories"
            items={categoryFilters}
            selectedItems={selectedCategories}
            onChange={(value, checked) => handleCheckboxChange('categories', value, checked)}
          />

          <FilterSection
            title="Districts"
            items={districtFilters}
            selectedItems={selectedDistricts}
            onChange={(value, checked) => handleCheckboxChange('districts', value, checked)}
          />

          <FilterSection
            title="Price Range"
            items={priceRangeFilters}
            selectedItems={selectedPriceRanges}
            onChange={(value, checked) => handleCheckboxChange('priceRanges', value, checked)}
          />

          <FilterSection
            title="Features"
            items={featureFilters}
            selectedItems={selectedFeatures}
            onChange={(value, checked) => handleCheckboxChange('features', value, checked)}
          />

          <button
            onClick={handleReset}
            className="w-full px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-lg hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
          >
            Reset Filters
          </button>
        </div>
      </div>
    </>
  );
};

interface FilterSectionProps {
  title: string;
  items: FilterOption[];
  selectedItems: Set<string>;
  onChange: (value: string, checked: boolean) => void;
}

const FilterSection: React.FC<FilterSectionProps> = ({
  title,
  items,
  selectedItems,
  onChange,
}) => {
  const [expanded, setExpanded] = useState(false);
  const displayItems = expanded ? items : items.slice(0, 5);
  const hasMore = items.length > 5;

  return (
    <div className="mb-6">
      <h3 className="text-lg font-semibold mb-3 text-gray-700">{title}</h3>
      <div className="space-y-2">
        {displayItems.map((item) => (
          <div key={item.id} className="flex items-center">
            <input
              type="checkbox"
              id={item.id}
              checked={selectedItems.has(item.id)}
              onChange={(e) => onChange(item.id, e.target.checked)}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor={item.id} className="ml-2 text-gray-700">
              {item.label} ({item.count})
            </label>
          </div>
        ))}
      </div>
      {hasMore && (
        <button
          onClick={() => setExpanded(!expanded)}
          className="mt-2 text-blue-600 hover:text-blue-800 text-sm font-medium"
        >
          {expanded ? 'Show Less' : 'Show More'}
        </button>
      )}
    </div>
  );
};
