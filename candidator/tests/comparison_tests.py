from django.test import TestCase
from candidator.models import Topic, Position, TakenPosition
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
        self.religion_topic = Topic.objects.create(label=u"Religion")
        self.religion_yes = Position.objects.create(
            topic=self.religion_topic,
            label=u"ReligionYes"
        )
        self.religion_no = Position.objects.create(
            topic=self.religion_topic,
            label=u"ReligionNo"
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

    def test_compare_one_on_one(self):
        '''Compare one on one'''
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
            self.marihuana_topic.slug: marihuana_position,
            self.religion_topic.slug: religion_position
        }
        topics = [
            self.marihuana_topic,
            self.religion_topic
        ]
        comparer.topics = topics
        result = comparer.one_on_one(self.person1, positions)
        expected_result = {
            self.marihuana_topic.slug: {
                "topic": self.marihuana_topic,
                "match": True
            },
            self.religion_topic.slug: {
                "topic": self.religion_topic,
                "match": False
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
        self.assertEquals(information_holder.positions[self.marihuana_topic.slug], marihuana_position)
        self.assertEquals(information_holder.positions[self.religion_topic.slug], religion_position)

        information_holder.add_person(self.person1)
        self.assertEquals(information_holder.persons, self.person1)
        information_holder.add_person(self.person2)
        self.assertEquals(information_holder.persons, [self.person1, self.person2])
        information_holder.add_person(self.person3)
        self.assertEquals(information_holder.persons, [self.person1, self.person2, self.person3])

        information_holder.add_topic(self.marihuana_topic)
        self.assertEquals(information_holder.topics, [self.marihuana_topic])

    def test_compare_with_information_holder(self):
        '''Compare using InformationHolder'''
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
        information_holder.add_person(self.person1)
        information_holder.add_person(self.person2)
        information_holder.add_topic(self.marihuana_topic)
        information_holder.add_topic(self.religion_topic)
        comparer = Comparer()
        result = comparer.compare(information_holder)
        expected_result = {
            self.person1.slug: {
                "explanation": {
                    self.marihuana_topic.slug: {
                        "topic": self.marihuana_topic,
                        "match": True
                    },
                    self.religion_topic.slug: {
                        "topic": self.religion_topic,
                        "match": False
                    }
                },
                "percentage": 0.5

            },
            self.person2.slug: {
                "explanation": {
                    self.marihuana_topic.slug: {
                        "topic": self.marihuana_topic,
                        "match": False
                    },
                    self.religion_topic.slug: {
                        "topic": self.religion_topic,
                        "match": True
                    }
                },
                "percentage": 0.5
            }
        }
        self.assertEquals(result, expected_result)

    def test_compare_several(self):
        '''Compare with several persons'''
        marihuana_position = TakenPosition(
            topic=self.marihuana_topic,
            position=self.marihuana_yes,
            )
        religion_position = TakenPosition(
            topic=self.religion_topic,
            position=self.religion_yes,
            )
        positions = {
            self.marihuana_topic.slug: marihuana_position,
            self.religion_topic.slug: religion_position
        }
        topics = [
            self.marihuana_topic,
            self.religion_topic
        ]

        persons = [self.person1, self.person2]

        expected_result = {
            self.person1.slug: {
                "explanation": {
                    self.marihuana_topic.slug: {
                        "topic": self.marihuana_topic,
                        "match": True
                    },
                    self.religion_topic.slug: {
                        "topic": self.religion_topic,
                        "match": False
                    }
                },
                "percentage": 0.5

            },
            self.person2.slug: {
                "explanation": {
                    self.marihuana_topic.slug: {
                        "topic": self.marihuana_topic,
                        "match": False
                    },
                    self.religion_topic.slug: {
                        "topic": self.religion_topic,
                        "match": True
                    }
                },
                "percentage": 0.5
            }
        }
        comparer = Comparer()
        comparer.topics = topics
        result = comparer.several(persons, positions)

        self.assertEquals(expected_result[self.person1.slug], result[self.person1.slug])
        self.assertEquals(expected_result[self.person2.slug], result[self.person2.slug])
