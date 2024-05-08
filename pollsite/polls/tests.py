import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse


# Create your tests here.

class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        '''
        must return False for questions published in the future
        '''
        time = timezone.now() + datetime.timedelta(30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


    def test_was_published_recently_with_past_question(self):
        '''
        test must return False for questions published in the past
        '''

        time = timezone.now() - datetime.timedelta(1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recently_question(self):
        '''
        test must return True for questions published in the present
        '''

        time = timezone.now()
        present_question = Question(pub_date=time)
        self.assertIs(present_question.was_published_recently(), True)

def create_question(question_text, days):

    '''This function creates test with a given text and publishing day offset to now (positive for future and negative days for past)'''

    time = timezone.now() + datetime.timedelta(days)
    question = Question.objects.create(question_text = question_text, pub_date=time)
    return question


# Testing for the index view

class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        '''
        If there are no questions available. 
        '''
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])


    def test_past_question(self):
        '''
        Checks if questions with pub_date ins the past are displayed
        '''
        question = create_question("test past question", -29)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question]
        )

    def test_future_question(self):
        '''
        Questions in the future must not be displayed
        '''

        question = create_question("test future question", 20)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            []
        )

'''Tests for the detail view'''

class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        '''Detail page of questions with future pub_date must return page 404 not found'''

        question = create_question("future question", 20)
        url = reverse("polls:detail", args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        '''Detail view of questions in the past must return the question text'''

        question = create_question("past question", -10)
        url = reverse("polls:detail", args=(question.id,))
        response = self.client.get(url)
        self.assertContains(response, question.question_text)


'''Tests for Results view'''

class QuestionResultViewTests(TestCase):
    def test_past_question(self):
        '''Displays the results for past questions'''

        question = create_question("past question", -39)
        url = reverse("polls:results", args=(question.id,))
        response = self.client.get(url)
        self.assertContains(response, question.question_text)

    def test_future_question(self):
        '''Displays page not found for future questions'''
        question = create_question("future question", 20)
        url = reverse("polls:results", args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

                      