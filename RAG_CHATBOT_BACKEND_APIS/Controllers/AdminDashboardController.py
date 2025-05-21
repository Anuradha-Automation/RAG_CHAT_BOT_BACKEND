import logging
import traceback
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib import messages
from RAG_CHATBOT_BACKEND_APIS.models import Country
from RAG_CHATBOT_BACKEND_APIS.services.AdminAuthServices import AuthServices

logger = logging.getLogger('myapp')

class AdminDashboardController:
    
    @method_decorator(login_required(login_url='/login/'))
    def SettingProfileAccount(self, request, user_uuid):
        """
        Handles the account settings page, including updating user details.
        """
        logger.debug(f"Entering SettingProfileAccount with user_uuid: {user_uuid}")
        country_list = Country.objects.all()  # Fetch all records with all fields
        logger.debug(f"Queried country list: {list(country_list)}")
        
        login_user_uuid = request.user.uuid
        logger.debug(f"Logged-in user UUID: {login_user_uuid}")

        if request.method == "POST":
            logger.debug(f"Processing POST request with data: {request.POST}, files: {request.FILES}")
            form_data = request.POST
            profile_data = request.FILES
            if AuthServices.check_user_existence('uuid', login_user_uuid):
                logger.debug(f"User exists, updating details for UUID: {login_user_uuid}")
                status, response = AuthServices.UpdateUser_Details(login_user_uuid, form_data, profile_data)
                logger.debug(f"UpdateUser_Details response - status: {status}, response: {response}")
                if not status:
                    messages.error(request, "Something Is Wrong")
                    logger.error(f"Failed to update user details for UUID: {login_user_uuid}, response: {response}")
                else:
                    messages.success(request, response)
                    logger.info(f"Successfully updated user details for UUID: {login_user_uuid}")
                return redirect(f"/dashboard/profile/{login_user_uuid}/setting-account/")
            else:
                messages.error(request, "Something Is Wrong")
                logger.error(f"User with UUID {login_user_uuid} does not exist")
                return redirect("/login/")
        context = {"country_list": country_list, "user": request.user}
        logger.debug(f"Rendering accountSetting.html with context: {context}")
        return render(request, "admin/auth/profile/accountSetting.html", context)
    
    @method_decorator(login_required(login_url='/login/'))
    def SettingProfileSercurity(self, request, user_uuid):
        """
        Handles the security settings page, including password changes.
        """
        logger.debug(f"Entering SettingProfileSercurity with user_uuid: {user_uuid}")
        login_user_uuid = request.user.uuid
        logger.debug(f"Logged-in user UUID: {login_user_uuid}")

        if request.method == 'POST':
            logger.debug(f"Processing POST request with data: {request.POST}")
            form_data = request.POST
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            logger.debug(f"Password change attempt - old: {old_password}, new: {new_password}, confirm: {confirm_password}")
            
            user = request.user  # Get the currently logged-in user
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match!")
                logger.error("Password change failed: New password and confirm password do not match")
                return redirect(f"/dashboard/profile/{login_user_uuid}/setting-security/")
            elif user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password changed successfully!")
                logger.info(f"Password changed successfully for user UUID: {login_user_uuid}")
                return redirect("/login/")
            else:
                messages.error(request, "Old password is incorrect")
                logger.error("Password change failed: Old password is incorrect")
                return redirect(f"/dashboard/profile/{login_user_uuid}/setting-security/")
        logger.debug("Rendering change_password.html")
        return render(request, "admin/auth/profile/change_password.html")

    @method_decorator(login_required(login_url='/login/'))
    def admin_dashboard_page(self, request):
        """
        Renders the admin dashboard page.
        """
        logger.info("Admin dashboard page accessed by user: %s", request.user)
        try:
            logger.debug("Rendering admin_dashboard.html")
            return render(request, "admin/admin_dashboard.html")
        except Exception as e:
            logger.error("Error loading admin dashboard: %s\n%s", str(e), traceback.format_exc())
            return redirect("error_page")  # Redirect to an error page if needed