export interface DirectoryItem {
  id: string;
  title: string;
  slug: string;
  image: string;
  address: string;
  featured?: boolean;
  rating?: number;
  reviewCount?: number;
  website?: string;
  categories: string[];
  regions: string[];
  amenities: string[];
  hours?: {
    current_status: string;
    schedule: string[];
  };
}

export interface FilterOption {
  id: string;
  label: string;
  count: number;
}

export interface DirectoryFilters {
  categories: FilterOption[];
  regions: FilterOption[];
  amenities: FilterOption[];
}
