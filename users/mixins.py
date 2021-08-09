from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect,reverse
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin

class LoggedOutOnlyView(UserPassesTestMixin):

    permission_denied_message = "Page Not Found"
    def test_func(self):
        return not self.request.user.is_authenticated
    def handle_no_permission(self):
        messages.error(self.request,"Your are already logged in.")
        return redirect("core:event")

class EmailLoginOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.login_method == "github" or "email"

    def handle_no_permission(self):
        messages.error(self.request,"Can't go there")
        return redirect("core:event")


class LogInOnlyView(LoginRequiredMixin):
    
    login_url = reverse_lazy("users:login")