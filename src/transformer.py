import argparse

from .raw_dao import RawSQLiteDAO
from .dao import SQLiteDAO


class Transformer:
    def __init__(self, raw_dao, dao):
        self._raw_dao = raw_dao
        self._dao = dao

    def transform(self, school_year):
        raise NotImplementedError('subclass should implement this method')


class StudentsByGenderTransformer(Transformer):
    def __init__(self, raw_dao, dao):
        super().__init__(raw_dao, dao)

    def transform(self, school_year):
        try:
            this_year = self._raw_dao.select_students_by_gender(school_year)
        except KeyError:
            print(f'nothing to transform for school_year={school_year}')
            return

        try:
            prev_year = self._raw_dao.select_students_by_gender(
                school_year - 1)
        except KeyError:
            total_growth = male_growth = female_growth = None
        else:
            total_growth = (
                this_year['total'] - prev_year['total']) / prev_year['total'] * 100
            male_growth = (
                this_year['male'] - prev_year['male']) / prev_year['male'] * 100
            female_growth = (
                this_year['female'] - prev_year['female']) / prev_year['female'] * 100

        data = (
            school_year,
            this_year['total'],
            total_growth,
            this_year['male'],
            male_growth,
            this_year['female'],
            female_growth
        )
        self._dao.insert_students_by_gender(data)


class GraduatesByDegreeTransformer(Transformer):
    def __init__(self, raw_dao, dao):
        super().__init__(raw_dao, dao)

    def transform(self, school_year):
        try:
            this_year = self._raw_dao.select_graduates(school_year)
        except KeyError:
            print(f'nothing to transform for school_year={school_year}')
            return

        data = (
            school_year,
            this_year['total'],
            this_year['associate'],
            this_year['bachelor'],
            this_year['master'],
            this_year['doctoral'],
        )
        self._dao.insert_graduates_by_degree(data)


TRANSFORMERS = {
    'students_by_gender': StudentsByGenderTransformer,
    'graduates_by_degree': GraduatesByDegreeTransformer
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, help='year to be processed')
    args = parser.parse_args()

    school_year = args.year

    dao_raw = RawSQLiteDAO()
    dao_raw.connect(db_path='raw.db')

    dao_data = SQLiteDAO()
    dao_data.connect(db_path='data.db')
    dao_data.init()

    for _, TRANSFORMER_CLASS in TRANSFORMERS.items():
        transformer = TRANSFORMER_CLASS(dao_raw, dao_data)
        transformer.transform(school_year)
