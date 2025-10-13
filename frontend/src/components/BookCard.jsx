// Reusable: for displaying info of a book in a list

import styles from './BookCard.module.css';

function BookCard({ book, rank }) {
  return (
    <div className={styles.listItem}>
      <span className={styles.rank}>{rank}.</span>
      <div className={styles.bookInfo}>
        <h3 className={styles.title}>{book.title}</h3>
        <p className={styles.author}>by {book.author.name}</p>
      </div>
    </div>
  );
}

export default BookCard;