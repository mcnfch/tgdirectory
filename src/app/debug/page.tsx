'use client';

import { FilterPane } from './FilterPane';
import { FilterOption, FilterType, SelectedFilters } from '@/types/filter';
import { useState } from 'react';

export default function DebugPage() {
  const [selectedFilters, setSelectedFilters] = useState<SelectedFilters>({
    categories: new Set<string>(),
    districts: new Set<string>(),
    priceRanges: new Set<string>(),
    features: new Set<string>(),
  });

  const handleFilterChange = (type: FilterType, value: string, checked: boolean) => {
    setSelectedFilters((prev) => {
      const newFilters = { ...prev };
      const set = new Set(prev[type]);
      
      if (checked) {
        set.add(value);
      } else {
        set.delete(value);
      }
      
      newFilters[type] = set;
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
