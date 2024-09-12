from django import forms
from .models import Member, Message
from django.contrib.auth.hashers import make_password

class MembershipAccountForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['username', 'first_name', 'last_name', 'other_name', 'address', 'contact', 'image', 'password']

    def save(self, commit=True):
        member = super(MembershipAccountForm, self).save(commit=False)
        member.password = make_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            member.save()
        return member
    

class MemberCreateForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = ('__all__')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit recipients to admins only
        self.fields['recipient'].queryset = Member.objects.filter(is_staff=True, is_superuser=True)

        # Adding Bootstrap classes to the form fields
        self.fields['recipient'].widget.attrs.update({'class': 'form-control'})
        self.fields['subject'].widget.attrs.update({'class': 'form-control'})
        self.fields['body'].widget.attrs.update({'class': 'form-control', 'rows': 5})

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Write your reply here...'
            }),
        }


class MembershipAccountEditForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['username', 'first_name', 'last_name', 'other_name', 'address', 'contact', 'password', 'image']
        widgets = {
            'password': forms.PasswordInput(),  # Use PasswordInput to hide password text
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Only generate a random password if it's not valid and empty, otherwise leave it as is
        if password and not password.startswith('pbkdf2_sha256$'):
            return password  # Return the new password for hashing in the view
        return password



class StaffAccountEditForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['username', 'first_name', 'last_name', 'other_name', 'address', 'contact', 'password', 'image', 'is_staff', 'is_superuser']
        widgets = {
            'password': forms.PasswordInput(),  # Hide password input
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Only generate a random password if it's not valid and empty, otherwise return the entered password
        if password and not password.startswith('pbkdf2_sha256$'):
            return password  # Return new password for hashing in the view
        return password