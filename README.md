# Touch Grass Directory Template

A modern, responsive directory template built with Next.js and TypeScript. Originally created for Chattanooga's restaurants, this template can be customized for any location-based directory.

## Features

- 🍽️ Comprehensive listing system with real-time open/closed status
- 🔍 Advanced filtering by categories, regions, and custom attributes
- 📱 Responsive design with grid and list views
- ⭐ Rating and review count display
- 🕒 Dynamic business hours display
- 🎨 High-contrast, accessible UI following WCAG 2.1 AA standards
- 🖼️ Automated image optimization for fast loading
- 🗺️ Built-in district/region mapping support

## Tech Stack

- Next.js 14
- TypeScript
- Tailwind CSS
- Font Awesome Icons
- Date-fns for time handling
- Sharp for image optimization

## Prerequisites

- Node.js >= 18.17
- npm >= 9.0.0

## Local Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm run start
```

The development server will start at http://localhost:3005

## Environment Variables

Create a `.env` file with:

```
NEXT_PUBLIC_NAME="Your Directory Name"
NEXT_PUBLIC_TAGLINE="Your Custom Tagline"
NEXT_PUBLIC_DEFAULT_DISTRICT="default"  # Optional: Set default district filter
NEXT_PUBLIC_DEFAULT_CATEGORY="all"      # Optional: Set default category filter
```

## Project Structure

```
src/
├── app/                 # Next.js app directory
├── components/         
│   ├── Header/         # Site header component
│   ├── DirectoryListing/# Main directory components
│   ├── AddressLink/    # Address display and mapping
│   ├── ImageSlider/    # Image gallery component
│   ├── OpeningHours/   # Business hours display
│   └── SchemaMarkup/   # SEO schema markup
├── data/
│   ├── config/         # Directory configuration
│   ├── media/          # Listing images
│   └── static/         # Static data files
├── types/              # TypeScript interfaces
└── utils/              # Utility functions
```

## Key Components

- `DirectoryList`: Main listing component with grid/list views and pagination
- `FilterPane`: Advanced filtering interface with categories and search
- `Header`: Site header with branding and navigation
- `ImageSlider`: Responsive image gallery with lazy loading
- `OpeningHours`: Business hours display with timezone support

## Accessibility

The project follows WCAG 2.1 AA standards with:
- High contrast text (minimum 4.5:1 ratio)
- Keyboard navigation support
- Semantic HTML structure
- Clear visual feedback for interactive elements
- ARIA labels and roles
- Screen reader optimizations

## Deployment

The project is optimized for deployment on Vercel or similar platforms:

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy to Vercel
vercel
```

For other platforms, build the project with:
```bash
npm run build
```

The built project will be in the `.next` directory.

## License

MIT
