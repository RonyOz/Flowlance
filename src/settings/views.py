from discord import User
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext as _

from flowlance.decorators import attach_profile_info
from profile.models import ProfileConfiguration


@login_required
def settings(request):
    section = "account"
    return render(request, "settings/account_settings.html", {"section": section})

@login_required
def security_settings(request):
    user = request.user
    profile, profile_type = user.get_profile_info()  # Use the get_profile_info method
    # Check if profile exists and handle the case when it's None
    if profile:
        has_2FA_on = profile.has_2FA_on
    else:
        has_2FA_on = False  # Default value if no profile is found

    return render(request, "settings/security_settings.html", {"has_2FA_on": has_2FA_on, "section": "security"})

@login_required
def account_settings(request):
    return render(request, "settings/account_settings.html", {"section": "account"})

@login_required
def notification_settings(request):
    user = request.user
    profile, profile_type = user.get_profile_info()

    if profile:
        periodicity_of_notification_report = profile.profileconfiguration.periodicity_of_notification_report
        has_notification_when_profile_visited = profile.profileconfiguration.notification_when_profile_visited
        has_sending_notification_to_email = profile.profileconfiguration.sending_notification_to_email
    else:
        periodicity_of_notification_report = ProfileConfiguration.Periodicity.DAILY

    return render(request, "settings/notification_settings.html", {"section": "notification", "periodicity_of_notification_report": periodicity_of_notification_report, "has_notification_when_profile_visited": has_notification_when_profile_visited, "has_sending_notification_to_email": has_sending_notification_to_email})

@login_required
def chat_settings(request):
    return render(request, "settings/chat_settings.html", {"section": "chat"})

@login_required
def toggle_2fa(request):
    user = request.user
    profile, profile_type = user.get_profile_info()  # Use the get_profile_info method

    if request.method == 'POST':
        has_2FA_on = request.POST.get('has_2FA_on') == 'on'
        if profile:  # If the user has a profile (either Freelancer or Company)
            profile.has_2FA_on = has_2FA_on
            profile.save()

        return redirect('security_settings')  # Redirect to the profile page or another relevant page


@login_required
def toggle_notification_when_profile_visited(request):
    user = request.user
    profile, profile_type = user.get_profile_info()  # Use the get_profile_info method

    if request.method == 'POST':
        notification_when_profile_visited_variable = request.POST.get('notification_when_profile_visited_variable') == 'on' #esto se lo deberias pasar desde la form, para ver si lo quiere activar o no
        if profile:  # If the user has a profile (either Freelancer or Company)
            profile.profileconfiguration.notification_when_profile_visited = notification_when_profile_visited_variable
            profile.profileconfiguration.save()

        return redirect('notification_settings')  # Redirect to the profile page or another relevant page

@login_required
def toggle_notification_to_email(request):
    user = request.user
    profile, profile_type = user.get_profile_info()  # Use the get_profile_info method

    if request.method == 'POST':
        sending_notification_to_email_variable = request.POST.get('sending_notification_to_email_variable') == 'on' #esto se lo deberias pasar desde la form, para ver si lo quiere activar o no
        if profile:  # If the user has a profile (either Freelancer or Company)
            profile.profileconfiguration.sending_notification_to_email = sending_notification_to_email_variable
            profile.profileconfiguration.save()

        return redirect('notification_settings')  # Redirect to the profile page or another relevant page

@login_required
def change_periodicity_of_notifications_reports(request):
    if request.method == 'POST':
        profile, profile_type = request.user.get_profile_info()
        new_periodicity = request.POST.get('new_periodicity')

        # Validate that the new periodicity is a valid choice
        if new_periodicity in ProfileConfiguration.Periodicity.values:
            profile.profileconfiguration.periodicity_of_notification_report = new_periodicity
            profile.profileconfiguration.save()
            messages.success(request, _("The periodicity of notification reports has been updated."))
        else:
            messages.error(request, _("Invalid periodicity choice."))

        return redirect('notification_settings') 

    return redirect('notification_settings')


@login_required
def information(request):
    return render(request, "settings/information.html")