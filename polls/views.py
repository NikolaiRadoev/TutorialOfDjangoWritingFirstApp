from django.shortcuts import get_object_or_404, render, redirect
from django import forms
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.utils import timezone

from .models import Question, User, Answer
from .forms import (
    QuestionChoiceForm,
    CreateNewQuestionForm,
    LoginUserForm,
    RegisterUserForm,
    SetChoiceText,
    ChoiceFormSetBase,
    EditQuestionForm,
)
from django.views import generic
from django.forms import formset_factory


def get_session_user(request):
    user_id = request.session.get("user_id")
    if not user_id:
        raise ValueError("You are not logged or don't have permission")
    else:
        user = User.objects.get(pk=user_id)
        return user


# Create your views here.
# 1
"""def index(request):
    return HttpResponse("Hello, world. You're at the polls index")"""


def detail(request, question_id):
    user = get_session_user(request)

    question = get_object_or_404(Question, pk=question_id)

    form = QuestionChoiceForm(request.POST or None, question=question, user=user)

    if request.method == "POST":
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Nice")
                return redirect("home")
            except forms.ValidationError as e:
                form.add_error(e)

    return render(
        request, "polls/detail.html", {"question": question, "user": user, "form": form}
    )


def create(request):
    user = get_session_user(request)

    extra = 2

    if request.method == "POST":
        extra = int(request.POST["form-TOTAL_FORMS"])

    next_extra = extra + 1
    prev_extra = extra - 1 if extra > 2 else 2

    ChoiceFormSet = formset_factory(
        SetChoiceText, formset=ChoiceFormSetBase, extra=extra, max_num=10
    )
    choice_formset = ChoiceFormSet(request.POST or None)

    form = CreateNewQuestionForm(request.POST or None, user=user)
    if request.method == "POST":
        if request.POST.get("create"):
            # validate the input
            # no +/- buttom has been pressed
            if form.is_valid() and choice_formset.is_valid():
                try:
                    with transaction.atomic():
                        question = form.save()
                        for choice_form in choice_formset.forms:
                            choice_form.save(question)
                        messages.success(request, "New Question Cool")
                        return redirect("home")
                except Exception as e:
                    messages.error(request, "Something Went wrong: %s" % e)

    return render(
        request,
        "polls/create.html",
        {
            "user": user,
            "form": form,
            "extra": extra,
            "next_extra": next_extra,
            "prev_extra": prev_extra,
            "choice_formset": choice_formset,
        },
    )


def my_questions(request):
    user = get_session_user(request)

    my_questions = list(user.question_set.all())

    return render(
        request,
        "polls/edit.html",
        {
            "my_questions": my_questions,
        },
    )


def edit(request, question_id):
    user = get_session_user(request)

    question = get_object_or_404(Question, id=question_id)

    if not question.user_id == user.id:
        raise ValueError("Not your question")

    extra = 0
    inital = question.choice_set.count()

    if request.method == "POST":
        extra = int(request.POST["form-TOTAL_FORMS"]) - inital

    next_extra = inital + (extra + 1)
    prev_extra = inital + (extra - 1 if extra >= 1 else 0)

    ChoiceFormSet = formset_factory(
        SetChoiceText, formset=ChoiceFormSetBase, extra=extra, can_delete=True
    )
    choice_formset = ChoiceFormSet(
        request.POST or None,
        initial=[
            {"id": choice.id, "choice_text": choice.choice_text}
            for choice in question.choice_set.all()
        ],
    )
    form = EditQuestionForm(request.POST or None, user=user, question=question)

    if request.method == "POST":
        if request.POST.get("edit"):
            if form.is_valid() and choice_formset.is_valid():
                form.save()
                choice_formset.save(question)
                messages.success(request, "Edit is successful")
                return redirect(request.build_absolute_uri())

    my_questions = list(user.question_set.all())

    return render(
        request,
        "polls/edit.html",
        {
            "form": form,
            "question": question,
            "my_questions": my_questions,
            "choice_formset": choice_formset,
            "next_extra": next_extra,
            "prev_extra": prev_extra,
        },
    )


# User
def register(request):
    form = RegisterUserForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            """try:
                        # username_input = User.objects.choice_set.get(pk=request.GET['username'])
                        # password_input = User.objects.choice_set.get(pk=request.POST['password'])
                        # user_email_input = User.objects.choice_set.get(pk=request.POST['user_email'])
                        username_input = form.cleaned_data["username"]
                        password_input = form.cleaned_data["password"]
                        user_email_input = form.cleaned_data["email"]
                    except (KeyError, User.DoesNotExist):
                        return render(request, "polls/register.html", {"form": form})
                    # return render(request, 'polls/home.html')
                    try:
                        u = User.objects.get(user_email=user_email_input)
                        return render(
                            request,
                            "polls/register.html",
                            {"error_message": "This email is taken Try another", "form": form},
                        )
                    except (KeyError, User.DoesNotExist):
                        user = User(
                            username=username_input,
                            password=password_input,
                            user_email=user_email_input,
                            is_active=True,
                        )
                        user.save()
                        request.session["user_id"] = user.id
                        return HttpResponseRedirect(reverse("home"))
            else:
                return render(
                    request,
                    "polls/register.html",
                    {"form": form}
                )"""
            try:
                form.save(request)
                messages.success(request, "Your registration is Successful")
                return redirect("home")
            except forms.ValidationError as e:
                form.add_error(e)

    return render(request, "polls/register.html", {"form": form})


def login(request):
    form = LoginUserForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            """user_email_input = form.cleaned_data["email"]
                    password_input = form.cleaned_data["password"]

                    try:
                        # user = get_object_or_404(User, user_email=user_email_input)
                        user = User.objects.get(user_email=user_email_input)
                        if user.password == password_input:
                            request.session["user_id"] = user.id
                            user.save()
                            # return render(request, 'polls/home.html', {'form': form})
                            return HttpResponseRedirect(reverse("home"))
                        else:
                            return render(
                                request,
                                "polls/login.html",
                                {"error_message": "Can't find user with this email",
                                 "form": form},
                            )
                    except (KeyError, User.DoesNotExist):
                        return render(request, "polls/login.html", {"error_message": "Login failed", "form": form})
            else:
                return render(
                    request,
                    "polls/login.html",
                    {"error_message": "Problem with login", "form": form},
                )"""
            try:
                form.save(request)
                messages.success(request, "Welcome back")
                return redirect("home")
            except forms.ValidationError as e:
                form.add_error(e)

    return render(request, "polls/login.html", {"form": form})


def home(request):
    user = get_session_user(request)

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
            "count_of_choices": 1,
        },
    )


def results(request, question_id):
    try:
        user = get_session_user(request)
    except ValueError:
        user = None

    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        question = None

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


def logout(request):
    if get_session_user(request):
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
