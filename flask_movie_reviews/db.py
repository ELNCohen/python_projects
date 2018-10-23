import sqlite3
import os

if os.path.exists('review.sqlite'):
    os.remove('review.sqlite')

conn = sqlite3.connect('review.sqlite')
c = conn.cursor()
c.execute("""
CREATE TABLE review_db
(
review TEXT,
sentiment INTEGER,
date TEXT
)
""")

example1 = 'I love this movie'
c.execute("""
INSERT INTO review_db
(review, sentiment, date) values
(?, ?, DATETIME('now'))
""", (example1, 1))

example2 = 'I disliked this movie'
c.execute("""
INSERT INTO review_db
(review, sentiment, date) values
(?, ?, DATETIME('now'))
""", (example2, 0))

conn.commit()
conn.close()


conn = sqlite3.connect('review.sqlite')
c = conn.cursor()
c.execute("""
select * from review_db where date between '2017-01-01' and DATETIME('now')
""")
results = c.fetchall()
conn.close()
print(results)
