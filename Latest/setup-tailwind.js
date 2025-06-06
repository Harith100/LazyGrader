const fs = require('fs');
const path = require('path');

// Create tailwind.config.js file
const tailwindConfig = `/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        'red': {
          50: '#fef2f2',
          100: '#fee2e2',
          200: '#fecaca',
          300: '#fca5a5',
          400: '#f87171',
          500: '#ef4444',
          600: '#dc2626',
          700: '#b91c1c',
          800: '#991b1b',
          900: '#7f1d1d',
        },
      },
    },
  },
  plugins: [],
}`;

// Create postcss.config.js file
const postcssConfig = `module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}`;

// Create jsconfig.json file
const jsconfigContent = `{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  }
}`;

// Create or check directories
const directories = ['app', 'components'];
directories.forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir);
    console.log(`Created directory: ${dir}`);
  }
});

// Write files
fs.writeFileSync('tailwind.config.js', tailwindConfig);
console.log('Created tailwind.config.js');

fs.writeFileSync('postcss.config.js', postcssConfig);
console.log('Created postcss.config.js');

fs.writeFileSync('jsconfig.json', jsconfigContent);
console.log('Created jsconfig.json');

// Create globals.css
const globalsCss = `@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom scrollbar styling */
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}

.hide-scrollbar {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

/* Optional animation for menu cards */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Add smooth transitions */
* {
  transition-property: background-color, border-color, color, fill, stroke, opacity, box-shadow, transform;
  transition-duration: 300ms;
}

/* Custom hover effects for cards */
.menu-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}`;

// Create app/globals.css
fs.writeFileSync(path.join('app', 'globals.css'), globalsCss);
console.log('Created app/globals.css');

// Create Next.js config file
const nextConfig = `/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
}

module.exports = nextConfig`;

fs.writeFileSync('next.config.js', nextConfig);
console.log('Created next.config.js');

console.log('Setup complete! You can now run npm run dev to start your application.');