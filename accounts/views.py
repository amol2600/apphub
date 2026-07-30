from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from .email_utils import send_brevo_email
from django.template.loader import render_to_string
from django.conf import settings


def signup(request):

    if request.user.is_authenticated:

        return redirect("transaction_list")

    if request.method == "POST":

        username = request.POST["username"].strip()
        email = request.POST["email"].strip()
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        context = {
            "username": username,
            "email": email,
        }

        # ==========================
        # Password Match
        # ==========================
        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match.",
            )

            return render(
                request,
                "accounts/signup.html",
                context,
            )

        # ==========================
        # Username Exists
        # ==========================
        if User.objects.filter(
            username=username,
        ).exists():

            messages.error(
                request,
                "Username already exists.",
            )

            return render(
                request,
                "accounts/signup.html",
                context,
            )

        # ==========================
        # Email Exists
        # ==========================
        if User.objects.filter(
            email=email,
        ).exists():

            messages.error(
                request,
                "Email is already registered.",
            )

            return render(
                request,
                "accounts/signup.html",
                context,
            )

        # ==========================
        # Password Validation
        # ==========================
        try:

            temp_user = User(
                username=username,
                email=email,
            )

            validate_password(
                password,
                user=temp_user,
            )

        except ValidationError as e:

            for message in e.messages:

                messages.error(
                    request,
                    message,
                )

            return render(
                request,
                "accounts/signup.html",
                context,
            )

        # ==========================
        # Create Inactive User
        # ==========================
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        user.is_active = False

        user.save()

        # ==========================
        # Generate Verification Token
        # ==========================
        uidb64 = urlsafe_base64_encode(
            force_bytes(user.pk)
        )

        token = default_token_generator.make_token(
            user
        )

        verification_link = request.build_absolute_uri(
            reverse(
                "activate_account",
                kwargs={
                    "uidb64": uidb64,
                    "token": token,
                },
            )
        )

        # ==========================
        # Email Context
        # ==========================
        email_context = {
            "user": user,
            "verification_link": verification_link,
        }

        subject = render_to_string(
            "accounts/verification_subject.txt",
            email_context,
        ).strip()

        text_content = render_to_string(
            "accounts/verification_email.txt",
            email_context,
        )

        html_content = render_to_string(
            "accounts/verification_email.html",
            email_context,
        )

        send_brevo_email(
            subject=subject,
            text_content=text_content,
            html_content=html_content,
            recipient_email=user.email,
        )

        messages.success(
            request,
            "Account created successfully. Please check your email to verify your account before logging in.",
        )

        return redirect("login")

    return render(
        request,
        "accounts/signup.html",
    )

def activate_account(request, uidb64, token):

    try:

        uid = force_str(
            urlsafe_base64_decode(uidb64)
        )

        user = User.objects.get(pk=uid)

    except (
        TypeError,
        ValueError,
        OverflowError,
        User.DoesNotExist,
    ):

        user = None

    if (
        user is not None
        and default_token_generator.check_token(
            user,
            token,
        )
    ):

        user.is_active = True

        user.save()

        return render(
            request,
            "accounts/verification_success.html",
        )

    return render(
        request,
        "accounts/verification_failed.html",
    )


def login_view(request):

    if request.user.is_authenticated:

        return redirect("transaction_list")

    if request.method == "POST":

        username = request.POST["username"].strip()
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:

            login(
                request,
                user,
            )

            messages.success(
                request,
                f"Welcome back, {user.username}!",
            )

            return redirect("transaction_list")

        try:

            existing_user = User.objects.get(
                username=username,
            )

            if not existing_user.is_active:

                messages.error(
                    request,
                    "Please verify your email before logging in.",
                )

            else:

                messages.error(
                    request,
                    "Invalid username or password.",
                )

        except User.DoesNotExist:

            messages.error(
                request,
                "Invalid username or password.",
            )

    return render(
        request,
        "accounts/login.html",
    )

@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully.",
    )

    return redirect("login")