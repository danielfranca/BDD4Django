# *-* coding: utf-8 *-*

from bdd4django.helpers import BDDCoreTestCase, BDDTestCase
from model_mommy import mommy

from polls.models import Poll, Choice

class PollsCoreTest(BDDCoreTestCase):

    fixtures = ['poll_users.json',]

    def extra_setup(self):
        self.client = self.client_class()

    def test_evaluate_file(self):
        self.parse_feature_file('polls')

    def prepare_database(self):
        poll  = mommy.make_one(Poll, question=u"What's the best Python IDE/Editor")
        choices = "WingIDE,PyCharm,Vi,Gedit,Eclipse,Aptana"
        [mommy.make_one(Choice, poll=poll, choice_text=choice_text) for choice_text in choices.split(',')]


class PollsBrowserTest(BDDTestCase):

    fixtures = ['poll_users.json',]

    def test_evaluate_file(self):
        self.parse_feature_file(file_path='polls/polls_browser.feature', scenarios=('Add new poll','Add new choices'))

    def prepare_database(self):
        r'a poll "([^"]+)" with choices "([^"]+)"'
        poll  = mommy.make_one(Poll, question=u"What's the best Python IDE/Editor")
        choices = "WingIDE,PyCharm,Vi,Gedit,Eclipse,Aptana"
        [mommy.make_one(Choice, poll=poll, choice_text=choice_text) for choice_text in choices.split(',')]

