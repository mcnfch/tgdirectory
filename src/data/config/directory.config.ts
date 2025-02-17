export interface DirectoryConfig {
  title: string;
  description: string;
  categories: string[];
  featuredListings: number;
  itemsPerPage: number;
}

export const directoryConfig: DirectoryConfig = {
  title: "Business Directory",
  description: "A comprehensive listing of local businesses and services",
  categories: [
    "Restaurants",
    "Retail",
    "Services",
    "Healthcare",
    "Entertainment"
  ],
  featuredListings: 6,
  itemsPerPage: 12
};
