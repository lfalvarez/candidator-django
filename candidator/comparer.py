from candidator.models import TakenPosition


class InformationHolder():
    def __init__(self, *args, **kwargs):
        self.positions = {}
        self.persons = []
        self.topics = []
        self.categories = []

    def add_topic(self, topic):
        self.topics.append(topic)

    def add_position(self, position):
        self.positions[position.topic.slug] = position

    def add_person(self, person):
        self.persons.append(person)

    def add_category(self, category):
        self.categories.append(category)
        for topic in category.topics.all():
            self.add_topic(topic)

    def positions_by(self, category):
        result = {}
        for topic_slug in self.positions:
            if self.positions[topic_slug].topic.category == category:
                result[topic_slug] = self.positions[topic_slug]
        return result


class Comparer():
    def __init__(self, *args, **kwargs):
        self.topics = None

    def one_on_one(self, person, positions, topics=None):
        comparison = {}
        if topics is None:
            topics = self.topics
        for topic in topics:
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
        if not information_holder.categories:
            return self.several(information_holder.persons, information_holder.positions)
        return self.compare_information_holder(information_holder)

    def compare_information_holder(self, information_holder):
        result = {}
        persons = information_holder.persons
        categories = information_holder.categories
        for person in persons:
            amount_of_matches_in_category = 0
            comparisons_per_category = 0
            explanations_per_person = {}
            for category in categories:
                positions = information_holder.positions_by(category)
                explanation = self.one_on_one(person, positions, topics=category.topics.all())
                explanations_per_person[category.slug] = explanation

                for t in explanation:
                    if explanation[t]["match"]:
                        amount_of_matches_in_category += 1
                comparisons_per_category += len(explanation)

            if comparisons_per_category:
                percentage = float(amount_of_matches_in_category) / float(comparisons_per_category)
            else:
                percentage = 0

            result[person.id] = {"person": person,
                                 "explanation": explanations_per_person,
                                 "percentage": percentage}

        def key(person_id):
            return result[person_id]['percentage']
        keys = sorted(result, key=key, reverse=True)
        ordered_result = []
        for key in keys:
            ordered_result.append(result[key])
        return ordered_result

    def several(self, persons, positions, categories=None):
        result = {}
        for person in persons:
            explanation = self.one_on_one(person, positions)
            amount_of_matches = 0
            for t in explanation:
                if explanation[t]["match"]:
                    amount_of_matches += 1
            len_explanation = len(explanation)
            if len_explanation:
                percentage = float(amount_of_matches) / float(len_explanation)
            else:
                percentage = 0
            result[person.id] = {
                "explanation": explanation,
                "percentage": percentage
            }
        return result
