from db_connection import connect_db  # Ensure this matches your actual function name

class Concert:
    def __init__(self, id, hometown="", city="", band_name=""):
        self.id = id
        self.hometown = hometown
        self.city = city
        self.band_name = band_name

    def band(self):
        conn = connect_db()
        if conn is not None:
            cur = conn.cursor()
            cur.execute('''
                SELECT b.name 
                FROM concerts c
                INNER JOIN bands b ON c.band_name = b.name
                WHERE c.concert_id = ?
            ''', (self.id,))
            band = cur.fetchone()
            cur.close()
            conn.close()
            return band[0] if band else None
        else:
            return None

    def venue(self):
        conn = connect_db()
        if conn is not None:
            cur = conn.cursor()
            cur.execute('''
                SELECT v.title 
                FROM concerts c
                INNER JOIN venues v ON c.venue_title = v.title
                WHERE c.concert_id = ?
            ''', (self.id,))
            venue = cur.fetchone()
            cur.close()
            conn.close()
            return venue[0] if venue else None
        else:
            return None

    def hometown_show(self):
        conn = connect_db()
        if conn is not None:
            cur = conn.cursor()
            cur.execute('''
                SELECT b.hometown,
                       v.city,
                       b.name            
                FROM concerts c
                INNER JOIN bands b ON c.band_name = b.name
                INNER JOIN venues v ON c.venue_title = v.title
                WHERE c.concert_id = ?
            ''', (self.id,))
            result = cur.fetchone()
            cur.close()
            conn.close()
            if result:
                self.hometown, self.city, self.band_name = result
                return self.hometown == self.city
            return None

    def introduction(self):
        return f"Hello {self.city}!!!!! We are {self.band_name} and we're from {self.hometown}"

    def most_performances(self):
        conn = connect_db()
        if conn is not None:
            cur = conn.cursor()
            cur.execute('''
                SELECT COUNT(*) as total
                FROM concerts
                WHERE band_name = ?
            ''', (self.band_name,))
            most_performances = cur.fetchone()
            cur.close()
            conn.close()
            return most_performances[0] if most_performances else 0
        else:
            return 0

# Example usage:
first_concert = Concert(1)
print(f"The band for concert {first_concert.id} is {first_concert.band()}")
print(f"The venue for concert {first_concert.id} is {first_concert.venue()}")
print(f"Hometown show: {first_concert.hometown_show()}")
print(f"Introduction: {first_concert.introduction()}")
print(f"Most performances: {first_concert.most_performances()}")
