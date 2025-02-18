'use client';

import { DirectoryList } from '@/components/DirectoryListing/DirectoryList';
import { FilterPane } from '@/components/DirectoryListing/FilterPane';
import { DirectoryItem } from '@/types/directory';
import rawData from '@/data/static/live_data.json';
import { useCallback, useMemo, useState } from 'react';

export default function Home() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategories, setSelectedCategories] = useState<Set<string>>(new Set());
  const [selectedDistricts, setSelectedDistricts] = useState<Set<string>>(new Set());
  const [selectedPriceRanges, setSelectedPriceRanges] = useState<Set<string>>(new Set());
  const [selectedFeatures, setSelectedFeatures] = useState<Set<string>>(new Set());

  // Transform raw data into DirectoryItems
  const items: DirectoryItem[] = useMemo(() => {
    return Object.values(rawData.restaurants).map((restaurant: any) => ({
      id: restaurant.basic_info.id,
      title: restaurant.basic_info.name,
      slug: restaurant.basic_info.id,
      image: restaurant.photos?.[0]?.name || '/placeholder.jpg',
      address: restaurant.location?.formatted_address || '',
      featured: false,
      rating: restaurant.basic_info.rating || 0,
      reviewCount: restaurant.basic_info.rating_count || 0,
      website: restaurant.basic_info.website || '',
      categories: restaurant.basic_info.types || [],
      districts: [],
      features: [],
      priceLevel: restaurant.basic_info.price_level || 1,
      hours: restaurant.hours || null
    }));
  }, []);

  const handleFilterChange = useCallback((type: string, value: string, checked: boolean) => {
    switch (type) {
      case 'categories':
        setSelectedCategories(prev => {
          const next = new Set(prev);
          if (checked) {
            next.add(value);
          } else {
            next.delete(value);
          }
          return next;
        });
        break;
      case 'districts':
        setSelectedDistricts(prev => {
          const next = new Set(prev);
          if (checked) {
            next.add(value);
          } else {
            next.delete(value);
          }
          return next;
        });
        break;
      case 'priceRanges':
        setSelectedPriceRanges(prev => {
          const next = new Set(prev);
          if (checked) {
            next.add(value);
          } else {
            next.delete(value);
          }
          return next;
        });
        break;
      case 'features':
        setSelectedFeatures(prev => {
          const next = new Set(prev);
          if (checked) {
            next.add(value);
          } else {
            next.delete(value);
          }
          return next;
        });
        break;
    }
  }, []);

  const handleReset = useCallback(() => {
    setSelectedCategories(new Set());
    setSelectedDistricts(new Set());
    setSelectedPriceRanges(new Set());
    setSelectedFeatures(new Set());
    setSearchTerm('');
  }, []);

  const selectedFilters = {
    categories: selectedCategories,
    districts: selectedDistricts,
    priceRanges: selectedPriceRanges,
    features: selectedFeatures
  };

  return (
    <main className="min-h-screen p-8">
      <div className="directory-container flex gap-6">
        <FilterPane
          selectedFilters={selectedFilters}
          onFilterChange={handleFilterChange}
          onReset={handleReset}
        />
        <DirectoryList 
          items={items} 
          selectedFilters={selectedFilters}
        />
      </div>
    </main>
  );
}
