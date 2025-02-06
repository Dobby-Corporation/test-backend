from django import forms

class TestForm(forms.Form):
    name = forms.CharField(label="Название теста", max_length=100)
    description = forms.CharField(label="Описание", max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control mb-2'

class CreateTestForm(TestForm):
    json_file = forms.FileField(label="Содержание")

class EditTestForm(TestForm):
    json_file = forms.FileField(label="Содержание", required=False)
