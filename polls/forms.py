from django import forms
from django.db import transaction
from .models import Question, User, Answer, Choice
from django.utils.translation import gettext_lazy
from django.forms import ModelForm
from django.forms import formset_factory, inlineformset_factory
from django.utils import timezone


class QuestionChoiceForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop("question")
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        # self.fields["insert_1"] = forms.CharField()
        self.fields["choice_id"] = forms.ChoiceField(
            widget=forms.RadioSelect,
            choices=[(choice.id, str(choice)) for choice in self.question.choice_set.all()],
        )

    """def clean_insert_1(self):
        if not self.cleaned_data["insert_1"] == "1":
            raise forms.ValidationError("You have forgotten 1!")

        return self.cleaned_data["insert_1"]"""
    def clean(self):
        cleaned_data = super(QuestionChoiceForm, self).clean()
        choice_id = cleaned_data["choice_id"]

        try:
            selected_choice = self.question.choice_set.get(pk=choice_id)
        except Exception as e:
            raise forms.ValidationError({"choice_id": "Choice not found %s" % e})

        cleaned_data["selected_choice"] = selected_choice
        return cleaned_data

    def save(self):
        try:
            with transaction.atomic():
                selected_choice = self.cleaned_data["selected_choice"]
                selected_choice.votes += 1
                selected_choice.save()
                answer = Answer(user_id=self.user, is_vote=True, choice_text=selected_choice, question_text=self.question)
                answer.save()
        except Exception as e:
            raise forms.ValidationError({None: "An Unexpected error %s " % e})


class CreateNewQuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        # self.q = object
        self.formset = kwargs.pop("formset")
        super().__init__(*args, **kwargs)
        """self.fields["question_text"] = forms.CharField(label='Name of the question',
                                                       max_length=100,
                                                       widget=forms.TextInput(
                                                           attrs={'placeholder': 'Enter question name'}))
        self.fields["choice_one"] = forms.CharField(label='Name of choice',
                                                    widget=forms.TextInput(attrs={'placeholder': 'Enter your choice'}),
                                                    max_length=100)
        self.fields["choice_two"] = forms.CharField(label="Name of choice",
                                                    max_length=100,
                                                    required=None,
                                                    widget=forms.TextInput(attrs={'placeholder': 'Enter your choice'}))
        self.fields["choice_three"] = forms.CharField(label="Name of choice",
                                                      max_length=100,
                                                      required=None,
                                                      widget=forms.TextInput(attrs={'placeholder': 'Enter your choice'}))"""
        self.fields["question_text"] = forms.CharField(label='Name of the question',
                                                       max_length=100,
                                                       widget=forms.TextInput(
                                                           attrs={'placeholder': 'Enter question name'}))
        # self.fields["count_of_choices"] = forms.IntegerField(min_value=1, max_value=12, initial=1)

        # self.fields["choice_text"] = forms.CharField(max_length=100)

    def clean(self):
        cleaned_data = super(CreateNewQuestionForm, self).clean()
        return cleaned_data

    def save(self):
        question_text = self.cleaned_data["question_text"]
        q = Question(user=self.user, question_text=question_text, pub_date=timezone.now())
        q.save()
        for form in self.formset:
            q.choice_set.create(choice_text=form.fields["choice"], votes=0)


class SetChoiceText(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["choice"] = forms.CharField(label='Name of Choice', max_length=100,
                                                widget=forms.TextInput(
                                                           attrs={'placeholder': 'Enter choice'}))


class LoginUserForm(ModelForm):
    """def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"] = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
                                               max_length=100)
        self.fields["password"] = forms.CharField(
            widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
            max_length=100)"""
    class Meta:
        model = User
        exclude = ['username', 'is_active']
        labels = {'user_email': 'Email'}
        #  help_texts = {'user_email': 'Enter valid email address'}
        widgets = {
            'password': forms.PasswordInput(),
            'user_email': forms.EmailInput(),
        }

    def clean(self):
        cleaned_data = super(LoginUserForm, self).clean()
        user_email_input = cleaned_data["user_email"]
        password_input = cleaned_data["password"]

        try:
            #  user = get_object_or_404(User, user_email=user_email_input)
            user = User.objects.get(user_email=user_email_input)
            if user.password == password_input:
                return cleaned_data
            else:
                raise forms.ValidationError("Incorrect password")

        except (KeyError, User.DoesNotExist):
            raise forms.ValidationError("Incorrect email")

    def save(self, request):
        user_email_input = self.cleaned_data["user_email"]
        user = User.objects.get(user_email=user_email_input)
        request.session["user_id"] = user.id


class RegisterUserForm(ModelForm):  # forms.Form
    """def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"] = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}),
                                                  max_length=100)
        self.fields["password"] = forms.CharField(
            widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
            max_length=100)
        self.fields["email"] = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
                                               max_length=100)"""
    class Meta:
        model = User
        #  fields = ['username', 'password', 'email']
        exclude = ['is_active']
        labels = {'user_email': 'Email'}
        widgets = {
            'password': forms.PasswordInput(),
            'user_email': forms.EmailInput(),
        }

    def clean(self):
        cleaned_data = super(RegisterUserForm, self).clean()
        username_input = cleaned_data["username"]
        password_input = cleaned_data["password"]
        user_email_input = cleaned_data["user_email"]

        try:
            u = User.objects.get(user_email=user_email_input)
            raise forms.ValidationError("email is taken")
        except User.DoesNotExist:
            return cleaned_data

    def save(self, request):
        username_input = self.cleaned_data["username"]
        password_input = self.cleaned_data["password"]
        user_email_input = self.cleaned_data["user_email"]

        user = User(
            username=username_input,
            password=password_input,
            user_email=user_email_input,
            # is_active=True,
        )
        user.save()
        request.session["user_id"] = user.id
