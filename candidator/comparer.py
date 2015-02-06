from candidator.models import TakenPosition


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

    def several(self, persons, positions):
        result = {

        }
        for person in persons:
            explanation = self.one_on_one(person, positions)
            amount_of_matches = 0
            for t in explanation:
                if explanation[t]["match"]:
                    amount_of_matches += 1
            percentage = float(amount_of_matches) / float(len(explanation))
            result[person.slug] = {
                "explanation": explanation,
                "percentage": percentage
            }
        return result
