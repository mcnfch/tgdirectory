'use client';

import React, { useMemo } from 'react';
import '@fortawesome/fontawesome-free/css/all.min.css';
import Image from 'next/image';
import { DirectoryItem } from '@/types/directory';
import { isRestaurantOpen } from '@/utils/dateUtils';
import dynamic from 'next/dynamic';

const FilterPane = dynamic(() => import('./FilterPane'), {
  ssr: false
});

interface DirectoryListProps {
  items: DirectoryItem[];
}

export const DirectoryList: React.FC<DirectoryListProps> = ({ items = [] }) => {
  const [viewMode, setViewMode] = React.useState<'list' | 'grid-view'>('grid-view');
  const [currentPage, setCurrentPage] = React.useState(1);
  const itemsPerPage = 6;

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const totalPages = Math.ceil(items.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const currentItems = items.slice(startIndex, startIndex + itemsPerPage);

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

  const getPageNumbers = () => {
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

  // Memoize the filtered items
  const displayItems = useMemo(() => currentItems, [currentItems]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className={`grid ${viewMode === 'grid-view' ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6' : 'grid-cols-1 gap-4'}`}>
        {displayItems.map((item, index) => (
          <div key={item.id} className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200">
            <div className="relative h-64 w-full">
              <Image
                src={getFirstPhotoPath(item.id)}
                alt={item.title}
                fill
                sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
                className="object-cover rounded-t-lg"
                priority={index === 0 && currentPage === 1}
                loading={index === 0 && currentPage === 1 ? 'eager' : 'lazy'}
                quality={75}
                placeholder="blur"
                blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb/2wBDABQODxIPDRQSEBIXFRQdHx4dHRsdHR4dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR3/2wBDAR4WFiMeJRwlJRwlHR4dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR3/wAARCAAIAAoDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAb/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k="
              />
            </div>
            <div className="info">
              <div className="top-info">
                <h4>
                  <a href={`/listing/${item.slug}`} className="title text-gray-900 hover:text-blue-600">
                    {item.title}
                  </a>
                </h4>
                <div className="meta">
                  <div className="flex items-center justify-between">
                    {item.rating && (
                      <div className="rating">
                        <span className="score text-gray-900 font-semibold">{item.rating}</span>
                        <span className="reviews text-gray-700">({item.reviewCount})</span>
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
                  <div className="address text-gray-700">{item.address}</div>
                </div>
                {getPrimaryType(item.categories || '') && (
                  <div className="restaurant-type">
                    <span className="type">
                      <i className={`fas ${getCategoryIcon(getPrimaryType(item.categories || ''))}`}></i>
                      <span>{capitalizeWords(getPrimaryType(item.categories || '').replace(/_/g, ' '))}</span>
                    </span>
                  </div>
                )}
                {getRelevantCategories(item.categories || '').length > 0 && (
                  <div className="categories">
                    {getRelevantCategories(item.categories || '').map((category, index) => (
                      <span key={index} className="category">
                        <i className={`fas ${getCategoryIcon(category)}`}></i>
                        <span>{capitalizeWords(category.replace(/_/g, ' '))}</span>
                      </span>
                    ))}
                  </div>
                )}
              </div>
              <div className="bottom-actions">
                <div className="website-link">
                  {item.website && (
                    <a href={item.website} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800 text-sm">
                      Visit website
                    </a>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {totalPages > 1 && (
        <div className="pagination flex flex-col sm:flex-row items-center justify-center gap-2 mt-6">
          <div className="hidden sm:block">
            <button
              onClick={() => handlePageChange(1)}
              disabled={currentPage === 1}
              className={`px-3 py-1 rounded-md border ${
                currentPage === 1
                  ? 'bg-gray-100 text-gray-400 border-gray-300'
                  : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'
              }`}
            >
              First
            </button>
          </div>
          <div className="order-2 sm:order-none flex gap-2 sm:gap-0">
            <button
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage === 1}
              className={`px-3 py-1 rounded-md border ${
                currentPage === 1
                  ? 'bg-gray-100 text-gray-400 border-gray-300'
                  : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'
              }`}
            >
              Previous
            </button>
            <button
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={currentPage === totalPages}
              className={`px-3 py-1 rounded-md border ${
                currentPage === totalPages
                  ? 'bg-gray-100 text-gray-400 border-gray-300'
                  : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'
              }`}
            >
              Next
            </button>
          </div>
          <div className="order-1 sm:order-none flex items-center gap-1">
            {getPageNumbers().map((pageNum) => (
              <button
                key={pageNum}
                onClick={() => handlePageChange(pageNum)}
                className={`px-3 py-1 rounded-md border ${
                  currentPage === pageNum
                    ? 'bg-gray-900 text-white border-gray-900'
                    : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'
                }`}
              >
                {pageNum}
              </button>
            ))}
          </div>
          <div className="hidden sm:block">
            <button
              onClick={() => handlePageChange(totalPages)}
              disabled={currentPage === totalPages}
              className={`px-3 py-1 rounded-md border ${
                currentPage === totalPages
                  ? 'bg-gray-100 text-gray-400 border-gray-300'
                  : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'
              }`}
            >
              Last
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
