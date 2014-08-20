from django.test import TestCase
from candidator.models import Topic, Position, TakenPosition
from popolo.models import Person

# Create your tests here.

class TopicTestCase(TestCase):
    def setUp(self):
        pass

    def test_instanciate(self):
        '''Instanciate a topic'''
        topic = Topic.objects.create(
            label=u"Should marijuana be legalized?",
            description=u"This is a description of the topic of marijuana")

        self.assertTrue(topic)
        self.assertEquals(topic.label, u"Should marijuana be legalized?")
        self.assertEquals(topic.description, u"This is a description of the topic of marijuana")



class PositionTestCase(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(
            label=u"Should marijuana be legalized?",
            description=u"This is a description of the topic of marijuana")

    def test_instanciate_a_position_on_a_given_topic(self):
        '''Instanciate a position on a given topic'''
        position = Position.objects.create(
            topic=self.topic,
            label=u"Yes",
            description=u"Yes, means that it is considered a good thing for marijuana to be legalized"
        )
        self.assertTrue(position)
        self.assertEquals(position.topic, self.topic)
        self.assertEquals(position.label, u"Yes")
        self.assertEquals(position.description, u"Yes, means that it is considered a good thing for marijuana to be legalized")



class TakenPositionTestCase(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(
            label=u"Should marijuana be legalized?",
            description=u"This is a description of the topic of marijuana")
        self.position = Position.objects.create(
            topic=self.topic,
            label=u"Yes",
            description=u"Yes, means that it is considered a good thing for marijuana to be legalized"
        )
        self.person = Person.objects.create(name=u"Felipe")

    def test_it_can_be_instanciated(self):
        '''A taken position can be instanciated'''
        taken_position = TakenPosition.objects.create(
            topic=self.topic,
            position=self.position,
            person=self.person
        )
        self.assertTrue(taken_position)
        self.assertEquals(taken_position.topic, self.topic)
        self.assertEquals(taken_position.position, self.position)
        self.assertEquals(taken_position.person, self.person)
