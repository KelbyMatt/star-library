//Displays the Most Popular Book Rankings.

import styles from './BookList.module.css';
import BookCard from './BookCard';

function BookList({ books }) {
  return (
    <section>
      <h2 className={styles.listHeader}>Top 10 Most Popular Books</h2>
      <ul className={styles.bookList}>
        {books?.map((book, index) => (
        
          <li key={book.id}>
            <BookCard book={book} rank={index + 1} />
          </li>
        ))}
      </ul>
    </section>
  );
}

export default BookList;