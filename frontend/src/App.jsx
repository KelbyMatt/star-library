import styles from './App.module.css';
import Dashboard from './components/Dashboard';
import BookList from './components/BookList';

function App() {
  // --- Placeholder Data ---
  const dashboardStats = {
    library_wide_stats: {
      most_popular_author: { id: 1, name: "Akira Toriyama" }
    },
    personal_stats: {
      user_profile: { id: 1, name: "James Bernhardt" },
      total_books_read: 9,
      favorite_authors: [
        { id: 1, name: "Akira Toriyama" },
        { id: 3, name: "Yuji Kaku" },
        { id: 2, name: "Masashi Kishimoto" }
      ]
    }
  };

  const popularBooks = [
    { id: 2, title: "Dragon Ball Z", author: { id: 1, name: "Akira Toriyama" } },
    { id: 5, title: "Naruto", author: { id: 2, name: "Masashi Kishimoto" } },
    { id: 1, title: "Dragon Ball", author: { id: 1, name: "Akira Toriyama" } },
    { id: 13, title: "Black Clover", author: { id: 4, name: "Yuki Tabata" } },
  ];

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