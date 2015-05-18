from candidator.models import TakenPosition


class CandidatorAdapter():
    def is_topic_category_the_same_as(self, topic, category):
        return topic.category == category

    def get_taken_position_by(self, person, topic):
        return TakenPosition.objects.get(person=person,
                                         topic=topic)


class CandidatorCalculator():
    final_results_key = 'percentage'

    def determine_match(self, topic, person_position, external_position):
        match = False
        if external_position == person_position:
            match = True

        return {"topic": topic, "match": match}

    def determine_points_per_person_per_category(self, explanation):
        points = 0
        for t in explanation:
            if explanation[t]["match"]:
                points += 1
        return points

    def determine_total_result_per_person(self, points_per_person, total_comparisons):
        if total_comparisons:
            percentage = float(points_per_person) / float(total_comparisons)
        else:
            percentage = 0
        return {self.final_results_key: percentage}

    def order_by(self):
        return self.final_results_key
