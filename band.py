from db_connection import database_connect

class Band:
    def __init__(self, id):
        self.id = id

    def concerts(self):
        """Fetch all concerts for the band."""
        conn = database_connect()
        if conn is not None:
            try:
                with conn.cursor() as cur:
                    cur.execute('''
                        SELECT concert.concert_name, 
                               concert.date,
                               venue.title 
                        FROM concert
                        INNER JOIN band ON concert.band_id = band.band_id
                        INNER JOIN venue ON venue.venue_id = concert.venue_id
                        WHERE band.band_id = %s
                    ''', (self.id,))
                    concerts = cur.fetchall()
                    return concerts
            finally:
                conn.close()
        else:
            return []

    def venues(self):
        """Fetch all venues where the band has performed."""
        conn = database_connect()
        if conn is not None:
            try:
                with conn.cursor() as cur:
                    cur.execute('''
                        SELECT DISTINCT venue.city, 
                                        venue.title 
                        FROM concert
                        INNER JOIN band ON concert.band_id = band.band_id
                        INNER JOIN venue ON venue.venue_id = concert.venue_id
                        WHERE band.band_id = %s
                    ''', (self.id,))
                    venues = cur.fetchall()
                    return venues
            finally:
                conn.close()
        else:
            return []

    def play_in_venue(self, venue_id, date, concert_name):
        """Add a new concert for the band."""
        conn = database_connect()
        if conn is not None:
            try:
                with conn.cursor() as cur:
                    cur.execute('''
                        INSERT INTO concert (band_id, venue_id, date, concert_name)
                        VALUES (%s, %s, %s, %s)
                    ''', (self.id, venue_id, date, concert_name))
                    conn.commit()
                    return True
            except Exception as e:
                print(f"An error occurred: {e}")
                return False
            finally:
                conn.close()
        else:
            return False

    def all_introductions(self):
        """Generate an introduction message for the band at all their venues."""
        conn = database_connect()
        if conn is not None:
            try:
                with conn.cursor() as cur:
                    cur.execute('''
                        SELECT band.hometown,
                               venue.city,
                               band.name
                        FROM concert
                        INNER JOIN band ON concert.band_id = band.band_id
                        INNER JOIN venue ON venue.venue_id = concert.venue_id
                        WHERE band.band_id = %s
                    ''', (self.id,))
                    hometown = cur.fetchone()
                    if hometown:
                        return f"Hello {hometown[1]}!!!!! We are {hometown[2]} and we're from {hometown[0]}"
                    else:
                        return "No introductions available."
            finally:
                conn.close()
        else:
            return "Database connection failed."

