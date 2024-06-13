import sqlite3


class DatabaseManager:
    def __init__(self, db_path='english_bot.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()


class ExerciseManager(DatabaseManager):
    def __init__(self, db_path='english_bot.db'):
        super().__init__(db_path)

    def init_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS grammar_exercises (
                id INTEGER PRIMARY KEY,
                russian TEXT,
                english TEXT,
                level INTEGER
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS irregular_verbs (
                id INTEGER PRIMARY KEY,
                russian TEXT,
                english TEXT,
                level INTEGER
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS new_words (
                id INTEGER PRIMARY KEY,
                russian TEXT,
                english TEXT,
                level INTEGER
            )
        ''')
        self.conn.commit()

    def add_grammar_exercise(self, russian, english, level):
        self.cursor.execute('INSERT INTO grammar_exercises (russian, english, level) VALUES (?, ?, ?)',
                            (russian, english, level))
        self.conn.commit()

    def add_irregular_verb(self, russian, english, level):
        self.cursor.execute('INSERT INTO irregular_verbs (russian, english, level) VALUES (?, ?, ?)',
                            (russian, english, level))
        self.conn.commit()

    def add_new_word(self, russian, english, level):
        self.cursor.execute('INSERT INTO new_words (russian, english, level) VALUES (?, ?, ?)',
                            (russian, english, level))
        self.conn.commit()

    def get_grammar_exercises(self):
        self.cursor.execute('SELECT id, russian, english FROM grammar_exercises')
        rows = self.cursor.fetchall()
        return rows

    def get_irregular_verbs(self):
        self.cursor.execute('SELECT id, russian, english FROM irregular_verbs')
        rows = self.cursor.fetchall()
        return rows

    def get_new_words(self):
        self.cursor.execute('SELECT id, russian, english FROM new_words')
        rows = self.cursor.fetchall()
        return rows


class UserProgressManager(DatabaseManager):
    def __init__(self, db_path='english_bot.db'):
        super().__init__(db_path)

    def init_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_progress (
                user_id INTEGER,
                exercise_type TEXT,
                exercise_id INTEGER,
                PRIMARY KEY (user_id, exercise_type, exercise_id)
            )
        ''')
        self.conn.commit()

    def mark_exercise_completed(self, user_id, exercise_type, exercise_id):
        self.cursor.execute('INSERT INTO user_progress (user_id, exercise_type, exercise_id) VALUES (?, ?, ?)',
                            (user_id, exercise_type, exercise_id))
        self.conn.commit()

    def get_completed_exercises(self, user_id, exercise_type):
        self.cursor.execute('SELECT exercise_id FROM user_progress WHERE user_id = ? AND exercise_type = ?',
                            (user_id, exercise_type))
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]
