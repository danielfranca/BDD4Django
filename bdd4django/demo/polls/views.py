from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from polls.models import Poll, Choice, PollChoice
from polls.forms import PollChoiceForm

@login_required
def vote(request, poll_id):

    poll = get_object_or_404(Poll, id=poll_id)

    if PollChoice.objects.filter(user=request.user, poll=poll).exists():
        return redirect(reverse('total_votes',kwargs={'poll_id': poll.id,}))

    form = PollChoiceForm(poll, request.POST or None)

    if form.is_valid():
        poll_choice = form.save(commit=False)
        poll_choice.user = request.user
        poll_choice.poll = poll
        poll_choice.save()

        return redirect(reverse('total_votes',kwargs={'poll_id': poll.id,}))

    return render_to_response(
        'polls/vote.html',
        {
            'poll': poll,
            'form': form,
        },
        context_instance=RequestContext(request)
    )


def total_votes(request, poll_id):

    poll = get_object_or_404(Poll, id=poll_id)
    percent_votes = [(choice.choice_text, choice.percent_for_choice()) for choice in Choice.objects.filter(poll=poll)]

    return render_to_response(
        'polls/total_votes.html',
        {
            'poll': poll,
            'percent_votes': percent_votes,
            'total_votes': poll.total_votes(),
        },
        context_instance=RequestContext(request)
    )




