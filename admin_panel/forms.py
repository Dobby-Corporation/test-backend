from django import forms

class CreateTestForm(forms.Form):
    name = forms.CharField(label="Название теста", max_length=100)
    description = forms.CharField(label="Описание", max_length=100)
    json_file = forms.FileField(label="Содержание")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control mb-2'
        # self.json_file.widget.attrs['enctype'] = "multipart/form-data"
