from band import Band
from concert import Concert
from venues import Venue
from db_connection import connect_db

def setup_sample_data():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO bands (name, hometown) VALUES (?, ?)", ("The Rockers", "Rockville"))
    cursor.execute("INSERT INTO venues (title, city) VALUES (?, ?)", ("Stadium", "Rockville"))
    cursor.execute("INSERT INTO concerts (band_name, venue_title, date) VALUES (?, ?, ?)", ("The Rockers", "Stadium", "2024-10-01"))

    conn.commit()
    conn.close()

def main():
    setup_sample_data()

    band = Band("The Rockers", "Rockville")
    venue = Venue("Stadium", "Rockville")
    concert = Concert(1, "The Rockers", "Stadium", "2024-10-01")

    print(concert.introduction())
    print("Hometown Show:", concert.hometown_show())
    print("Venue Concerts:", venue.concerts())
    print("Band Venues:", band.venues())
    print("All Introductions:", band.all_introductions())
    print("Most Performances:", band.most_performances())

if __name__ == "__main__":
    main()
