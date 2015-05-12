from candidator.models import TakenPosition


class InformationHolder():
    def __init__(self, *args, **kwargs):
        self.positions = {}
        self.persons = []
        self.topics = []

    def add_topic(self, topic):
        self.topics.append(topic)

    def add_position(self, position):
        self.positions[position.topic.slug] = position

    def add_person(self, person):
        self.persons.append(person)


class Comparer():
    def __init__(self, *args, **kwargs):
        self.topics = None

    def one_on_one(self, person, positions):
        comparison = {}
        for topic in self.topics:
            person_taken_positions = TakenPosition.objects.get(
                person=person,
                topic=topic
                )
            r = False
            if positions[topic.slug].position == person_taken_positions.position:
                r = True
            comparison[topic.slug] = {
                "topic": topic,
                "match": r
            }
        return comparison

    def compare(self, information_holder):
        self.topics = information_holder.topics
        return self.several(information_holder.persons, information_holder.positions)

    def several(self, persons, positions):
        result = {}
        for person in persons:
            explanation = self.one_on_one(person, positions)
            amount_of_matches = 0
            for t in explanation:
                if explanation[t]["match"]:
                    amount_of_matches += 1
            percentage = float(amount_of_matches) / float(len(explanation))
            result[person.id] = {
                "explanation": explanation,
                "percentage": percentage
            }
        return result
