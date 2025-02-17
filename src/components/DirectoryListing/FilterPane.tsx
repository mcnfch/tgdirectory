'use client';

import React from 'react';

export interface FilterOption {
  id: string;
  label: string;
  count: number;
}

export interface FilterPaneProps {
  categories: FilterOption[];
  regions: FilterOption[];
  amenities: FilterOption[];
  onFilterChange: (type: string, value: string) => void;
  onReset: () => void;
}

export const FilterPane: React.FC<FilterPaneProps> = ({
  categories,
  regions,
  amenities,
  onFilterChange,
  onReset
}) => {
  const [isOpen, setIsOpen] = React.useState(false);

  const togglePane = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      <button 
        onClick={togglePane}
        className={`md:hidden fixed left-0 top-1/2 -translate-y-1/2 bg-gray-900 text-white p-3 rounded-r-md shadow-lg z-50 hover:bg-gray-800 border border-gray-700 transition-opacity duration-300 ${isOpen ? 'opacity-0 pointer-events-none' : 'opacity-100'}`}
        aria-label="Open filters"
      >
        <i className="fas fa-chevron-right text-lg"></i>
      </button>

      <div className={`
        fixed md:static top-0 left-0 h-full md:h-auto w-72 
        transform ${isOpen ? 'translate-x-0' : '-translate-x-full'} md:translate-x-0 
        transition-transform duration-300 ease-in-out 
        bg-white p-4 rounded-lg shadow-md flex-shrink-0 
        overflow-y-auto md:block z-40
        border border-gray-200
      `}>
        <div className="flex justify-between items-center mb-4 md:hidden">
          <h2 className="text-lg font-semibold text-gray-900">Filters</h2>
          <button 
            onClick={togglePane}
            className="p-2 text-gray-700 hover:text-gray-900 rounded-full hover:bg-gray-100"
            aria-label="Close filters"
          >
            <i className="fas fa-times text-lg"></i>
          </button>
        </div>

        <div data-type="keyword" className="filter">
          <div className="keyword">
            <div className="filterLabel text-gray-900">Keyword</div>
            <div className="keyword-input">
              <input 
                type="text" 
                placeholder="Search" 
                aria-label="Search"
                className="w-full p-2 border border-gray-300 rounded-md text-gray-700 placeholder-gray-500"
              />
              <button 
                type="submit" 
                aria-label="filter on keyword"
                className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-700 hover:text-gray-900"
              >
                <i className="fa fa-search"></i>
              </button>
            </div>
          </div>
        </div>

        <div data-type="checkbox" className="filter">
          <fieldset>
            <legend className="filterLabel text-gray-900">Categories</legend>
            <ul className="space-y-2">
              {categories.map((category) => (
                <li key={category.id}>
                  <input
                    type="checkbox"
                    id={category.id}
                    className="hidden"
                    onChange={() => onFilterChange('category', category.id)}
                  />
                  <label htmlFor={category.id} className="cursor-pointer text-gray-700 hover:text-gray-900">
                    <span className="custom-checkbox border-gray-400">
                      <i className="fas fa-check"></i>
                    </span>
                    {category.label}
                    <span className="text-gray-700">({category.count})</span>
                  </label>
                </li>
              ))}
            </ul>
          </fieldset>
        </div>

        <div data-type="checkbox" className="filter">
          <fieldset>
            <legend className="filterLabel text-gray-900">Regions</legend>
            <ul className="space-y-2">
              {regions.map((region) => (
                <li key={region.id}>
                  <input
                    type="checkbox"
                    id={region.id}
                    className="hidden"
                    onChange={() => onFilterChange('region', region.id)}
                  />
                  <label htmlFor={region.id} className="cursor-pointer text-gray-700 hover:text-gray-900">
                    <span className="custom-checkbox border-gray-400">
                      <i className="fas fa-check"></i>
                    </span>
                    {region.label}
                    <span className="text-gray-700">({region.count})</span>
                  </label>
                </li>
              ))}
            </ul>
          </fieldset>
        </div>

        <div data-type="checkbox" className="filter">
          <fieldset>
            <legend className="filterLabel text-gray-900">Amenities</legend>
            <ul className="space-y-2">
              {amenities.map((amenity) => (
                <li key={amenity.id}>
                  <input
                    type="checkbox"
                    id={amenity.id}
                    className="hidden"
                    onChange={() => onFilterChange('amenity', amenity.id)}
                  />
                  <label htmlFor={amenity.id} className="cursor-pointer text-gray-700 hover:text-gray-900">
                    <span className="custom-checkbox border-gray-400">
                      <i className="fas fa-check"></i>
                    </span>
                    {amenity.label}
                    <span className="text-gray-700">({amenity.count})</span>
                  </label>
                </li>
              ))}
            </ul>
          </fieldset>
        </div>

        <button 
          onClick={onReset} 
          className="resetButton border-red-300 text-red-700 hover:bg-red-50"
        >
          <i className="fas fa-undo mr-2"></i>
          Reset Filters
        </button>
      </div>

      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-30 md:hidden"
          onClick={togglePane}
          aria-hidden="true"
        ></div>
      )}
    </>
  );
};
