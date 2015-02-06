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
