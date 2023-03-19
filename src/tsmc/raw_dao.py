import sqlite3
from .const import *

StudentsBySchoolGenderCOLUMNS = {
    'school_id': 0,
    'school_name': 1,
    'day_or_night': 2,
    'degree': 3,
    'total': 4,
    'male': 5,
    'female': 6,
    'male_1_year': 7,
    'female_1_year': 8,
    'male_2_year': 9,
    'female_2_year': 10,
    'male_3_year': 11,
    'female_3_year': 12,
    'male_4_year': 13,
    'female_4_year': 14,
    'male_5_year': 15,
    'female_5_year': 16,
    'male_6_year': 17,
    'female_6_year': 18,
    'male_7_year': 19,
    'female_7_year': 20,
    'male_extended': 21,
    'female_extended': 22,
    'city_name': 23,
    'school_system': 24
}

GraduatesBySchoolGenderCOLUMNS = {
    'school_id': 0,
    'school_name': 1,
    'day_or_night': 2,
    'degree': 3,
    'male': 4,
    'female': 5,
    'city_name': 6,
    'school_system': 7
}


class RawDataAccessObject:
    def connect(self, **kwargs):
        raise NotImplementedError('subclass should implement this method')

    def init(self):
        raise NotImplementedError('subclass should implement this method')

    def insert_students_by_school_gender(self, values):
        raise NotImplementedError('subclass should implement this method')

    def select_students_by_gender(self, school_year):
        raise NotImplementedError('subclass should implement this method')

    def insert_graduates_by_school_gender(self, values):
        raise NotImplementedError('subclass should implement this method')

    def select_graduates(self, school_year):
        raise NotImplementedError('subclass should implement this method')


class RawSQLiteDAO(RawDataAccessObject):
    def __init__(self):
        self._db = None

    def connect(self, **kwargs):
        self._db = sqlite3.connect(kwargs['db_path'], check_same_thread=False)

    def init(self):
        self._db.executescript(
            """
            CREATE TABLE IF NOT EXISTS students_by_school_gender (
                school_year INT,
                school_id INT,
                school_name TEXT,
                day_or_night TEXT,
                degree TEXT,
                total INT,
                male INT,
                female INT,
                male_1_year INT,
                female_1_year INT,
                male_2_year INT,
                female_2_year INT,
                male_3_year INT,
                female_3_year INT,
                male_4_year INT,
                female_4_year INT,
                male_5_year INT,
                female_5_year INT,
                male_6_year INT,
                female_6_year INT,
                male_7_year INT,
                female_7_year INT,
                male_extended INT,
                female_extended INT,
                city_name TEXT,
                school_system TEXT
            );

            CREATE TABLE IF NOT EXISTS graduates_by_school_gender (
                school_year INT,
                school_id INT,
                school_name TEXT,
                day_or_night TEXT,
                degree TEXT,
                male INT,
                female INT,
                city_name TEXT,
                school_system TEXT
            );
            """
        )

    def insert_students_by_school_gender(self, values):
        sql_cmd = self._get_insert_cmd(
            'students_by_school_gender',
            ['school_year'] +
            list(
                StudentsBySchoolGenderCOLUMNS.keys()))
        self._db.execute(sql_cmd, values)
        self._db.commit()

    @staticmethod
    def _get_insert_cmd(table, columns):
        return """
            INSERT INTO {} ({})
            VALUES ({})
        """.format(table, ','.join(columns),
                   ','.join(['?'] * len(columns))
                   )

    def select_students_by_gender(self, school_year):
        sql_cmd = """
            SELECT
                school_year,
                SUM("total"),
                SUM("male"),
                SUM("female")
            FROM
                students_by_school_gender
            WHERE
                school_year={};
        """.format(school_year)
        res = self._db.execute(sql_cmd)
        school_year, total, male, female = res.fetchone()
        if school_year is None:
            raise KeyError(f'school_year={school_year} not exists')

        return {
            'school_year': school_year,
            'total': total,
            'male': male,
            'female': female,
        }

    def insert_graduates_by_school_gender(self, values):
        sql_cmd = self._get_insert_cmd(
            'graduates_by_school_gender',
            ['school_year'] +
            list(
                GraduatesBySchoolGenderCOLUMNS.keys()))
        self._db.execute(sql_cmd, values)
        self._db.commit()

    def select_graduates(self, school_year):
        sql_cmd = """
            SELECT
                school_year,
                degree,
                SUM("male") + SUM("female")
            FROM
                graduates_by_school_gender
            WHERE
                school_year={}
            GROUP BY
                degree;
        """.format(school_year)
        res = self._db.execute(sql_cmd)
        rows = res.fetchall()
        if len(rows) == 0:
            raise KeyError(f'school_year={school_year} not exists')
        total = associate = master = doctoral = 0
        for row in rows:
            school_year, degree, degree_sum = row
            total += degree_sum
            associate += degree_sum if degree in (
                TWO_YEAR_COLLEGE, FIVE_YEAR_COLLEGE) else 0
            master += degree_sum if degree == MASTER else 0
            doctoral += degree_sum if degree == DOCTORAL else 0

        return {
            'school_year': school_year,
            'total': total,
            'associate': associate,
            'bachelor': total - associate - master - doctoral,
            'master': master,
            'doctoral': doctoral
        }
