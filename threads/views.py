from django.views import generic
from .models import ThreadPost
from .forms import ThreadPostForm, ThreadCommentForm
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormMixin
# Create your views here.

'''
Notes:
1. get_queryset gets multiple instances of a model while
   get_object returns an instance of a object
'''


class ThreadDetailView(FormMixin, generic.DetailView):
    #To-do track number of views using django hitcount https://dev.to/coderasha/how-to-track-number-of-hits-views-for-chosen-objects-in-django-django-packages-series-2-3bcb # noqa
    template_name = 'threads/thread_detail.html'
    model = ThreadPost
    context_object_name = "threaddetail"
    form_class = ThreadCommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.thread_comments # noqa
        context['form'] = ThreadCommentForm(initial={
            'thread': self.object,
            'user': self.request.user,
        })
        return context

    def get_success_url(self):
        return reverse_lazy('thread_detail', kwargs={'slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ThreadListView(generic.ListView):
    template_name = 'threads/thread_list.html'
    model = ThreadPost
    context_object_name = "threadpost"
    ordering = ['-created_at']
    # TO-DO: Pagination
    paginate_by = 9
    queryset = ThreadPost.objects.annotate(
        num_comments=Count('thread_comments')
    )


class ThreadCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = ThreadPostForm
    success_url = reverse_lazy('home')
    template_name = 'threads/thread_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ThreadUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ThreadPost
    template_name = 'threads/thread_update.html'
    form_class = ThreadPostForm

    def get_success_url(self):
        return reverse('thread_detail', kwargs={'slug': self.object.slug})


class UserThreadListView(LoginRequiredMixin, generic.ListView):
    template_name = 'threads/user_thread_list.html'
