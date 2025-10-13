import { useState, useEffect } from 'react';
import styles from './App.module.css';
import Dashboard from './components/Dashboard';
import BookList from './components/BookList';

function App() {
  const [dashboardStats, setDashboardStats] = useState({
    library_wide_stats: { most_popular_author: null },
    personal_stats: {
      user_profile: { name: "..." },
      total_books_read: 0,
      favorite_authors: []
    }
  });

  const [popularBooks, setPopularBooks] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);


  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsResponse, booksResponse] = await Promise.all([
          fetch('/api/dashboard/stats'),
          fetch('/api/books/popular')
        ]);
        if (!statsResponse.ok || !booksResponse.ok) {
          throw new Error('Network response was not ok');
        }

        const statsData = await statsResponse.json();
        const booksData = await booksResponse.json();

        setDashboardStats(statsData);
        setPopularBooks(booksData);
      } catch (error) {
        console.error("Failed to fetch data:", error);
        setError("Could not connect to the library. Please try again.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);


  if (isLoading) {
    return <div className={styles.centeredMessage}>Loading Library...</div>;
  }

  if (error) {
    return <div className={styles.centeredMessageError}>{error}</div>;
  }

return (
    <div>
      <header className={styles.header}>
        <h1 className={styles.headerTitle}>STAR Library</h1>
      </header>
      <main className={styles.mainContent}>
        <div className={styles.dashboardColumn}>
          <Dashboard stats={dashboardStats} />
        </div>
        <div className={styles.bookListColumn}>
          <BookList books={popularBooks} />
        </div>
      </main>
    </div>
  );
}

export default App