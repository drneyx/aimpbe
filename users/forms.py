from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, SellerProfile

class SellerRegistrationForm(UserCreationForm):
    store_name = forms.CharField(max_length=255)
    store_description = forms.CharField(widget=forms.Textarea, required=False)
    store_address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True 

    def clean_phoneno(self):
        phoneno = self.cleaned_data.get('phoneno')
        if not phoneno.isdigit() or len(phoneno) != 10:
            raise forms.ValidationError('Phone number must be 10 digits long.')
        return phoneno

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.is_seller = True
        
        if commit:
            user.save()

            print('User', user.username, user.password)
            SellerProfile.objects.create(
                user=user,
                store_name=self.cleaned_data['store_name'],
                store_description=self.cleaned_data['store_description'],
                store_address=self.cleaned_data['store_address']
            )
        return user
    

class CustomerForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 
            'last_name', 
            'email',
            'is_buyer',
            'is_seller',
        ]