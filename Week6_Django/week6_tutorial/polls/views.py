from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Question, Choice

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "index.html", context)

def detail(request, question_id):
    question = Question.objects.get(pk=question_id)
    return render(request, "detail.html", {
        "question": question,
        "choices": question.choice_set.all().order_by("choice_text")
    })

def vote(request, question_id):
    question = Question.objects.get(pk=question_id)

    if request.method == "GET":
        return render(request, "vote.html", {
            "question": question,
            "choices": question.choice_set.all().order_by("choice_text")
        })
    elif request.method == "POST":
        choice_id = request.POST.get('choice')
        choice = Choice.objects.get(pk=choice_id)
        choice.votes += 1
        choice.save()
        return redirect("detail", question_id=question_id)