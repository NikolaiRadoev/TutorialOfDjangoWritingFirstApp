from django.shortcuts import get_object_or_404, render, redirect
from django.db import transaction
from django.contrib import messages
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.utils import timezone

from .models import Question, User, Answer
from .forms import QuestionChoiceForm
from django.views import generic

# Create your views here.
# 1
"""def index(request):
    return HttpResponse("Hello, world. You're at the polls index")"""


def detail(request, question_id, user_id):
    _user_id = request.session.get("user_id")

    if not _user_id:
        raise ValueError("You are not logged")

    user = User.objects.get(pk=_user_id)

    if not user.id == user_id:
        raise ValueError("You dont have permission")

    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    form = QuestionChoiceForm(request.POST or None, question=question)

    if request.method == "POST":
        if form.is_valid():
            choice_id = form.cleaned_data["choice"]

            try:
                selected_choice = question.choice_set.get(pk=choice_id)
            except Exception:
                messages.error(request, "Choice not found")
            else:
                try:
                    with transaction.atomic():
                        selected_choice.votes += 1
                        selected_choice.save()
                        answer = Answer(
                            user_id=user,
                            is_vote=True,
                            choice_text=selected_choice,
                            question_text=question,
                        )
                        answer.save()
                    messages.success(request, "Nice")
                    return redirect("home", user_id)
                except Exception as e:
                    messages.error(request, "Unexpected error: %s" % e)

    return render(
        request, "polls/detail.html", {"question": question, "user": user, "form": form}
    )


def results(request, question_id):
    # response = "You're looking at the results of question %s"
    # return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id, user_id):
    return redirect("detail", question_id, user_id)


"""def vote(request, question_id):
    # return HttpResponse("You're voting on question %s" % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        |||return render(request, 'polls/detail.html', {
            'question': "You didn't select a choice",
        })|||
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('results', args=(question_id,)))  # polls:results"""


def create(request, user_id):
    _user_id = request.session.get("user_id")

    if not _user_id:
        raise ValueError("You are not logged")

    user = User.objects.get(pk=_user_id)

    if not user.id == user_id:
        raise ValueError("You dont have permission")

    if request.method == "POST":
        question_text_input = request.POST["question_text"]
        choice_one_input = request.POST["choice_one"]
        choice_two_input = request.POST["choice_two"]
        choice_three_input = request.POST["choice_three"]

        q = Question(
            user=user, question_text=question_text_input, pub_date=timezone.now()
        )
        q.save()
        q.choice_set.create(choice_text=choice_one_input, votes=0)
        if choice_two_input:
            q.choice_set.create(choice_text=choice_two_input, votes=0)
        if choice_three_input:
            q.choice_set.create(choice_text=choice_three_input, votes=0)

        return HttpResponseRedirect(reverse("home", args=(user.id,)))

    return render(request, "polls/create.html", {"user": user})


# User
def register(request):
    #  user = get_object_or_404(User, pk=user_id)

    try:
        """username_input = User.objects.choice_set.get(pk=request.GET['username'])
        password_input = User.objects.choice_set.get(pk=request.POST['password'])
        user_email_input = User.objects.choice_set.get(pk=request.POST['user_email'])"""
        username_input = request.POST["username"]
        password_input = request.POST["password"]
        user_email_input = request.POST[
            "user_email"
        ]  # trqbva proverka dali nqma sushtestuvasht

    except (KeyError, User.DoesNotExist):
        return render(request, "polls/register.html")
    # return render(request, 'polls/home.html')
    try:
        u = User.objects.get(user_email=user_email_input)
        return render(
            request,
            "polls/register.html",
            {"error_message": "This email is taken Try another"},
        )
    except (KeyError, User.DoesNotExist):
        user = User(
            username=username_input,
            password=password_input,
            user_email=user_email_input,
            is_active=True,
        )
        user.save()
        return HttpResponseRedirect(reverse("home", args=(user.id,)))


def login(request):
    user_email_input = request.POST.get("user_email_login")
    password_input = request.POST.get("password_login")

    try:
        # user = get_object_or_404(User, user_email=user_email_input)
        user = User.objects.get(user_email=user_email_input)
        if user.password == password_input:
            """return render(request, 'polls/home.html', {
                'error_message': "Can't login"
            })"""
            request.session["user_id"] = user.id
            user.save()
            # return render(request, 'polls/home.html', {'user': user})
            return HttpResponseRedirect(reverse("home", args=(user.id,)))
        else:
            return render(
                request,
                "polls/login.html",
                {"error_message": "Can't find user with this email"},
            )
    except (KeyError, User.DoesNotExist):
        return render(request, "polls/login.html", {"error_message": "Login failed"})


def home(request, user_id):
    _user_id = request.session.get("user_id")

    if not _user_id:
        raise ValueError("You are not logged")

    user = User.objects.get(pk=_user_id)

    if not user.id == user_id:
        raise ValueError("You dont have permission")

    user_answers = list(user.answer_set.all())
    open_questions = (
        Question.objects.filter(pub_date__lte=timezone.now())
        .exclude(answer__user_id=user)
        .order_by("-pub_date")
    )

    return render(
        request,
        "polls/home.html",
        {
            "user": user,
            "user_answers": user_answers,
            "open_questions": open_questions,
        },
    )


def result(request, user_id, question_id):
    _user_id = request.session.get("user_id")

    if not _user_id:
        raise ValueError("You are not logged")

    user = User.objects.get(pk=_user_id)

    if not user.id == user_id:
        raise ValueError("You dont have permission")

    question = Question.objects.get(id=question_id)

    try:
        answer = Answer.objects.filter(user_id=user, question_text=question).get()
    except Answer.DoesNotExist:
        answer = None

    return render(
        request,
        "polls/results.html",
        {
            "user": user,
            "question": question,
            "answer": answer,
        },
    )


def logout(request, user_id):
    _user_id = request.session.get("user_id")

    if not _user_id:
        raise ValueError("You are not logged")

    user = User.objects.get(pk=_user_id)

    if not user.id == user_id:
        raise ValueError("You dont have permission")

    del request.session["user_id"]

    return HttpResponseRedirect(reverse("index"))


"""def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)"""


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    # return HttpResponse(template.render(context, request))
    # може и така
    return render(request, "polls/index.html", context)


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


class HomeView(generic.ListView):
    template_name = "polls/home.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]
