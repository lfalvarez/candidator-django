from django.test import TestCase
from candidator.models import Topic, Position, TakenPosition
from popolo.models import Person
from candidator.comparer import Comparer


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
