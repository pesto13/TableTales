from django.contrib.auth.mixins import UserPassesTestMixin


class LoginRequiredMixin(UserPassesTestMixin):
    def __init__(self):
        self.request = None

    def test_func(self):
        return self.request.user.is_authenticated
