from django.test import TestCase
from candidator.models import Topic, Position, TakenPosition, Category
from popolo.models import Person
from candidator.comparer import Comparer, InformationHolder


class ComparisonTestCase(TestCase):
    def setUp(self):
        self.person1 = Person.objects.create(name=u"Person1")
        self.person2 = Person.objects.create(name=u"Person2")
        self.person3 = Person.objects.create(name=u"Person3")

        self.marihuana_topic = Topic.objects.create(label=u"Marihuana")
        self.marihuana_yes = Position.objects.create(
            topic=self.marihuana_topic,
            label=u"MarihuanaYes"
        )
        self.marihuana_no = Position.objects.create(
            topic=self.marihuana_topic,
            label=u"MarihuanaNo"
        )
        self.chamomile_topic = Topic.objects.create(label="Chamomile")
        self.chamomile_yes = Position.objects.create(
            topic=self.chamomile_topic,
            label=u"ChamomileYes"
        )
        self.chamomile_no = Position.objects.create(
            topic=self.chamomile_topic,
            label=u"ChamomileNo"
        )

        self.religion_topic = Topic.objects.create(label=u"Religion")
        self.religion_yes = Position.objects.create(
            topic=self.religion_topic,
            label=u"ReligionYes"
        )
        self.religion_no = Position.objects.create(
            topic=self.religion_topic,
            label=u"ReligionNo"
        )

        self.gay_marriage_topic = Topic.objects.create(label=u"GayMarriage")
        self.gay_marriage_yes = Position.objects.create(
            topic=self.gay_marriage_topic,
            label=u"GayMarriageYes"
        )
        self.gay_marriage_no = Position.objects.create(
            topic=self.gay_marriage_topic,
            label=u"GayMarriageNo"
        )
        #
        #   topic\person   |  person1 |  person2  |  person3
        #===================================================
        #   marihuana      |    y     |    n      |    n
        #   chamomille     |    y     |    n      |    n
        #   religion       |    n     |    y      |    n
        #   gay marriage   |    y     |    y      |    y
        #
        self.person1_chamomile_yes = TakenPosition.objects.create(
            topic=self.chamomile_topic,
            position=self.chamomile_yes,
            person=self.person1
        )

        self.person1_marihuana_yes = TakenPosition.objects.create(
            topic=self.marihuana_topic,
            position=self.marihuana_yes,
            person=self.person1
        )

        self.person1_religion_no = TakenPosition.objects.create(
            topic=self.religion_topic,
            position=self.religion_no,
            person=self.person1
        )

        self.person1_gay_marriage_yes = TakenPosition.objects.create(
            topic=self.gay_marriage_topic,
            position=self.gay_marriage_yes,
            person=self.person1
        )

        self.person2_chamomile_no = TakenPosition.objects.create(
            topic=self.chamomile_topic,
            position=self.chamomile_no,
            person=self.person2
        )

        self.person2_marihuana_no = TakenPosition.objects.create(
            topic=self.marihuana_topic,
            position=self.marihuana_no,
            person=self.person2
        )

        self.person2_religion_yes = TakenPosition.objects.create(
            topic=self.religion_topic,
            position=self.religion_yes,
            person=self.person2
        )

        self.person2_gay_marriage_yes = TakenPosition.objects.create(
            topic=self.gay_marriage_topic,
            position=self.gay_marriage_yes,
            person=self.person2
        )

        self.person3_chamomile_no = TakenPosition.objects.create(
            topic=self.chamomile_topic,
            position=self.chamomile_no,
            person=self.person3
        )

        self.person3_marihuana_no = TakenPosition.objects.create(
            topic=self.marihuana_topic,
            position=self.marihuana_no,
            person=self.person3
        )

        self.person3_religion_no = TakenPosition.objects.create(
            topic=self.religion_topic,
            position=self.religion_no,
            person=self.person3
        )

        self.person3_gay_marriage_yes = TakenPosition.objects.create(
            topic=self.gay_marriage_topic,
            position=self.gay_marriage_yes,
            person=self.person3
        )

    def test_compare_one_on_one(self):
        '''Compare one on one'''
        self.maxDiff = None
        comparer = Comparer()
        marihuana_position = TakenPosition(
            topic=self.marihuana_topic,
            position=self.marihuana_yes,
            )
        religion_position = TakenPosition(
            topic=self.religion_topic,
            position=self.religion_yes,
            )
        positions = {
            self.marihuana_topic.id: marihuana_position,
            self.religion_topic.id: religion_position
        }
        topics = [
            self.marihuana_topic,
            self.religion_topic
        ]
        comparer.topics = topics
        result = comparer.one_on_one(self.person1, positions)
        expected_result = {
            self.marihuana_topic.id: {
                "topic": self.marihuana_topic,
                "match": True,
                "my_position": self.marihuana_yes,
                "their_position": self.marihuana_yes
            },
            self.religion_topic.id: {
                "topic": self.religion_topic,
                "match": False,
                "my_position": self.religion_yes,
                "their_position": self.religion_no
            }
        }
        self.assertEquals(result, expected_result)

    def test_information_holder(self):
        '''InformationHolder'''
        information_holder = InformationHolder()
        marihuana_position = TakenPosition(
            topic=self.marihuana_topic,
            position=self.marihuana_yes,
            )
        religion_position = TakenPosition(
            topic=self.religion_topic,
            position=self.religion_yes,
            )
        information_holder.add_position(marihuana_position)
        information_holder.add_position(religion_position)
        self.assertEquals(information_holder.positions[self.marihuana_topic.id], marihuana_position)
        self.assertEquals(information_holder.positions[self.religion_topic.id], religion_position)

        information_holder.add_person(self.person1)
        self.assertEquals(information_holder.persons, [self.person1])
        information_holder.add_person(self.person2)
        self.assertEquals(information_holder.persons, [self.person1, self.person2])
        information_holder.add_person(self.person3)
        self.assertEquals(information_holder.persons, [self.person1, self.person2, self.person3])

        information_holder.add_topic(self.marihuana_topic)
        self.assertEquals(information_holder.topics, [self.marihuana_topic])

    def test_information_holder_with_categories(self):
        information_holder = InformationHolder()
        herbs_category = Category.objects.create(name="Herbs")
        self.marihuana_topic.category = herbs_category
        self.marihuana_topic.save()
        others_category = Category.objects.create(name="Others")
        self.religion_topic.category = others_category
        self.religion_topic.save()
        information_holder.add_category(herbs_category)
        information_holder.add_category(others_category)
        self.assertEquals(information_holder.categories, [herbs_category, others_category])
        self.assertEquals(information_holder.topics, [self.marihuana_topic, self.religion_topic])

    def test_split_positions_in_categories(self):
        information_holder = InformationHolder()
        herbs_category = Category.objects.create(name="Herbs")
        self.marihuana_topic.category = herbs_category
        self.marihuana_topic.save()
        self.chamomile_topic.category = herbs_category
        self.chamomile_topic.save()
        others_category = Category.objects.create(name="Others")
        self.religion_topic.category = others_category
        self.religion_topic.save()
        self.gay_marriage_topic.category = others_category
        self.gay_marriage_topic.save()
        marihuana_position = TakenPosition(
            topic=self.marihuana_topic,
            position=self.marihuana_yes,
            )
        religion_position = TakenPosition(
            topic=self.religion_topic,
            position=self.religion_yes,
            )

        chamomile_position = TakenPosition(
            topic=self.chamomile_topic,
            position=self.chamomile_no,
            )
        gay_marriage_position = TakenPosition(
            topic=self.gay_marriage_topic,
            position=self.gay_marriage_yes,
            )
        information_holder.add_position(marihuana_position)
        information_holder.add_position(religion_position)
        information_holder.add_position(chamomile_position)
        information_holder.add_position(gay_marriage_position)
        positions_by_herbs = information_holder.positions_by(herbs_category)
        self.assertEquals(positions_by_herbs[self.marihuana_topic.id], marihuana_position)
        self.assertEquals(positions_by_herbs[self.chamomile_topic.id], chamomile_position)

        positions_by_others = information_holder.positions_by(others_category)

        self.assertEquals(positions_by_others[self.religion_topic.id], religion_position)
        self.assertEquals(positions_by_others[self.gay_marriage_topic.id], gay_marriage_position)

    def test_compare_categories_with_information_holder(self):
        information_holder = InformationHolder()
        herbs_category = Category.objects.create(name="Herbs")
        self.marihuana_topic.category = herbs_category
        self.marihuana_topic.save()
        self.chamomile_topic.category = herbs_category
        self.chamomile_topic.save()
        others_category = Category.objects.create(name="Others")
        self.religion_topic.category = others_category
        self.religion_topic.save()
        self.gay_marriage_topic.category = others_category
        self.gay_marriage_topic.save()

        marihuana_position = TakenPosition(
            topic=self.marihuana_topic,
            position=self.marihuana_no,
            )
        religion_position = TakenPosition(
            topic=self.religion_topic,
            position=self.religion_no,
            )

        chamomile_position = TakenPosition(
            topic=self.chamomile_topic,
            position=self.chamomile_no,
            )
        gay_marriage_position = TakenPosition(
            topic=self.gay_marriage_topic,
            position=self.gay_marriage_yes,
            )
        information_holder.add_position(marihuana_position)
        information_holder.add_position(religion_position)
        information_holder.add_position(chamomile_position)
        information_holder.add_position(gay_marriage_position)
        information_holder.add_person(self.person1)
        information_holder.add_person(self.person2)
        information_holder.add_person(self.person3)
        information_holder.add_category(herbs_category)
        information_holder.add_category(others_category)
        comparer = Comparer()
        result = comparer.compare(information_holder)
        #
        #   topic\person   |  person1 |  person2  |  person3  | my positions
        #====================================================================
        #   marihuana      |    y     |    n      |    n      |    n
        #   chamomille     |    y     |    n      |    n      |    n
        #   religion       |    n     |    y      |    n      |    n
        #   gay marriage   |    y     |    y      |    y      |    y
        #====================================================================
        #     Afinity %    |   50%    |   75%     |   100%    |    N/A
        #
        self.maxDiff = None
        expected_result = [{"person": self.person3,
                            "explanation": {
                                herbs_category.slug: {
                                    "category": herbs_category,
                                    "per_topic": {
                                        self.marihuana_topic.id: {
                                            "topic": self.marihuana_topic,
                                            "match": True,
                                            'my_position': self.marihuana_no,
                                            'their_position': self.marihuana_no
                                        },
                                        self.chamomile_topic.id: {
                                            "topic": self.chamomile_topic,
                                            "match": True,
                                            'my_position': self.chamomile_no,
                                            'their_position': self.chamomile_no
                                        },
                                    }
                                },
                                others_category.slug: {
                                    "category": others_category,
                                    "per_topic": {

                                        self.religion_topic.id: {
                                            "topic": self.religion_topic,
                                            "match": True,
                                            'my_position': self.religion_no,
                                            'their_position': self.religion_no
                                        },
                                        self.gay_marriage_topic.id: {
                                            "topic": self.gay_marriage_topic,
                                            "match": True,
                                            'my_position': self.gay_marriage_yes,
                                            'their_position': self.gay_marriage_yes
                                        }
                                    }
                                }
                            },
                            "percentage": 1.0
                            },
                           {"person": self.person2,
                            "explanation": {
                                herbs_category.slug: {
                                    "category": herbs_category,
                                    "per_topic": {
                                        self.marihuana_topic.id: {
                                            "topic": self.marihuana_topic,
                                            "match": True,
                                            'my_position': self.marihuana_no,
                                            'their_position': self.marihuana_no
                                        },
                                        self.chamomile_topic.id: {
                                            "topic": self.chamomile_topic,
                                            "match": True,
                                            'my_position': self.chamomile_no,
                                            'their_position': self.chamomile_no
                                        }
                                    }
                                },
                                others_category.slug: {
                                    "category": others_category,
                                    "per_topic": {
                                        self.religion_topic.id: {
                                            "topic": self.religion_topic,
                                            "match": False,
                                            'my_position': self.religion_no,
                                            'their_position': self.religion_yes
                                        },
                                        self.gay_marriage_topic.id: {
                                            "topic": self.gay_marriage_topic,
                                            "match": True,
                                            'my_position': self.gay_marriage_yes,
                                            'their_position': self.gay_marriage_yes
                                        }
                                    }
                                }
                            },
                            "percentage": 0.75
                            },
                           {"person": self.person1,
                            "explanation": {
                                herbs_category.slug: {
                                    "category": herbs_category,
                                    "per_topic": {
                                        self.marihuana_topic.id: {
                                            "topic": self.marihuana_topic,
                                            "match": False,
                                            'my_position': self.marihuana_no,
                                            'their_position': self.marihuana_yes
                                        },
                                        self.chamomile_topic.id: {
                                            "topic": self.chamomile_topic,
                                            "match": False,
                                            'my_position': self.chamomile_no,
                                            'their_position': self.chamomile_yes
                                        }
                                    }
                                },
                                others_category.slug: {
                                    "category": others_category,
                                    "per_topic": {
                                        self.religion_topic.id: {
                                            "topic": self.religion_topic,
                                            "match": True,
                                            'my_position': self.religion_no,
                                            'their_position': self.religion_no
                                        },
                                        self.gay_marriage_topic.id: {
                                            "topic": self.gay_marriage_topic,
                                            "match": True,
                                            'my_position': self.gay_marriage_yes,
                                            'their_position': self.gay_marriage_yes
                                        }
                                    }
                                }
                            },
                            "percentage": 0.5
                            }]
        self.assertEquals(result, expected_result)

        #
        #   topic\person   |  person1 |  person2  |  person3  | my positions
        #====================================================================
        #   marihuana      |    y     |    n      |    n      |    n
        #   chamomille     |    y     |    n      |    n      |    n
        #   religion       |    -     |    y      |    n      |    n
        #   gay marriage   |    y     |    y      |    y      |    y
        #====================================================================
        #     Afinity %    |   25%    |   75%     |   100%    |    N/A
        #
        self.person1_religion_no.delete()
        result = comparer.compare(information_holder)
        self.assertEquals(result[2]['percentage'], 0.25)

    def test_compare_one_on_one_not_giving_a_taken_position(self):
        '''Compare one on one'''
        comparer = Comparer()
        marihuana_position = TakenPosition(
            topic=self.marihuana_topic,
            position=self.marihuana_yes,
            )
        positions = {
            self.marihuana_topic.id: marihuana_position
        }
        topics = [
            self.marihuana_topic,
            self.religion_topic
        ]
        comparer.topics = topics
        result = comparer.one_on_one(self.person1, positions)

        expected_result = {
            self.marihuana_topic.id: {
                "topic": self.marihuana_topic,
                "match": True,
                "my_position": self.marihuana_yes,
                "their_position": self.marihuana_yes
            },
            self.religion_topic.id: {
                "topic": self.religion_topic,
                "match": False,
                "my_position": None,
                "their_position": self.religion_no
            }
        }
        self.assertEquals(result, expected_result)

        # If there are no taken positions it should for a given position it should
        # automatically determine that this is not a match.
        taken_position = TakenPosition.objects.get(person=self.person1, topic=self.religion_topic)
        taken_position.position = None
        taken_position.save()
        result2 = comparer.one_on_one(self.person1, positions)
        self.assertFalse(result2[self.religion_topic.id]["match"])

        TakenPosition.objects.filter(topic=self.religion_topic).delete()
        result3 = comparer.one_on_one(self.person1, positions)
        self.assertFalse(result3[self.religion_topic.id]["match"])
