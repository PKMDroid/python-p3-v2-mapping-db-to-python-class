from __init__ import CURSOR, CONN


class Department:
    all = {}

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT
            );
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS departments;"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO departments (name, location)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, location):
        dept = cls(name, location)
        dept.save()
        return dept

    def update(self):
        sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        sql = "DELETE FROM departments WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        dept = cls.all.get(row[0])
        if dept:
            dept.name = row[1]
            dept.location = row[2]
        else:
            dept = cls(row[1], row[2], row[0])
            cls.all[dept.id] = dept
        return dept

    @classmethod
    def get_all(cls):
        rows = CURSOR.execute("SELECT * FROM departments").fetchall()
        return [cls.instance_from_db(r) for r in rows]

    @classmethod
    def find_by_id(cls, id):
        row = CURSOR.execute(
            "SELECT * FROM departments WHERE id = ?", 
            (id,)
        ).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        row = CURSOR.execute(
            "SELECT * FROM departments WHERE name IS ?", 
            (name,)
        ).fetchone()
        return cls.instance_from_db(row) if row else None
