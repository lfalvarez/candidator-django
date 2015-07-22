# -*- coding: utf-8 -*-
from django.test import TestCase
from candidator.models import Topic, Position, TakenPosition, Category
from popolo.models import Person


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
        self.assertTrue(topic.slug)

        self.assertEquals(topic.__str__(), u"<Should marijuana be legalized?>")

    def test_get_taken_position(self):
        topic = Topic.objects.create(
            label=u"Should marijuana be legalized?",
            description=u"This is a description of the topic of marijuana")

        position = Position.objects.create(
            topic=topic,
            label=u"Yes",
            description=u"Yes, means that it is considered a good thing for marijuana to be legalized"
        )
        person = Person.objects.create(name=u"Felipe")
        taken_position = TakenPosition.objects.create(
            topic=topic,
            position=position,
            person=person,
        )
        self.assertEquals(topic.get_taken_position_for(person), taken_position)
        taken_position.delete()
        self.assertIsNone(topic.get_taken_position_for(person))


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

        self.assertEquals(position.__str__(), u"<Yes> to <Should marijuana be legalized?>")
        # Reverse naming
        self.assertIn(position, self.topic.positions.all())


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
        self.assertEquals(taken_position.__str__(), "<Felipe> says <Yes> to <Should marijuana be legalized?>")

        self.assertIn(taken_position, self.topic.taken_positions.all())
        self.assertIn(taken_position, self.position.taken_positions.all())
        self.assertIn(taken_position, self.person.taken_positions.all())

    def test_can_be_saved_without_a_position(self):
        '''We can save a TakenPosition without a position'''
        taken_position = TakenPosition.objects.create(
            topic=self.topic,
            person=self.person,
            description=u"This is a total description"
        )
        self.assertIsNone(taken_position.position)
        self.assertEquals(taken_position.__str__(), u"<Felipe> doesn't have an opinion in <Should marijuana be legalized?>")

    def test_str_without_a_person(self):
        '''A taken position can be instantiated withouth a person therefore the __str__ method should be able to handle that'''
        taken_position = TakenPosition(
            topic=self.topic,
            position=self.position,
        )
        self.assertEquals(taken_position.__str__(), "<Unknown> says <Yes> to <Should marijuana be legalized?>")

    def test_issue_243_votainteligente(self):
        '''str TakenPosition with non unicode text'''
        self.person.name = u"Felipe Álvarez"
        self.topic.label = u"Debería ser legalizada?"
        self.position.label = u"Sí, por supuesto!"
        taken_position = TakenPosition.objects.create(
            topic=self.topic,
            position=self.position,
            person=self.person
        )
        self.assertEquals(taken_position.__str__(), "<Felipe Álvarez> says <Sí, por supuesto!> to <Debería ser legalizada?>")

    def test_taken_position_can_have_sources(self):
        '''TakenPositions can have sources'''
        taken_position = TakenPosition.objects.create(
            topic=self.topic,
            position=self.position,
            person=self.person
        )
        taken_position.sources.create(url='http://link.example.org/', note='Note')
        self.assertEqual(taken_position.sources.count(), 1)


class TopicCategoryTestCase(TestCase):
    def setUp(self):
        self.topic1 = Topic.objects.create(
            label=u"Should marijuana be legalized?",
            description=u"This is a description of the topic of marijuana")

        self.topic2 = Topic.objects.create(
            label=u"Should marijuana be grown by the state?",
            description=u"This is a description of the topic of marijuana")

        self.topic3 = Topic.objects.create(
            label=u"Should regligion be taught at schools?",
            description=u"This is a description of the topic of religion")

        self.topic4 = Topic.objects.create(
            label=u"What do you think of morality?",
            description=u"This is a description of the topic of religion")

    def test_it_cant_be_instanciated(self):
        '''I can instanciate a category'''
        category = Category.objects.create(name=u"Marihuana Category")
        category.topics.add(self.topic1)
        category.topics.add(self.topic2)

        self.assertTrue(category)
        self.assertEquals(category.name, u"Marihuana Category")
        self.assertTrue(category.slug)
        self.assertEquals(category.slug, u"marihuana-category")
        self.assertEquals(self.topic1.category, category)
        self.assertEquals(self.topic2.category, category)

        self.assertEquals(category.__str__(), "<Marihuana Category>")
