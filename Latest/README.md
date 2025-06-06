# Restaurant Menu Page - Next.js Project

This is a beautiful and interactive restaurant menu page built with Next.js and Tailwind CSS.

## Features

- 🎨 Beautiful and modern UI design
- 🔍 Search functionality for menu items
- 🏷️ Category filtering
- ❤️ Favorites system
- 🛒 Shopping cart functionality
- 📱 Fully responsive design
- ✨ Interactive animations with Framer Motion

## No-npx Setup Guide

Since you're having issues with npx, here's a complete setup guide using only npm commands:

### Step 1: Clone or Download the Project

Download this project to your local machine.

### Step 2: Install Dependencies

Navigate to the project directory and run:

```bash
npm install
```

This will install all the required dependencies from package.json.

### Step 3: Set Up Tailwind CSS

Run the setup script to create the necessary configuration files:

```bash
npm run setup-tailwind
```

This script will create:
- tailwind.config.js
- postcss.config.js
- jsconfig.json
- Required directories

### Step 4: Start the Development Server

```bash
npm run dev
```

Visit http://localhost:3000 in your browser to see your restaurant menu page!

## Project Structure

```
restaurant-app/
├── app/
│   ├── globals.css     # Global CSS styles with Tailwind
│   ├── layout.js       # Root layout for the app
│   └── page.js         # Main page that imports the RestaurantPage component
├── components/
│   └── RestaurantPage.js # The restaurant page component
├── package.json        # Project dependencies
├── jsconfig.json       # Path aliases configuration
├── tailwind.config.js  # Tailwind CSS configuration
├── postcss.config.js   # PostCSS configuration
├── next.config.js