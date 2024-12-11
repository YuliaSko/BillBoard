from board.models import User
from django.shortcuts import redirect, render
from django.views.generic import UpdateView, CreateView, View
from users.forms import CommonSignupForm
# from .forms import BaseRegisterForm


# class RegisterView(CreateView):
#     # User = get_user_model()
#     model = User
#     form_class = CommonSignupForm
#     success_url = reverse_lazy('activate_account')
#
#     def form_valid(self, form):
#         form.save(request=self.request)
#         return super().form_valid(form)


class ActivateAccount(UpdateView):
    model = User
    context_object_name = 'activate_account'

    def post(self,  request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, 'account/invalid_code.html')
            return redirect('/')

