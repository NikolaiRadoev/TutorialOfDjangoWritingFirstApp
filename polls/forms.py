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
