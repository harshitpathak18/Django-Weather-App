from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(label='Search City', max_length=100, 
                            widget=forms.TextInput(attrs={
                                'class': 'w-full justify-center border  h-10 shadow p-4 rounded-full text-gray-500 font-medium', 
                                'placeholder':"Search City",
                                'required':True}))