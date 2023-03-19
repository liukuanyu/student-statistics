class Loader:
    def __init__(self, dao):
        self._dao = dao

    def load(self, school_year, row):
        raise NotImplementedError('subclass should implement this method')


class StudentsBySchoolGenderLoader(Loader):
    def __init__(self, dao):
        super().__init__(dao)

    def load(self, school_year, row):
        values = [school_year] + row
        self._dao.insert_students_by_school_gender(values)


class GraduatesBySchoolGenderLoader(Loader):
    def __init__(self, dao):
        super().__init__(dao)

    def load(self, school_year, row):
        values = [school_year] + row
        self._dao.insert_graduates_by_school_gender(values)


LOADERS = {
    'students_by_school_gender': StudentsBySchoolGenderLoader,
    'graduates_by_school_gender': GraduatesBySchoolGenderLoader
}
