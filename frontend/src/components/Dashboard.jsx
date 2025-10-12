import styles from './Dashboard.module.css';
import StatCard from './StatCard';

function Dashboard({ stats }) {
  const { personal_stats, library_wide_stats } = stats;

  return (
    <section className={styles.dashboardContainer}>
      <h2 className={styles.welcomeHeader}>
        Welcome, {personal_stats.user_profile.name}!
      </h2>
      
      <div className={styles.statsGrid}>
        <StatCard 
          title="Books You've Read" 
          value={personal_stats.total_books_read} 
        />
        <StatCard 
          title="Top Author" 
          value={library_wide_stats.most_popular_author.name}
          subtext="(Star Library's No.1)"
        />
      </div>

      <div className={styles.favoritesSection}>
        <h3 className={styles.favoritesTitle}>Your Favorite Authors</h3>
        <ul className={styles.favoritesList}>
          {personal_stats.favorite_authors.map((author, index) => (
            <li key={author.id} className={styles.favoriteItem}>
              {index + 1}. {author.name}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

export default Dashboard;