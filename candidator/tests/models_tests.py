from django.test import TestCase
from candidator.models import Topic, Position

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
