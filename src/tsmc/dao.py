import sqlite3
import mariadb

StudentsByGenderCOLUMNS = {
    'school_year': 0,
    'total': 1,
    'total_growth': 2,
    'male': 3,
    'male_growth': 4,
    'female': 5,
    'female_growth': 6,
}

GraduatesByDegreeCOLUMNS = {
    'school_year': 0,
    'total': 1,
    'associate': 2,
    'bachelor': 3,
    'master': 4,
    'doctoral': 5
}


class DataAccessObject:
    def connect(self, **kwargs):
        raise NotImplementedError('subclass should implement this method')

    def init(self):
        raise NotImplementedError('subclass should implement this method')

    def insert_students_by_gender(self, values):
        raise NotImplementedError('subclass should implement this method')

    def select_students_by_gender(self, start_year, end_year):
        raise NotImplementedError('subclass should implement this method')

    def insert_graduates_by_degree(self, values):
        raise NotImplementedError('subclass should implement this method')

    def select_graduates_by_degree(self, year):
        raise NotImplementedError('subclass should implement this method')


class SQLiteDAO(DataAccessObject):
    def __init__(self):
        self._db = None

    def connect(self, **kwargs):
        self._db = sqlite3.connect(kwargs['db_path'])

    def init(self):
        self._db.executescript(
            """
            CREATE TABLE IF NOT EXISTS students_by_gender (
                school_year INT,
                total INT,
                total_growth REAL,
                male INT,
                male_growth REAL,
                female INT,
                female_growth REAL
            );

            CREATE TABLE IF NOT EXISTS graduates_by_degree (
                school_year INT,
                total INT,
                associate INT,
                bachelor INT,
                master INT,
                doctoral INT
            );
            """
        )

    @staticmethod
    def _get_insert_cmd(table, columns):
        return """
            INSERT INTO {} ({})
            VALUES ({})
        """.format(table, ','.join(columns),
                   ','.join(['?'] * len(columns))
                   )

    @staticmethod
    def _get_select_cmd(table):
        return """
            SELECT * FROM {};
        """.format(table)

    def insert_students_by_gender(self, values):
        sql_cmd = self._get_insert_cmd('students_by_gender',
                                       list(StudentsByGenderCOLUMNS.keys()))
        self._db.execute(sql_cmd, values)
        self._db.commit()

    def select_students_by_gender(self, start_year, end_year):
        sql_cmd = """
            SELECT * FROM students_by_gender
            WHERE school_year >= ?
            AND school_year <= ?
            ORDER BY school_year;
        """
        rows = self._db.execute(sql_cmd, (start_year, end_year))
        ret = []
        for row in rows:
            ret.append({
                'school_year': row[StudentsByGenderCOLUMNS['school_year']],
                'total': row[StudentsByGenderCOLUMNS['total']],
                'total_growth': row[StudentsByGenderCOLUMNS['total_growth']],
                'male': row[StudentsByGenderCOLUMNS['male']],
                'male_growth': row[StudentsByGenderCOLUMNS['male_growth']],
                'female': row[StudentsByGenderCOLUMNS['female']],
                'female_growth': row[StudentsByGenderCOLUMNS['female_growth']],
            })
        return ret

    def insert_graduates_by_degree(self, values):
        sql_cmd = self._get_insert_cmd('graduates_by_degree',
                                       list(GraduatesByDegreeCOLUMNS.keys()))
        self._db.execute(sql_cmd, values)
        self._db.commit()

    def select_graduates_by_degree(self, year):
        sql_cmd = """
            SELECT * FROM graduates_by_degree
            WHERE school_year = ?;
        """
        res = self._db.execute(sql_cmd, (year,))
        row = res.fetchone()
        if row is None:
            raise KeyError(f'school_year={year} not exists')

        school_year, total, associate, bachelor, master, doctoral = row
        return {
            'total': total,
            'associate': associate,
            'bachelor': bachelor,
            'master': master,
            'doctoral': doctoral
        }


class MySQLDAO(DataAccessObject):
    def __init__(self):
        self._conn = None
        self._cursor = None

    def connect(self, **kwargs):
        self._conn = mariadb.connect(**kwargs)
        self._cursor = self._conn.cursor()

    def init(self):
        self._cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS students_by_gender (
                school_year INT,
                total INT,
                total_growth REAL,
                male INT,
                male_growth REAL,
                female INT,
                female_growth REAL
            );
        """
        )
        self._cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS graduates_by_degree (
                school_year INT,
                total INT,
                associate INT,
                bachelor INT,
                master INT,
                doctoral INT
            );
        """
        )


    @staticmethod
    def _get_insert_cmd(table, columns):
        return """
            INSERT INTO {} ({})
            VALUES ({})
        """.format(table, ','.join(columns),
                   ','.join(['?'] * len(columns))
                   )

    @staticmethod
    def _get_select_cmd(table):
        return """
            SELECT * FROM {};
        """.format(table)

    def insert_students_by_gender(self, values):
        sql_cmd = self._get_insert_cmd('students_by_gender',
                                       list(StudentsByGenderCOLUMNS.keys()))
        self._cursor.execute(sql_cmd, values)
        self._conn.commit()

    def select_students_by_gender(self, start_year, end_year):
        sql_cmd = """
            SELECT * FROM students_by_gender
            WHERE school_year >= ?
            AND school_year <= ?
            ORDER BY school_year;
        """
        rows = self._cursor.execute(sql_cmd, (start_year, end_year))
        ret = []
        for row in rows:
            ret.append({
                'school_year': row[StudentsByGenderCOLUMNS['school_year']],
                'total': row[StudentsByGenderCOLUMNS['total']],
                'total_growth': row[StudentsByGenderCOLUMNS['total_growth']],
                'male': row[StudentsByGenderCOLUMNS['male']],
                'male_growth': row[StudentsByGenderCOLUMNS['male_growth']],
                'female': row[StudentsByGenderCOLUMNS['female']],
                'female_growth': row[StudentsByGenderCOLUMNS['female_growth']],
            })
        return ret

    def insert_graduates_by_degree(self, values):
        sql_cmd = self._get_insert_cmd('graduates_by_degree',
                                       list(GraduatesByDegreeCOLUMNS.keys()))
        self._cursor.execute(sql_cmd, values)
        self._conn.commit()

    def select_graduates_by_degree(self, year):
        sql_cmd = """
            SELECT * FROM graduates_by_degree
            WHERE school_year = ?;
        """
        res = self._cursor.execute(sql_cmd, (year,))
        row = res.fetchone()
        if row is None:
            raise KeyError(f'school_year={year} not exists')

        school_year, total, associate, bachelor, master, doctoral = row
        return {
            'total': total,
            'associate': associate,
            'bachelor': bachelor,
            'master': master,
            'doctoral': doctoral
        }