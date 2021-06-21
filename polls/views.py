from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.utils import timezone

from .models import Choice, Question, User, Answer
from django.views import generic

# Create your views here.
# 1
"""def index(request):
    return HttpResponse("Hello, world. You're at the polls index")"""


def detail(request, question_id, user_id):
    # return HttpResponse("You're looking at question %s" % question_id)
    #     question = get_object_or_404(Question, pk=question_id)
    #     return render(request, 'polls/detail.html', {'question': question}) # може и така
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    # response = "You're looking at the results of question %s"
    # return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id, user_id):
    # return HttpResponse("You're voting on question %s" % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        user = User.objects.get(id=user_id)
    except (KeyError, Choice.DoesNotExist):
        """return render(request, 'polls/detail.html', {
            'question': "You didn't select a choice",
        })"""
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        answer = Answer(user_id=user, is_vote=True, choice_text=selected_choice, question_text=question)
        answer.save()
    return HttpResponseRedirect(reverse('results', args=(question_id,)))  # polls:results


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
    try:
        question_text_input = request.POST['question_text']
        choice_one_input = request.POST['choice_one']
        choice_two_input = request.POST['choice_two']
        choice_three_input = request.POST['choice_three']

        user = User.objects.get(id=user_id)

        q = Question(user=user, question_text=question_text_input, pub_date=timezone.now())
        q.save()
        q.choice_set.create(choice_text=choice_one_input, votes=0)
        if choice_two_input != '':
            q.choice_set.create(choice_text=choice_two_input, votes=0)
        if choice_three_input != '':
            q.choice_set.create(choice_text=choice_three_input, votes=0)
    except (KeyError, Question.DoesNotExist):
        return render(request, 'polls/create.html')
    return HttpResponseRedirect(reverse('home', args=(user_id,)))


# User
def register(request):
    #  user = get_object_or_404(User, pk=user_id)

    try:
        """username_input = User.objects.choice_set.get(pk=request.GET['username'])
        password_input = User.objects.choice_set.get(pk=request.POST['password'])
        user_email_input = User.objects.choice_set.get(pk=request.POST['user_email'])"""
        username_input = request.POST['username']
        password_input = request.POST['password']
        user_email_input = request.POST['user_email']  # trqbva proverka dali nqma sushtestuvasht
        user = User(username=username_input, password=password_input, user_email=user_email_input, is_active=True)
        user.save()
    except (KeyError, User.DoesNotExist):
        return render(request, 'polls/register.html', {
            'error_message': "Please enter your data below"
        })
    # return render(request, 'polls/home.html')
    return HttpResponseRedirect(reverse('home', args=(user.id,)))


def login(request):
    user_email_input = request.POST.get('user_email_login')
    password_input = request.POST.get('password_login')

    try:
        # user = get_object_or_404(User, user_email=user_email_input)
        user = User.objects.get(user_email=user_email_input)
        if user.password == password_input:
            """return render(request, 'polls/home.html', {
                'error_message': "Can't login"
            })"""
            user.is_active = True
            user.save()
            # return render(request, 'polls/home.html', {'user': user})
            return HttpResponseRedirect(reverse('home', args=(user.id,)))
        else:
            return render(request, 'polls/login.html', {
                'error_message': "Can't find user with this email"
            })
    except(KeyError, User.DoesNotExist):
        return render(request, 'polls/login.html', {
            'error_message': "Login failed"
        })


def home(request, user_id):
    latest_question_list = list()
    voted_question_list = list()
    questions = Question.objects.all()
    #  choices = questions.choice_set.all()
    user = User.objects.get(id=user_id)

    if not user.is_active:
        return render(request, 'polls/login.html')
    else:
        for question in questions:
            latest_question_list.insert(0, question)
        answers = Answer.objects.filter(user_id=user)
        for answer in answers:
            if latest_question_list.__contains__(answer.question_text):
                voted_question_list.insert(0, answer.question_text)
                latest_question_list.remove(answer.question_text)

        """try:
        answers = Answer.objects.filter(user_id=user)
        for question in questions:
            for answer in answers:
                #  for choice in question.choice_set.all():
                    if question == answer.question_text:
                        if answer.is_vote:
                            voted_question_list.insert(0, question)
                            break
                    else:
                        if not latest_question_list.__contains__(question):
                            latest_question_list.insert(0, question)
                        break
    except(KeyError, Answer.DoesNotExist):
        return render(request, 'polls/home.html', {
            'latest_question_list': latest_question_list,
            'user': user,
            'voted_question_list': voted_question_list,
        })"""
        return render(request, 'polls/home.html', {
            'latest_question_list': latest_question_list,
            'user': user,
            'voted_question_list': voted_question_list,
            })


def result(request, user_id, question_id):
    question = Question.objects.get(id=question_id)
    user = User.objects.get(id=user_id)
    answer = Answer.objects.filter(user_id=user, question_text=question)
    selected_choice = ''
    for ans in answer:
        selected_choice = ans.choice_text
    return render(request, 'polls/results.html', {
        'selected_choice': selected_choice,
        'question': question,
    })


def logout(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return HttpResponseRedirect(reverse('index'))


"""def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)"""


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    # return HttpResponse(template.render(context, request))
    # може и така
    return render(request, 'polls/index.html', context)


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


class HomeView(generic.ListView):
    template_name = 'polls/home.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
