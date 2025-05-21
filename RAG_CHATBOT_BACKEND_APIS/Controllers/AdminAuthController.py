import logging
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, render
from django.contrib.auth import logout, authenticate, login
from RAG_CHATBOT_BACKEND_APIS.models import CustomUser
from RAG_CHATBOT_BACKEND_APIS.services.AdminAuthServices import AuthServices
from RAG_CHATBOT_BACKEND_APIS.utils import get_base_url
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger("auth")

class AuthController:
    def auth_register_page(self, request):
        if request.method == "POST":
            base_url = get_base_url(request)
            username = request.POST.get("username", "").strip()
            email = request.POST.get("email", "").strip()
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")

            print(f"Register request: username={username}, email={email}")
            logger.debug(f"Register request received for username: {username}, email: {email}")

            if not all([username, email, password1, password2]):
                messages.error(request, "All fields are required.")
                logger.warning("Registration failed: Missing fields.")
            elif password1 != password2:
                messages.error(request, "Passwords do not match!")
                logger.warning("Registration failed: Passwords do not match.")
            elif AuthServices.check_user_existence("username", username):
                messages.error(request, "Username is already taken.")
                logger.warning(f"Registration failed: Username {username} already exists.")
            elif AuthServices.check_user_existence("email", email):
                messages.error(request, "Email is already registered.")
                logger.warning(f"Registration failed: Email {email} already registered.")
            else:
                status, message = AuthServices.RegisterUser(username, email, password1, base_url)
                print(f"User registration status: {status}, message: {message}")
                if not status:
                    messages.error(request, message)
                    logger.error(f"User registration failed for {email}: {message}")
                else:
                    messages.success(request, message)
                    logger.info(f"User registered successfully: {email}")
                    return redirect("/login/")
            return redirect("/register/")
        
        return render(request, "admin/auth/register.html")
    
    def auth_login_page(self, request):
        if request.method == "POST":
            username_or_address = request.POST.get("username_or_address", "").strip()
            password = request.POST.get("password")

            print(f"Login attempt: {username_or_address}")
            logger.info(f"Login attempt for: {username_or_address}")

            if AuthServices.check_user_existence("email", username_or_address):
                user = AuthServices.fetch_user_data("email", username_or_address)
                username = user.username  # type: ignore
            else:
                username = username_or_address
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login Successfully")
                logger.info(f"User logged in successfully: {username}")
                return redirect("/dashboard/")
            else:
                messages.error(request, "Invalid username/email or password.")
                logger.warning(f"Login failed for: {username_or_address}")
                return redirect("/login/")
        
        return render(request, "admin/auth/login.html")
    
    @csrf_exempt
    def forget_password_page(self, request):
        if request.method == "POST":
            email = request.POST.get("email")
            user = CustomUser.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(reverse("reset_password", kwargs={"uidb64": uid, "token": token}))

                print(f"Generated reset link: {reset_link}")
                logger.debug(f"Password reset link generated for {email}: {reset_link}")
                
                send_mail(
                    subject="Password Reset Request",
                    message=f"Click the link to reset your password: {reset_link}",
                    from_email="pythonweb@exoticaitsolutions.com",
                    recipient_list=[email],
                    fail_silently=False,
                )

                messages.success(request, "Password reset link sent to your email.")
                return redirect(reset_link)  
            else:
                messages.error(request, "Invalid email address.")
                return redirect("/forget-password/")

        return render(request, "admin/auth/forgetpasswordpage.html")
    
    def reset_password_page(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if request.method == "POST":
                new_password = request.POST.get("password")
                confirm_password = request.POST.get("confirm_password")

                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Password reset successfully. Please log in.")
                    return redirect(reverse("login"))
                else:
                    messages.error(request, "Passwords do not match.")
                    return render(request, "admin/auth/resetpasswordpage.html", {"validlink": True, "uid": uidb64, "token": token})

            return render(request, "admin/auth/resetpasswordpage.html", {"validlink": True, "uid": uidb64, "token": token})
        else:
            messages.error(request, "The password reset link is invalid or expired.")
            return redirect(reverse("forget_password"))

    def auth_logoutSession(self, request):
        username = request.user.username if request.user.is_authenticated else "Anonymous"
        logout(request)
        messages.success(request, "Logout Successfully")
        request.session.flush()
        print(f"User logged out: {username}")
        logger.info(f"User logged out: {username}")
        return redirect("/login/")
