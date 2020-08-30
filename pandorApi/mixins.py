from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied

from .models import ImportantOccasionModel


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class ImportantOccasionMixin(object):
    def get_context_data(self, **kwargs):
        context = super(ImportantOccasionMixin, self).get_context_data(**kwargs)

        context.update({
            'occasions': ImportantOccasionModel.objects.filter(user=self.request.user).order_by('-occasion_date'),
        })

        return context

    def check_user_or_403(self, user):
        """ Issue a 403 if the current user is no the same as the `user` param. """
        if self.request.user != user:
            raise PermissionDenied