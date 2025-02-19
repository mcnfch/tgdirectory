# Touch Grass Directory Template

A modern, responsive directory of Chattanooga's restaurants built with Next.js and TypeScript.

## Features

- 🍽️ Comprehensive restaurant listings with real-time open/closed status
- 🔍 Advanced filtering by categories, regions, and amenities
- 📱 Responsive design with grid and list views
- ⭐ Rating and review count display
- 🕒 Dynamic business hours display
- 🎨 High-contrast, accessible UI following WCAG 2.1 AA standards

## Tech Stack

- Next.js 14
- TypeScript
- Tailwind CSS
- Font Awesome Icons
- Date-fns for time handling

## Local Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

The development server will start at http://localhost:3005

## Environment Variables

Create a `.env` file with:

```
NEXT_PUBLIC_NAME="Nooga Bites"
NEXT_PUBLIC_TAGLINE="Discover Chattanooga's Best Eats – One Bite at a Time!"
```

## Project Structure

```
src/
├── app/                 # Next.js app directory
├── components/         
│   ├── Header/         # Site header component
│   └── DirectoryListing/# Main directory components
├── data/
│   ├── config/         # Directory configuration
│   ├── media/          # Restaurant images
│   └── static/         # Static data files
├── types/              # TypeScript interfaces
└── utils/              # Utility functions
```

## Key Components

- `DirectoryList`: Main listing component with grid/list views and pagination
- `FilterPane`: Advanced filtering interface with categories and search
- `Header`: Site header with branding and navigation

## Accessibility

The project follows WCAG 2.1 AA standards with:
- High contrast text (minimum 4.5:1 ratio)
- Keyboard navigation support
- Semantic HTML structure
- Clear visual feedback for interactive elements

## License

MIT
