from dataclasses import dataclass
from allen.solution import SubjectSolution
from datetime import datetime


@dataclass(frozen=True, order=True)
class TestRecord:
    biology: int
    '''The marks received in biology'''

    physics: int
    '''The marks received in physics'''

    chemistry: int
    '''The marks received in chemistry'''

    maths: int
    '''The marks received in maths'''

    total: int
    '''The total marks received'''

    percentage: float
    '''The percentage of marks'''

    rank: int
    '''Rank received in the test'''

    test_name: str
    '''
    The name of the test
    
    Example::
    
        JEE ENTHUSE INTERNAL TEST-01-PAPER 1
    '''

    _test_date: str
    '''The date the test was conducted'''

    _test_id: str
    '''The unique ID of the test.'''

    @classmethod
    def from_json(cls, json_obj: dict, client):
        """
        Deserialize the video json dict to a TestRecord object.

        :param json_obj: The json dictionary to deserialize.
        :param client: The allen client.
        :meta private:
        """
        bio = json_obj.get('Bio')
        phy = json_obj.get('Phy')
        chem = json_obj.get('Chem')
        math = json_obj.get('Math')
        total = json_obj.get('Total')
        percentage = json_obj.get('Per')
        rank = json_obj.get('Rank')
        name = json_obj.get('TestName')
        date = json_obj.get('TestDate')
        id = json_obj.get('TestID')
        cls.client = client

        return TestRecord(bio, phy, chem, math, total, percentage, rank, name, date, id)

    def get_subject_solutions(self) -> list[SubjectSolution]:
        """
        Get the solutions of the test.

        :return: A list of SubjectSolution objects.
        """
        solution = self.client.fetch_json('GetTestSolution', post_data={
            'PaperNo': 1,
            'TestID': self._test_id
        })

        subjects = solution['listPaper'][0]['listSubject']
        solutions = list()
        for subject in subjects:
            solutions.append(SubjectSolution.from_json(subject))

        return solutions

    def get_test_date(self) -> str:
        """
        Returns the date of the test in ``Thursday : 01 January 1970`` format.

        :return: The date if a valid date is present, else None.
        """
        try:
            return datetime.fromisoformat(self._test_date).strftime('%A : %d %B %Y')
        except ValueError:
            return None
