from django import forms

class AddMessageForm(forms.Form):
    message = forms.CharField(required=True,widget=forms.TextInput(attrs={"placeholder":"Write a message...",'class':"msg-box"}))