from candidator.models import TakenPosition


class CandidatorAdapter():
    def is_topic_category_the_same_as(self, topic, category):
        return topic.category == category

    def get_taken_position_by(self, person, topic):
        return TakenPosition.objects.get(person=person,
                                         topic=topic)


class CandidatorCalculator():
    '''
    This class does all the calculations related to comparing
    several persons's positions to your positions
    '''
    final_results_key = 'percentage'

    def determine_match(self, person_position, external_position):
        '''
        Receives two person's positions on an issue and determines if they are a match.
        In the simplest case, this method determines if this is just a match and returns a dict with {'match': True}
        or {'match': False}.
        There can be more complex calculations regarding how different the positions are.
        '''
        match = False
        if external_position == person_position:
            match = True

        return {"match": match}

    def determine_points_per_person_per_category(self, explanation):
        '''
        This determines how many points should a person receives based on a comparison previously done with
        determine_match(person_position, external_position)
        per category.
        In the simplest form, we add one point per match.
        '''
        points = 0
        for t in explanation:
            if explanation[t]["match"]:
                points += 1
        return points

    def determine_total_result_per_person(self, points_per_person, total_comparisons):
        '''
        This determines the final score of a candidate. In the most basic form, this is a percentage of matches.
        '''
        if total_comparisons:
            percentage = float(points_per_person) / float(total_comparisons)
        else:
            percentage = 0
        return {self.final_results_key: percentage}

    def order_by(self):
        '''
        This returns the key that we are looking for when searching for the final result.
        The default value is "percentage".
        '''
        return self.final_results_key
