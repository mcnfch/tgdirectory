'use client';

import { DirectoryList } from '@/components/DirectoryListing/DirectoryList';
import { FilterPane } from '@/components/DirectoryListing/FilterPane';
import { DirectoryItem } from '@/types/directory';
import rawData from '@/data/static/live_data.json';
import { useCallback, useMemo, useState } from 'react';

export default function Home() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [selectedRegions, setSelectedRegions] = useState<string[]>([]);
  const [selectedAmenities, setSelectedAmenities] = useState<string[]>([]);

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
      regions: [],
      amenities: [],
      hours: restaurant.hours || null
    }));
  }, []);

  const categories = [
    { id: "restaurant", label: "ALL Restaurant", count: 229 },
    { id: "cafe", label: "Cafe", count: 38 },
    { id: "bar", label: "Bar", count: 70 }
  ];

  const regions = [
    { id: "downtown", label: "Downtown", count: 122 },
    { id: "airport", label: "Hamilton Place/Airport", count: 35 },
    { id: "neardowntown", label: "Near Downtown", count: 24 }
  ];

  const amenities = [
    { id: "outdoor", label: "Outdoor dining available", count: 67 },
    { id: "delivery", label: "Delivery available", count: 43 },
    { id: "takeout", label: "Offers takeout", count: 87 }
  ];

  const handleFilterChange = useCallback((type: string, value: string) => {
    switch (type) {
      case 'category':
        setSelectedCategories(prev => 
          prev.includes(value) 
            ? prev.filter(cat => cat !== value)
            : [...prev, value]
        );
        break;
      case 'region':
        setSelectedRegions(prev => 
          prev.includes(value)
            ? prev.filter(reg => reg !== value)
            : [...prev, value]
        );
        break;
      case 'amenity':
        setSelectedAmenities(prev => 
          prev.includes(value)
            ? prev.filter(am => am !== value)
            : [...prev, value]
        );
        break;
    }
  }, []);

  const handleReset = useCallback(() => {
    setSelectedCategories([]);
    setSelectedRegions([]);
    setSelectedAmenities([]);
    setSearchTerm('');
  }, []);

  return (
    <main className="min-h-screen p-8">
      <div className="directory-container">
        <FilterPane
          categories={categories}
          regions={regions}
          amenities={amenities}
          onFilterChange={handleFilterChange}
          onReset={handleReset}
        />
        <DirectoryList items={items} />
      </div>
    </main>
  );
}
