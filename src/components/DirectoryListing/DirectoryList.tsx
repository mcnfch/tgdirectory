'use client';

import React, { useMemo } from 'react';
import '@fortawesome/fontawesome-free/css/all.min.css';
import Image from 'next/image';
import { DirectoryItem } from '@/types/directory';
import { isRestaurantOpen } from '@/utils/dateUtils';
import dynamic from 'next/dynamic';

const FilterPane = dynamic(
  () => import('./FilterPane').then(mod => mod.FilterPane),
  { ssr: false }
);

interface DirectoryListProps {
  items: DirectoryItem[];
  selectedFilters: {
    categories: Set<string>;
    districts: Set<string>;
    priceRanges: Set<string>;
    features: Set<string>;
  };
}

export const DirectoryList: React.FC<DirectoryListProps> = ({ items = [], selectedFilters }) => {
  const [viewMode, setViewMode] = React.useState<'list' | 'grid-view'>('grid-view');
  const [currentPage, setCurrentPage] = React.useState(1);
  const itemsPerPage = 6;

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const totalPages = Math.ceil(items.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentItems = items.slice(startIndex, endIndex);

  // Filter items based on selected filters
  const filteredItems = useMemo(() => {
    return currentItems.filter(item => {
      // Apply category filters
      if (selectedFilters.categories.size > 0) {
        const hasMatchingCategory = item.categories.some(cat => 
          selectedFilters.categories.has(cat)
        );
        if (!hasMatchingCategory) return false;
      }

      // Apply district filters
      if (selectedFilters.districts.size > 0) {
        const hasMatchingDistrict = item.districts.some(dist => 
          selectedFilters.districts.has(dist)
        );
        if (!hasMatchingDistrict) return false;
      }

      // Apply price range filters
      if (selectedFilters.priceRanges.size > 0 && !selectedFilters.priceRanges.has(item.priceLevel.toString())) {
        return false;
      }

      // Apply feature filters
      if (selectedFilters.features.size > 0) {
        const hasMatchingFeature = item.features.some(feat =>
          selectedFilters.features.has(feat)
        );
        if (!hasMatchingFeature) return false;
      }

      return true;
    });
  }, [currentItems, selectedFilters]);

  const getFirstPhotoPath = (id: string) => {
    return `/media/${id}/photo_1.jpg`;
  };

  // Filter out generic types
  const excludedTypes = [
    'establishment',
    'store',
    'food_store',
    'point_of_interest',
    'food',
    'business'
  ];

  const getPrimaryType = (types: string[]) => {
    return types.find(type => !excludedTypes.includes(type)) || '';
  };

  const getRelevantCategories = (types: string[]) => {
    return types
      .filter(type => !excludedTypes.includes(type))
      .filter(type => type !== getPrimaryType(types))
      .slice(0, 2); // Limit to 2 additional categories
  };

  const getCategoryIcon = (type: string) => {
    switch (type) {
      case 'american_restaurant': return 'fa-utensils';
      case 'asian_restaurant': return 'fa-bowl-rice';
      case 'brazilian_restaurant': return 'fa-drumstick-bite';
      case 'barbecue_restaurant': return 'fa-fire';
      case 'breakfast_restaurant': return 'fa-bacon';
      case 'brunch_restaurant': return 'fa-egg';
      case 'chinese_restaurant': return 'fa-bowl-food';
      case 'french_restaurant': return 'fa-wine-glass';
      case 'greek_restaurant': return 'fa-olive';
      case 'hamburger_restaurant': return 'fa-hamburger';
      case 'italian_restaurant': return 'fa-pizza-slice';
      case 'japanese_restaurant': return 'fa-fan';
      case 'korean_restaurant': return 'fa-pepper-hot';
      case 'mediterranean_restaurant': return 'fa-lemon';
      case 'mexican_restaurant': return 'fa-pepper-hot';
      case 'pizza_restaurant': return 'fa-pizza-slice';
      case 'seafood_restaurant': return 'fa-fish';
      case 'steak_house': return 'fa-drumstick-bite';
      case 'sushi_restaurant': return 'fa-fish';
      case 'thai_restaurant': return 'fa-leaf';
      case 'vegan_restaurant': return 'fa-seedling';
      case 'vegetarian_restaurant': return 'fa-carrot';
      case 'bagel_shop': return 'fa-bagel';
      case 'bakery': return 'fa-bread-slice';
      case 'bar': return 'fa-beer-mug-empty';
      case 'bar_and_grill': return 'fa-fire';
      case 'cafe': return 'fa-mug-hot';
      case 'coffee_shop': return 'fa-coffee';
      case 'confectionery': return 'fa-candy-cane';
      case 'deli': return 'fa-cheese';
      case 'dessert_shop': return 'fa-ice-cream';
      case 'diner': return 'fa-utensils';
      case 'donut_shop': return 'fa-donut';
      case 'fast_food_restaurant': return 'fa-hamburger';
      case 'fine_dining_restaurant': return 'fa-champagne-glasses';
      case 'ice_cream_shop': return 'fa-ice-cream';
      case 'juice_shop': return 'fa-blender';
      case 'pub': return 'fa-beer-mug-empty';
      case 'sandwich_shop': return 'fa-sandwich';
      case 'wine_bar': return 'fa-wine-glass-alt';
      default: return 'fa-utensils';
    }
  };

  const capitalizeWords = (str: string) => {
    return str.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  };

  const generatePageNumbers = () => {
    const pageNumbers = [];
    
    if (totalPages <= 7) {
      // If we have 7 or fewer pages, show all
      for (let i = 1; i <= totalPages; i++) {
        pageNumbers.push(i);
      }
    } else {
      // Always show first page
      if (currentPage <= 4) {
        // Near the start: show 1,2,3,4,5 ... lastPage
        for (let i = 1; i <= 5; i++) {
          pageNumbers.push(i);
        }
        pageNumbers.push('...');
        pageNumbers.push(totalPages);
      } else if (currentPage >= totalPages - 3) {
        // Near the end: show 1 ... lastPage-4,lastPage-3,lastPage-2,lastPage-1,lastPage
        pageNumbers.push(1);
        pageNumbers.push('...');
        for (let i = totalPages - 4; i <= totalPages; i++) {
          pageNumbers.push(i);
        }
      } else {
        // In the middle: show 1 ... currentPage-1,currentPage,currentPage+1 ... lastPage
        pageNumbers.push(1);
        pageNumbers.push('...');
        for (let i = currentPage - 1; i <= currentPage + 1; i++) {
          pageNumbers.push(i);
        }
        pageNumbers.push('...');
        pageNumbers.push(totalPages);
      }
    }
    
    return pageNumbers;
  };

  const generateListingUrl = (name: string, id: string) => {
    const slug = name
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-|-$/g, '');
    const idSuffix = id.slice(-6);
    return `https://noogabites.com/listing/${slug}-${idSuffix}`;
  };

  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-4">
        <div className="text-sm text-gray-500">
          Showing {startIndex + 1}-{Math.min(startIndex + itemsPerPage, items.length)} of {items.length} restaurants
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setViewMode('list')}
            className={`p-2 rounded-md transition-colors duration-150 ${
              viewMode === 'list'
                ? 'bg-gray-200 text-gray-800'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            <i className="fas fa-list" />
          </button>
          <button
            onClick={() => setViewMode('grid-view')}
            className={`p-2 rounded-md transition-colors duration-150 ${
              viewMode === 'grid-view'
                ? 'bg-gray-200 text-gray-800'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            <i className="fas fa-th-large" />
          </button>
        </div>
      </div>

      <div className={`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8`}>
        {currentItems.map((item, index) => (
          <div key={item.id} 
               onClick={() => window.location.href = generateListingUrl(item.title, item.id)}
               className={`
                 bg-white rounded-lg shadow-md overflow-hidden cursor-pointer
                 transition-transform duration-200 hover:scale-[1.02]
                 ${viewMode === 'list' ? 'flex gap-4' : ''}
               `}
          >
            <div className={`relative ${viewMode === 'list' ? 'w-48 h-32' : 'w-full h-48'}`}>
              <Image
                src={getFirstPhotoPath(item.id)}
                alt={item.title}
                fill
                className="object-cover"
                sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                priority={index === 0 && currentPage === 1}
                loading={index === 0 && currentPage === 1 ? 'eager' : 'lazy'}
              />
            </div>
            <div className={`info p-4 ${viewMode === 'list' ? 'flex-1' : ''}`}>
              <div className="top-info">
                <h4 className="title text-gray-900 hover:text-blue-600 text-lg font-medium">
                  {item.title}
                </h4>
                <div className="meta mt-2">
                  <div className="flex items-center gap-4">
                    {item.rating && (
                      <div className="rating flex items-center gap-1">
                        <i className="fas fa-star text-yellow-400"></i>
                        <span className="score text-gray-900 font-semibold">{item.rating}</span>
                        <span className="reviews text-gray-500">({item.reviewCount})</span>
                      </div>
                    )}
                    {item.hours?.schedule && (
                      <div className="flex items-center gap-1">
                        <span className={`w-2 h-2 rounded-full ${isRestaurantOpen(item.hours.schedule) ? 'bg-green-500' : 'bg-red-500'}`}></span>
                        <span className={`text-sm ${isRestaurantOpen(item.hours.schedule) ? 'text-green-700' : 'text-red-700'}`}>
                          {isRestaurantOpen(item.hours.schedule) ? 'Open' : 'Closed'}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
                {getPrimaryType(item.categories || '') && (
                  <div className="restaurant-type mt-2">
                    <span className="type flex items-center gap-2 text-gray-600">
                      <i className={`fas ${getCategoryIcon(getPrimaryType(item.categories || ''))} text-gray-500`}></i>
                      <span>{capitalizeWords(getPrimaryType(item.categories || '').replace(/_/g, ' '))}</span>
                    </span>
                    {getRelevantCategories(item.categories || '').length > 0 && (
                      <div className="additional-categories mt-1 text-sm text-gray-500">
                        {getRelevantCategories(item.categories || '').map(category => (
                          <span key={category} className="mr-2">
                            • {capitalizeWords(category.replace(/_/g, ' '))}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {totalPages > 1 && (
        <div className="flex justify-center items-center space-x-2 mt-8">
          <button
            onClick={() => handlePageChange(1)}
            disabled={currentPage === 1}
            className={`p-2 rounded-md transition-colors duration-150 ${
              currentPage === 1
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            <i className="fas fa-angle-double-left" />
          </button>
          <button
            onClick={() => handlePageChange(currentPage - 1)}
            disabled={currentPage === 1}
            className={`p-2 rounded-md transition-colors duration-150 ${
              currentPage === 1
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            <i className="fas fa-angle-left" />
          </button>

          {/* Page Numbers */}
          <div className="flex space-x-2">
            {generatePageNumbers().map((pageNum, index) => (
              <React.Fragment key={index}>
                {typeof pageNum === 'string' ? (
                  <span className="px-2 py-1">...</span>
                ) : (
                  <button
                    onClick={() => handlePageChange(pageNum)}
                    className={`w-8 h-8 rounded-md transition-colors duration-150 ${
                      pageNum === currentPage
                        ? 'bg-gray-800 text-white'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                  >
                    {pageNum}
                  </button>
                )}
              </React.Fragment>
            ))}
          </div>

          <button
            onClick={() => handlePageChange(currentPage + 1)}
            disabled={currentPage === totalPages}
            className={`p-2 rounded-md transition-colors duration-150 ${
              currentPage === totalPages
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            <i className="fas fa-angle-right" />
          </button>
          <button
            onClick={() => handlePageChange(totalPages)}
            disabled={currentPage === totalPages}
            className={`p-2 rounded-md transition-colors duration-150 ${
              currentPage === totalPages
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            <i className="fas fa-angle-double-right" />
          </button>
        </div>
      )}
    </div>
  );
};
