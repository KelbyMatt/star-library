import styles from './StatCard.module.css';

function StatCard({ title, value, subtext }) {
  return (
    <div className={styles.card}>
      <h3 className={styles.title}>{title}</h3>
      <p className={styles.value}>{value}</p>
      {subtext && <p className={styles.subtext}>{subtext}</p>}
    </div>
  );
}

export default StatCard;