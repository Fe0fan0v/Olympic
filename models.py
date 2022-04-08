class Part:
    def __init__(self, name: str):
        self.name = name
        self.task_list = [Task]

    def add_task(self, task):
        self.task_list.append(task)


class Task:
    def __init__(self, part: Part, points: int, answer: str):
        self.part = part
        self.points = points
        self.answer = answer


class Team:
    def __init__(self, name: str, school: str, scores=0, position=None):
        self.name = name
        self.school = school
        self.scores = scores
        self.position = position
