
from django.shortcuts import redirect
from django.views import View


class HomePageView(View):
    def get(self, request):
        return redirect('swagger')
