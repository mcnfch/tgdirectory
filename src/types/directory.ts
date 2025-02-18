export interface DirectoryItem {
  id: string;
  title: string;
  slug: string;
  image: string;
  address: string;
  featured: boolean;
  rating: number;
  reviewCount: number;
  website: string;
  categories: string[];
  districts: string[];
  features: string[];
  priceLevel: number;
  hours: any;
  service_options?: {
    dine_in: boolean;
    takeout: boolean;
    delivery: boolean;
    curbside_pickup: boolean;
    reservations: boolean;
    outdoor_seating: boolean;
  };
  accessibility?: {
    wheelchair_accessible_parking: boolean;
    wheelchair_accessible_entrance: boolean;
    wheelchair_accessible_restroom: boolean;
    wheelchair_accessible_seating: boolean;
  };
  amenities?: {
    restroom: boolean;
    good_for_groups: boolean;
    good_for_watching_sports: boolean;
    live_music?: boolean;
    happy_hour?: boolean;
  };
  basic_info?: {
    name: string;
    id: string;
    types: string[];
    primary_type: string;
    phone: {
      local: string;
      international: string;
    };
    website: string;
    rating: number;
    rating_count: number;
    description: string;
    district: string;
    district_description: string;
    coordinates: number[];
    price_level?: {
      value: string;
      numeric: number;
    };
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
