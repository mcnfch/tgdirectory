import { DirectoryItem, FilterOption } from '@/types/directory';

export interface SelectedFilters {
  categories: Set<string>;
  districts: Set<string>;
  priceRanges: Set<string>;
  features: Set<string>;
}

export const getFilterOptions = (items: DirectoryItem[], field: keyof DirectoryItem): FilterOption[] => {
  const counts = new Map<string, number>();
  
  items.forEach(item => {
    const value = item[field];
    if (Array.isArray(value)) {
      value.forEach(v => {
        counts.set(v, (counts.get(v) || 0) + 1);
      });
    } else if (typeof value === 'string') {
      counts.set(value, (counts.get(value) || 0) + 1);
    }
  });

  return Array.from(counts.entries()).map(([id, count]) => ({
    id,
    label: id,
    count
  }));
};
