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
        self.positions[position.topic.id] = position

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
            candidate_taken_position = self.adapter.get_taken_position_by(person, topic)
            comparison[topic.id] = {"topic": topic}
            if candidate_taken_position is not None and candidate_taken_position.position is not None:
                users_taken_position = positions.get(topic.id, None)
                external_position = None
                comparison[topic.id]['my_position'] = None
                if users_taken_position:
                    external_position = users_taken_position.position
                    comparison[topic.id]['my_position'] = users_taken_position.position
                comparison[topic.id]['their_position'] = candidate_taken_position.position
                comparison[topic.id].update(self.calculator.determine_match(candidate_taken_position.position,
                                                                            external_position))
            else:
                comparison[topic.id].update(self.calculator.determine_not_match())
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
                explanations_per_person[category.slug] = {
                    'category': category,
                    'per_topic': explanation
                }
                points_per_person += self.calculator.determine_points_per_person_per_category(explanation)
                comparisons_per_category += len(explanation)
            result[person.id] = {"person": person,
                                 "explanation": explanations_per_person}
            result[person.id].update(self.calculator.
                determine_total_result_per_person(points_per_person, comparisons_per_category))

        def key(person_id):
            return result[person_id][self.calculator.order_by()]
        keys = sorted(result, key=key, reverse=self.calculator.order_reversed)
        ordered_result = []
        for key in keys:
            ordered_result.append(result[key])
        return ordered_result
