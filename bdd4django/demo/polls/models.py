from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class Poll(models.Model):
    question = models.CharField(_('Question'),max_length=200)
    pub_date = models.DateTimeField(_('Date published'), auto_now_add=True, auto_now=True)

    def __unicode__(self):
        return self.question

    def total_votes(self):
        return sum([choice.votes_for_choice() for choice in Choice.objects.filter(poll=self)])

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(_('Choice text'), max_length=200)

    def __unicode__(self):
        return self.choice_text

    def votes_for_choice(self):
        return PollChoice.objects.filter(choice=self).count()

    def percent_for_choice(self):
        return (PollChoice.objects.filter(choice=self).count()*100)/(self.poll.total_votes() or 1)

class PollChoice(models.Model):
    poll   = models.ForeignKey(Poll)
    user   = models.ForeignKey(User)
    choice = models.ForeignKey(Choice)

    class Meta:
        unique_together = ("user", "poll")


