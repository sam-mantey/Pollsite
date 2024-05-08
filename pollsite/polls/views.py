from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.db.models import F
from .models import Question, Choice
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# Create your views here.

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        #return the 5 latest polls
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):

        '''Returns questions with pub_date less or equal to today'''
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request, 
            "polls/detail",
            {
                "question": question,
                "error_message": "You didn't select a choice"
            }
        )
    else: 
        #adds 1 vote to the selected choise
        #F("votes") + 1 is used to instruct the database to increase the value ov votes by 1
        selected_choice.votes = F("votes") + 1

        #Saves the changes made to the database
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))




