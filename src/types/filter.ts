export interface FilterOption {
  id: string;
  label: string;
  count: number;
}

export interface SelectedFilters {
  categories: Set<string>;
  districts: Set<string>;
  priceRanges: Set<string>;
  features: Set<string>;
}

export type FilterType = keyof SelectedFilters;
