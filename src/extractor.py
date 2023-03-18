import requests
import json
import csv
import tempfile
import argparse

from loader import LOADERS
from raw_dao import RawSQLiteDAO, StudentsBySchoolGenderCOLUMNS, \
    GraduatesBySchoolGenderCOLUMNS


def get_csv(url):
    resp = requests.get(url, timeout=10)
    if resp.status_code == 200:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(resp.content)
        return temp_file.name

    else:
        raise RuntimeError(f'Download {url} status code: {resp.status_code}')


class CSVExtractor:
    def extract(self, row):
        raise NotImplementedError('subclass should implement this method')

    @staticmethod
    def num_str_to_int(num_str):
        return 0 if num_str == '-' else int(num_str.replace(',', ''))


class StudentsBySchoolGenderExtractor(CSVExtractor):
    def extract(self, row):
        return [
            int(row[StudentsBySchoolGenderCOLUMNS['school_id']]),
            row[StudentsBySchoolGenderCOLUMNS['school_name']],
            row[StudentsBySchoolGenderCOLUMNS['day_or_night']],
            row[StudentsBySchoolGenderCOLUMNS['degree']],
            self.num_str_to_int(row[StudentsBySchoolGenderCOLUMNS['total']]),
            self.num_str_to_int(row[StudentsBySchoolGenderCOLUMNS['male']]),
            self.num_str_to_int(row[StudentsBySchoolGenderCOLUMNS['female']]),
            self.num_str_to_int(row[StudentsBySchoolGenderCOLUMNS['male_1_year']]),
            self.num_str_to_int(row[StudentsBySchoolGenderCOLUMNS['female_1_year']]),
            self.num_str_to_int(row[StudentsBySchoolGenderCOLUMNS['male_2_year']]),
            self.num_str_to_int(row[StudentsBySchoolGenderCOLUMNS['female_2_year']]),
            self.num_str_to_int(row[StudentsBySchoolGenderCOLUMNS['male_3_year']]),
            self.num_str_to_int(row[StudentsBySchoolGenderCOLUMNS['female_3_year']]),
            self.num_str_to_int(row[StudentsBySchoolGenderCOLUMNS['male_4_year']]),
            self.num_str_to_int(row[StudentsBySchoolGenderCOLUMNS['female_4_year']]),
            self.num_str_to_int(row[StudentsBySchoolGenderCOLUMNS['male_5_year']]),
            self.num_str_to_int(row[StudentsBySchoolGenderCOLUMNS['female_5_year']]),
            self.num_str_to_int(row[StudentsBySchoolGenderCOLUMNS['male_6_year']]),
            self.num_str_to_int(row[StudentsBySchoolGenderCOLUMNS['female_6_year']]),
            self.num_str_to_int(row[StudentsBySchoolGenderCOLUMNS['male_7_year']]),
            self.num_str_to_int(row[StudentsBySchoolGenderCOLUMNS['female_7_year']]),
            self.num_str_to_int(row[StudentsBySchoolGenderCOLUMNS['male_extended']]),
            self.num_str_to_int(row[StudentsBySchoolGenderCOLUMNS['female_extended']]),
            row[StudentsBySchoolGenderCOLUMNS['city_name']],
            row[StudentsBySchoolGenderCOLUMNS['school_system']]
        ]


class GraduatesBySchoolGenderExtractor(CSVExtractor):
    def extract(self, row):
        return [
            int(row[GraduatesBySchoolGenderCOLUMNS['school_id']]),
            row[GraduatesBySchoolGenderCOLUMNS['school_name']],
            row[GraduatesBySchoolGenderCOLUMNS['day_or_night']],
            row[GraduatesBySchoolGenderCOLUMNS['degree']],
            self.num_str_to_int(row[GraduatesBySchoolGenderCOLUMNS['male']]),
            self.num_str_to_int(row[GraduatesBySchoolGenderCOLUMNS['female']]),
            row[GraduatesBySchoolGenderCOLUMNS['city_name']],
            row[GraduatesBySchoolGenderCOLUMNS['school_system']]
        ]


EXTRACTORS = {
    'students_by_school_gender': StudentsBySchoolGenderExtractor,
    'graduates_by_school_gender': GraduatesBySchoolGenderExtractor
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, help='year to be processed')
    args = parser.parse_args()

    school_year = args.year

    with open(f'resources/{school_year}.json', 'r') as fp:
        data = fp.read()
        stats = json.loads(data)

    dao = RawSQLiteDAO()
    dao.connect(db_path='raw.db')
    dao.init()

    for table_name, url in stats.items():
        LOADER_CLASS = LOADERS.get(table_name)
        if LOADER_CLASS is None:
            continue

        loader = LOADER_CLASS(dao)
        extractor = EXTRACTORS[table_name]()
        filename = get_csv(url)
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for row in csv_reader:
                clean_row = extractor.extract(row)
                loader.load(school_year, clean_row)
