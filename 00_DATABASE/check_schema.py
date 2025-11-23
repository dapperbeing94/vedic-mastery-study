import sqlite3

conn = sqlite3.connect('/home/ubuntu/vedic-mastery-study/00_DATABASE/vedic_knowledge.db')
cursor = conn.cursor()

for table in ['concepts', 'verses', 'study_progress']:
    print(f'\n{table}:')
    cursor.execute(f'PRAGMA table_info({table})')
    for row in cursor.fetchall():
        print(row)

conn.close()
