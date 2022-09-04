from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.forms import SignupForm
from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import (
    get_account_adapter,
    DefaultSocialAccountAdapter,
)
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms
from django.contrib.sites.models import Site
from django.core.mail import mail_admins
from stravalib.client import Client

from main.utils import create_update_athlete


class DeactivateAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_email, user_field, user_username

        data = form.cleaned_data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("username")
        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name", last_name)
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)

        if commit:
            # Deactivate the account
            user.is_active = False
            send_user_activation_email(user)

            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()

            # Create an Athlete
            sex = None
            dob = None
            if "sex" in data:
                sex = data["sex"]
            if "dob" in data:
                dob = data["dob"]
            create_update_athlete(
                user=user,
                sex=sex,
                dob=dob,
            ),

        return user


class DeactivateSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        """
        Saves a newly signed up social login. Accounts are disabled by default.
        """
        u = sociallogin.user
        u.set_unusable_password()
        if form:
            get_account_adapter().save_user(request, u, form, commit=False)
        else:
            get_account_adapter().populate_username(request, u)

        # Deactivate the account unless they are in the RRR Strava Club
        u.is_active = False
        if sociallogin.token.app.name == "Strava":
            client = Client()
            client.access_token = sociallogin.token.token
            client.refresh_token = sociallogin.token.token_secret
            client.token_expires_at = sociallogin.token.expires_at
            clubs = client.get_athlete_clubs()
            for club in clubs:
                if club.id == 7686:
                    u.is_active = True
                    break

        if not u.is_active:
            send_user_activation_email(u)

        sociallogin.save(request)

        # Create an Athlete
        if sociallogin.account.extra_data:
            sex = None
            photo = None
            dob = None
            if form and "dob" in form.cleaned_data:
                dob = form.cleaned_data["dob"]
            if (
                "sex" in sociallogin.account.extra_data
                and sociallogin.account.extra_data["sex"] in ["F", "M"]
            ):
                sex = sociallogin.account.extra_data["sex"]
            if "profile" in sociallogin.account.extra_data:
                photo = sociallogin.account.extra_data["profile"]
        create_update_athlete(
            user=u,
            sex=sex,
            photo_url=photo,
            dob=dob,
        )

        return u


class AccountSignupForm(SignupForm):
    first_name = forms.CharField(max_length=150, label="First Name")
    last_name = forms.CharField(max_length=150, label="Last Name")
    SEX_CHOICES = [("F", "Female"), ("M", "Male")]
    sex = forms.ChoiceField(choices=SEX_CHOICES, label="Sex")
    dob = forms.DateField(label="Date of Birth")

    # Send verification email even though we initially deactivate accounts
    def save(self, request):
        user = super(AccountSignupForm, self).save(request)
        email_address = EmailAddress.objects.get_primary(user)
        email_address.send_confirmation()
        return user


class SocialAccountSignupForm(SocialSignupForm):
    dob = forms.DateField(label="Date of Birth")


def send_user_activation_email(user):
    site = Site.objects.get_current()

    message_text = (
        f"A new user has signed up to {site.name} with email address {user.email} and needs activation. "
        f'Please go to https://{site.domain}/admin/auth/user/ and set them to "Active" '
        "after verifying that they are a member of the club. \n\n"
        "When you have done this you will need to email them to inform them that their account is now "
        "active, as this is not automated."
    )
    mail_admins(
        f"User {user.first_name} {user.last_name} needs manual activation", message_text
    )
