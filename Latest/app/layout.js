import './globals.css';

export const metadata = {
  title: 'Delizioso Restaurant',
  description: 'Discover our delicious menu with the freshest ingredients',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}