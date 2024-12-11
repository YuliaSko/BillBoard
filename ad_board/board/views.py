import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.mail import send_mail
from django.http import HttpResponseForbidden, JsonResponse

from ad_board import settings
from .forms import *
from .models import *
from .filters import *

logger = logging.getLogger(__name__)


class HomePageView(ListView):
    model = Ad
    ordering = '-date'
    template_name = 'home.html'
    context_object_name = 'ad_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = Ad.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AdView(DetailView):
    model = Ad
    template_name = 'ad_detail.html'
    context_object_name = 'ad'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Ad, pk=self.kwargs['pk'])
        return obj

    def get_queryset(self):
        category = self.kwargs.get('pk')
        queryset = Ad.objects.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['response'] = AdResponse.objects.filter(ad_response=self.object)
        return context


class AdSearch(ListView):
    model = Ad
    ordering = '-date'
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class AdCreate(LoginRequiredMixin, CreateView):
    form_class = AdCreateForm
    model = Ad
    template_name = 'ad_create.html'

    def form_valid(self, form):
        ad = form.save(commit=False)
        ad.ad_user = self.request.user
        ad.save()
        return super().form_valid(form)


class AdUpdate(LoginRequiredMixin, UpdateView):
    form_class = AdCreateForm
    model = Ad
    template_name = 'ad_edit.html'
    context_object_name = 'search'


class AdDelete(LoginRequiredMixin, DeleteView):
    model = Ad
    template_name = 'ad_delete.html'
    success_url = reverse_lazy('home')
    context_object_name = 'delete'


class CategoryAdList(HomePageView):
    model = Ad
    template_name = 'category_ads_list.html'
    context_object_name = 'category_ads_list'

    def get_queryset(self):
        category = self.kwargs.get('pk')
        queryset = Ad.objects.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_ads_list'] = self.get_queryset()
        category_pk = self.kwargs.get('pk')
        category_name = dict(Ad._meta.get_field('category').choices).get(category_pk)
        context['category_name'] = category_name
        return context


class ResponseCreateView(LoginRequiredMixin, CreateView):
    model = AdResponse
    form_class = ResponseCreateForm
    template_name = 'response_create.html'
    context_object_name = 'response_create'

    def form_valid(self, form):
        ad_id = self.kwargs.get('pk')
        ad = get_object_or_404(Ad, id=ad_id, pk=self.kwargs.get("pk"))

        if ad.ad_user == self.request.user:
            return HttpResponseForbidden("Вы не можете откликаться на свои собственные объявления.")

        response = form.save(commit=False)
        response.ad_response = ad
        response.user_response = self.request.user
        response.save()
        send_mail(
            subject=f'На Ваш пост {response.ad_response.title} откликнулся {response.user_response.username}.',
            message=response.content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[response.ad_response.ad_user.username]
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('ad_detail', kwargs={'pk': self.object.ad_response.pk})


class ResponseDelete(LoginRequiredMixin, DeleteView):
    model = AdResponse
    template_name = 'resp_delete.html'
    success_url = reverse_lazy('home')
    context_object_name = 'resp_delete'
    queryset = AdResponse.objects.all()


class UserProfileView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'user_prfile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_id = self.kwargs['pk']
        context['user'] = User.objects.get(id=user_id)
        return context


class AdListUser(LoginRequiredMixin, ListView):
    model = Ad
    ordering = '-date'
    template_name = 'ad_list_user.html'
    context_object_name = 'my_ad'
    paginate_by = 10

    def get_queryset(self):
        queryset = Ad.objects.filter(ad_user=self.request.user)
        self.filterset = AdUserFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
    # def get_queryset(self):
    #     queryset = Ad.objects.filter(ad_user=self.request.user).order_by('-date')
    #     order_by = self.request.GET.get('sort', 'date')
    #     if order_by in ['date', '-date']:
    #         queryset = queryset.order_by(order_by)
    #     return queryset


class ResponseListUser(LoginRequiredMixin, ListView):
    model = AdResponse
    ordering = '-date'
    template_name = 'response_list_user.html'
    context_object_name = 'my_response'
    paginate_by = 10

    def get_queryset(self):
        # queryset = super().get_queryset().filter(user_response=self.request.user)
        queryset = AdResponse.objects.filter(user_response=self.request.user).order_by('-date')
        self.filterset = ResponseUserFilter(self.request.GET, queryset)
        return self.filterset.qs
        # return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
    # def get_queryset(self):
    #     queryset = AdResponse.objects.filter(user_response=self.request.user).order_by('-date')
    #     # order_by = self.request.GET.get('sort', 'date')
    #     # if order_by in ['date', '-date', 'is_accepted', '-is_accepted']:
    #     #     queryset = queryset.order_by(order_by)
    #     return queryset


class ResponsesToAdsList(LoginRequiredMixin, ListView):
    """Список откликов на объявления пользователей"""
    model = AdResponse
    ordering = '-date'
    template_name = 'response_to_ad.html'
    context_object_name = 'response_to_ad'
    paginate_by = 10

    def get_queryset(self):
        queryset = AdResponse.objects.filter(ad_response__ad_user=self.request.user).order_by('-date')
        # queryset = AdResponse.objects.all().order_by('-date')
        self.filterset = ResponseFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
    # def get_queryset(self):
    #     queryset = AdResponse.objects.filter(user_response=self.request.user).order_by('-date')
    #     order_by = self.request.GET.get('sort', 'date')
    #     if order_by in ['date', '-date', 'is_accepted', '-is_accepted']:
    #         queryset = queryset.order_by(order_by)
    #     return queryset


@login_required
def response_accept(request, pk):
    resp = get_object_or_404(AdResponse, id=pk)
    resp.is_accepted = True
    resp.save()
    send_mail(
        subject=f'Оповещение',
        message=f'Ваш отклик "{resp}" был принят автором {resp.ad_response.ad_user.username}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[resp.user_response.email],
    )

    return redirect('home')

