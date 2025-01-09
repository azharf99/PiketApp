from django import forms


class UploadModelForm(forms.Form):
    file = forms.FileField(
        max_length=50,
        allow_empty_file=False,
        required=True,
        widget=forms.FileInput(
            attrs={
                "class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"
            }
        ),
    )