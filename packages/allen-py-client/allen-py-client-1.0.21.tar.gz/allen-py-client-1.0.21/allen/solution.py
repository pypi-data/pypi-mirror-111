from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Solution:
    question_no: int
    '''The number of the question'''

    response: str
    '''The answer marked while attempting the test'''

    image: str
    '''The url of the image containing the solution'''

    @classmethod
    def from_json(cls, json_obj: dict):
        """
        Deserialize the video json dict to a TestSolution object.

        :param json_obj: The json dictionary to deserialize.
        :meta private:
        """
        question_no = json_obj.get('QuestionNo')
        response = json_obj.get('Response')
        image = json_obj.get('SolutionImage')

        return Solution(question_no, response, image)


@dataclass(frozen=True, order=True)
class SubjectSolution:
    subject_name: str
    '''The name of the subject'''

    total_questions: int
    '''The number of questions which were present for the subject'''

    solutions: list[Solution]
    '''The list of solutions for the subject'''

    @classmethod
    def from_json(cls, json_obj: dict):
        """
        Deserialize the video json dict to a TestSolution object.

        :param json_obj: The json dictionary to deserialize.
        :meta private:
        """
        subject_name = str(json_obj.get('SubjectName')).title()
        total_questions = json_obj.get('QTo')
        solutions = list()

        questions = json_obj.get('listQuestion')
        for question in questions:
            solutions.append(Solution.from_json(question))

        return SubjectSolution(subject_name, total_questions, solutions)

    def get_solutions(self):
        """
        Get the list of Solution for the subject.

        :return: A list of :class:`the Solution object <solution.Solution>`
        """
        return self.solutions
