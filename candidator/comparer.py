from candidator.adapters import CandidatorAdapter, CandidatorCalculator


class InformationHolder():
    def __init__(self, adapter=CandidatorAdapter, *args, **kwargs):
        self.positions = {}
        self.persons = []
        self.topics = []
        self.categories = []
        self.adapter = adapter()

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
            if self.adapter.is_topic_category_the_same_as(self.positions[topic_slug].topic, category):
                result[topic_slug] = self.positions[topic_slug]
        return result


class Comparer():
    def __init__(self, adapter_class=CandidatorAdapter, calculator_class=CandidatorCalculator, *args, **kwargs):
        self.topics = None
        self.adapter = adapter_class()
        self.calculator = calculator_class()

    def one_on_one(self, person, positions, topics=None):
        comparison = {}
        if topics is None:
            topics = self.topics
        for topic in topics:
            person_taken_positions = self.adapter.get_taken_position_by(person, topic)
            comparison[topic.slug] = self.calculator.determine_match(topic,
                                                          person_taken_positions.position,
                                                          positions[topic.slug].position)
        return comparison

    def compare(self, information_holder):
        return self.compare_information_holder(information_holder)

    def compare_information_holder(self, information_holder):
        result = {}
        persons = information_holder.persons
        categories = information_holder.categories
        for person in persons:
            points_per_person = 0
            comparisons_per_category = 0
            explanations_per_person = {}
            for category in categories:
                positions = information_holder.positions_by(category)
                explanation = self.one_on_one(person, positions, topics=category.topics.all())
                explanations_per_person[category.slug] = explanation
                points_per_person += self.calculator.determine_points_per_person_per_category(explanation)
                comparisons_per_category += len(explanation)

            result[person.id] = {"person": person,
                                 "explanation": explanations_per_person}

            result[person.id].update(self.calculator.
                determine_total_result_per_person(points_per_person, comparisons_per_category))

        def key(person_id):
            return result[person_id][self.calculator.order_by()]
        keys = sorted(result, key=key, reverse=True)
        ordered_result = []
        for key in keys:
            ordered_result.append(result[key])
        return ordered_result
