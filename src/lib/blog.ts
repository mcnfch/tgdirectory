import 'server-only';
import { cache } from 'react';

export interface BlogPost {
  id: string;
  title: string;
  date: string;
  excerpt: string;
  content?: string;
}

const BLOG_POSTS: BlogPost[] = [
  {
    id: '1',
    title: 'Best Breakfast Spots in Chattanooga',
    date: '2025-02-19',
    excerpt: 'From downtown diners to upscale brunch locations, here are our top picks...',
    content: `
<p>Chattanooga's breakfast scene is booming with incredible options for early risers and brunch enthusiasts alike. Here are our top picks for the best breakfast spots in the Scenic City:</p>

<ol>
  <li>
    <a href="/listing/milk-honey--XLOd60" class="text-blue-600 hover:text-blue-800">Milk & Honey</a>
    <p>Located in the North Shore, Milk & Honey offers an amazing selection of fresh pastries, artisanal coffee, and hearty breakfast plates. Their homemade biscuits are a must-try!</p>
  </li>

  <li>
    <a href="/listing/bluegrass-grill--Azv1Hw" class="text-blue-600 hover:text-blue-800">Bluegrass Grill</a>
    <p>This cozy spot in downtown Chattanooga is famous for their hearty Southern-style breakfasts. Their homemade biscuits and gravy are a local favorite, and the friendly atmosphere makes it worth the wait!</p>
  </li>

  <li>
    <a href="/listing/frothy-monkey--ZdjkCo" class="text-blue-600 hover:text-blue-800">Frothy Monkey</a>
    <p>A newcomer to the Chattanooga scene, Frothy Monkey has quickly become a local favorite for their excellent coffee and creative breakfast menu.</p>
  </li>
</ol>
<p>Stay tuned for more food adventures in Chattanooga!</p>`
  },
  {
    id: '2',
    title: 'Fine Dining Gems in Chattanooga',
    date: '2025-02-18',
    excerpt: 'Discover the most elegant and sophisticated dining experiences that Chattanooga has to offer...',
    content: `
<p>Chattanooga's fine dining scene offers an impressive array of sophisticated restaurants that combine exceptional cuisine with elegant atmospheres. Here are some must-visit establishments for your next special occasion:</p>

<ol>
  <li>
    <a href="/listing/bridgeman-s-chophouse--7vt2AE" class="text-blue-600 hover:text-blue-800">Bridgeman's Chophouse</a>
    <p>Located in the Read House Hotel, Bridgeman's Chophouse offers an upscale steakhouse experience with impeccable service. Their premium cuts of beef and extensive wine list make it perfect for special occasions.</p>
  </li>

  <li>
    <a href="/listing/calliope-restaurant-bar--Emezx0" class="text-blue-600 hover:text-blue-800">Calliope Restaurant & Bar</a>
    <p>A modern American restaurant that showcases local ingredients with creative flair. Their seasonal menu and craft cocktails have made them a standout in the downtown dining scene.</p>
  </li>

  <li>
    <a href="/listing/main-street-meats--EysUls" class="text-blue-600 hover:text-blue-800">Main Street Meats</a>
    <p>While more casual than traditional fine dining, Main Street Meats has earned its place among Chattanooga's best restaurants with its exceptional butcher program and sophisticated take on casual dining.</p>
  </li>
</ol>

<p>Make sure to make reservations in advance, as these popular establishments often book up quickly, especially on weekends!</p>`
  },
  {
    id: '3',
    title: 'Best Italian Restaurants in Chattanooga',
    date: '2025-02-20',
    excerpt: 'From rustic pasta to wood-fired pizzas, discover the finest Italian cuisine in the Scenic City...',
    content: `
<p>Craving authentic Italian cuisine? Chattanooga offers several outstanding Italian restaurants that bring the flavors of Italy to the Southeast. Here are our top picks for an exceptional Italian dining experience:</p>

<ol>
  <li>
    <a href="/listing/alleia--9AAJCI" class="text-blue-600 hover:text-blue-800">Alleia</a>
    <p>Located in a beautifully restored vintage brick building, Alleia is a cornerstone of Chattanooga's fine dining scene. Chef Daniel Lindley's rustic Italian cuisine features handmade pasta, wood-fired pizzas, and an exceptional wine list. The artfully modern interior creates the perfect ambiance for a romantic dinner or special occasion.</p>
  </li>

  <li>
    <a href="/listing/boccaccia-restaurant--gCZig0" class="text-blue-600 hover:text-blue-800">Boccaccia Restaurant</a>
    <p>This hidden gem offers an authentic Italian dining experience with a warm, intimate atmosphere. Their menu features traditional Italian dishes made from family recipes, complemented by an carefully curated wine selection. Don't miss their homemade tiramisu!</p>
  </li>
</ol>

<p>Pro tip: Italian restaurants are popular date night spots in Chattanooga, so we recommend making reservations, especially for weekend dining.</p>`
  }
];

export const getBlogPosts = cache(async () => {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 100));
  return BLOG_POSTS;
});

export const getBlogPost = cache(async (id: string) => {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 100));
  return BLOG_POSTS.find(p => p.id === id);
});
