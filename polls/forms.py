from django import forms


class QuestionChoiceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop("question")
        super().__init__(*args, **kwargs)
        self.fields["insert_1"] = forms.CharField()
        self.fields["choice"] = forms.ChoiceField(
            widget=forms.RadioSelect,
            choices=[(choice.id, str(choice)) for choice in question.choice_set.all()],
        )

    def clean_insert_1(self):
        if not self.cleaned_data["insert_1"] == "1":
            raise forms.ValidationError("You have forgotten 1!")

        return self.cleaned_data["insert_1"]


class CreateNewQuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["question_text"] = forms.CharField(label='Name of the question',
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
                                                      widget=forms.TextInput(attrs={'placeholder': 'Enter your choice'}))


class LoginUserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"] = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
                                               max_length=100)
        self.fields["password"] = forms.CharField(
            widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
            max_length=100)


class RegisterUserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"] = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}),
                                                  max_length=100)
        self.fields["password"] = forms.CharField(
            widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
            max_length=100)
        self.fields["email"] = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
                                               max_length=100)
