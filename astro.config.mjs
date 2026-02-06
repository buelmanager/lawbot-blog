import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://lawbot-blog.vercel.app',
  integrations: [sitemap()],
});
