from app.database import SessionLocal
from app import models, schemas

def seed_data():
    db = SessionLocal()

    try:
        if db.query(models.Author).count() > 0:
            print("Skipping seeding as data already exists")
            return
        print("Seeding the database with initial data")

        author1 = models.Author(name="Akira Toriyama")
        author2 = models.Author(name="Masashi Kishimoto")
        author3 = models.Author(name="Yuji Kaku")
        author4 = models.Author(name="Yuki Tabata")

        db.add_all([author1, author2, author3, author4])
        db.commit()
        print("Authors Created")


        books_to_add = [
            models.Book(title="Dragon Ball", author_id=author1.id),
            models.Book(title="Dragon Ball Z", author_id=author1.id),
            models.Book(title="Dragon Ball Super", author_id=author1.id),
            models.Book(title="Sand Land", author_id=author1.id),
            models.Book(title="Naruto", author_id=author2.id),
            models.Book(title="Naruto Shippuden", author_id=author2.id),
            models.Book(title="Boruto: Naruto Next Generations", author_id=author2.id),
            models.Book(title="Boruto: Two Blue Vortex", author_id=author2.id),
            models.Book(title="Samurai 8: The Tale of Hachimaru", author_id=author2.id),
            models.Book(title="Hell's Paradise", author_id=author3.id),
            models.Book(title="Evil Heart", author_id=author3.id),
            models.Book(title="Fantasma", author_id=author3.id),
            models.Book(title="Black Clover", author_id=author4.id),
            models.Book(title="Black Clover Gaiden: Quartet Knights", author_id=author4.id),
            models.Book(title="Hungry Joker", author_id=author4.id),
        ]

        db.add_all(books_to_add)
        db.commit()
        print("Books Created")


        reader1 = models.Reader(name="James Bernhardt")
        reader2 = models.Reader(name="Kelby Matthew")
        reader3 = models.Reader(name="Thierry Henry")
        reader4 = models.Reader(name="Arsene Wenger")
        reader5 = models.Reader(name="John Frusciante")

        db.add_all([reader1, reader2, reader3, reader4, reader5])
        db.commit()
        print("Readers Created")

        all_books = db.query(models.Book).all()

        dragon_ball_z_book = all_books[1]
        toriyama_books = all_books[0:4]
        kishimoto_books = all_books[4:9]
        kaku_books = all_books[9:12]
        tabata_books = all_books[12:15]


        reader2.read_books.append(dragon_ball_z_book)
        reader3.read_books.append(dragon_ball_z_book)
        reader4.read_books.append(dragon_ball_z_book)
        reader5.read_books.append(dragon_ball_z_book)

        reader1.read_books.extend(toriyama_books)
        reader1.read_books.extend(kaku_books)
        reader1.read_books.append(all_books[4])
        reader1.read_books.append(all_books[12])
        
        reader2.read_books.extend(kishimoto_books)
        reader2.read_books.extend(all_books[12:14])
        
        reader3.read_books.append(all_books[0])
        reader4.read_books.append(all_books[2])

        db.commit()
        print("Relationships Created")
        print("\nData Seeding Completed")

    finally:
        db.close()

if __name__ == "__main__":
    seed_data()      