from db_connection import connect_db  

class Venue:
    def __init__(self, id):
        self.id = id
    
    def bands(self):
        conn = connect_db()
        if conn is not None:
            cur = conn.cursor()
            cur.execute('''
                SELECT b.name, 
                       b.hometown 
                FROM concerts c
                INNER JOIN bands b ON c.band_name = b.name
                WHERE c.venue_title = ?
            ''', (self.id,))
            bands = cur.fetchall()
            cur.close()
            conn.close()
            return bands
        else:
            return []

    def concerts(self):
        conn = connect_db()
        if conn is not None:
            cur = conn.cursor()
            cur.execute('''
                SELECT c.date, 
                       b.name 
                FROM concerts c
                INNER JOIN bands b ON c.band_name = b.name
                WHERE c.venue_title = ?
            ''', (self.id,))
            concerts = cur.fetchall()
            cur.close()
            conn.close()
            return concerts
        else:
            return []

    def concert_on(self, date):
        conn = connect_db()
        if conn is not None:
            cur = conn.cursor()
            cur.execute('''
                SELECT c.date, 
                       c.band_name 
                FROM concerts c
                WHERE c.venue_title = ? AND c.date = ?
            ''', (self.id, date))
            concert = cur.fetchone()
            cur.close()
            conn.close()
            return concert if concert else None
        else:
            return None

    def most_frequent_band(self):
        conn = connect_db()
        if conn is not None:
            cur = conn.cursor()
            cur.execute('''
                SELECT c.band_name, 
                       COUNT(*) as total
                FROM concerts c
                WHERE c.venue_title = ?
                GROUP BY c.band_name
                ORDER BY total DESC
                LIMIT 1
            ''', (self.id,))
            most_frequent_band = cur.fetchone()
            cur.close()
            conn.close()
            return most_frequent_band[0] if most_frequent_band else None
        else:
            return None


first_venue = Venue('Stadium')
print(f"Bands at venue: {first_venue.bands()}")
print(f"Concerts at venue: {first_venue.concerts()}")
print(f"First concert on 2024-10-01: {first_venue.concert_on('2024-10-01')}")
print(f"Most frequent band: {first_venue.most_frequent_band()}")
