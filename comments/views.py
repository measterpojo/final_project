from typing import Any, Dict

from django.urls import reverse
from django.template.loader import render_to_string

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import FormView,  CreateView, UpdateView, DeleteView

from django.utils import timezone
from django.conf import settings
from .forms import CommentForm
from .models import Comment
from .context import CommentDABContext, DABContext
from comments.validators import CommentValidateMixin
from core.utils import get_user_for_request

from core.responses import UTF8JsonResponse
from .mixins import CanEditCommentMixin, CanDeleteCommentMixin

from core.views import BaseView, BaseCreateView


class CreateCommentView(CommentValidateMixin, BaseCreateView):

    form_class = CommentForm

    comment = None
    email_service = None

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['comment'] = self.comment
        context.update(CommentDABContext(self.request))
        return context

    def form_valid(self, form):
        user = get_user_for_request(self.request)
        comment_content = form.cleaned_data['content']
        time_posted = timezone.now()
        temp_comment = Comment(
            content_object = self.model_obj,
            content = comment_content,
            user=user,
            parent=self.parent_comment,
            posted=time_posted,)

        self.perform_create(temp_comment, self.request)

        return redirect(self.model_obj.get_absolute_url())

class UpdateCommentView(UpdateView):

    def get_object(self):
        return super().get_object()

    model = Comment

    fields = [
        'content'
    ]



# class UpdateComment(CanEditCommentMixin, BaseCommentView):
#     comment = None
    
#     def get_object(self):
#         self.comment = get_object_or_404(
#             Comment.objects.select_related('user'), 
#             pk=self.kwargs.get('pk')
#         )

#         print(self.comment, 'asssssssssssss')
#         return self.comment

#     def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
#         context = self.get_context_data()
#         context['comment_form'] = CommentForm(instance=self.comment, request=self.request)
#         context['comment'] = self.comment
#         self.data = render_to_string('comments/update_comment.html', context, request=self.request)
#         print(self.data, 'get')
#         return UTF8JsonResponse(self.data)
    
#     def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
#         form = CommentForm(request.POST, instance=self.comment, request=self.request)
#         context = self.get_context_data()
#         print(context)
#         if form.is_valid():
#             form.save()
#             context['comment'] = self.comment
#             return redirect(self.model_obj.get_absolute_url())

class DeleteCommentView(CanDeleteCommentMixin, BaseView):
    comment = None

    def get_object(self):
        self.comment = get_object_or_404(
            Comment.objects.select_related('user'), pk=self.kwargs.get('pk')
        )

        return self.comment
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['comment'] = self.comment
        context['has_parent'] = not self.comment.is_parent
        self.data = render_to_string('comments/delete_comment.html')    
        return UTF8JsonResponse(self.json())


    def post(self, request, *args, **kwargs):
        self.comment.delete()
        return redirect(self.model_obj.get_absolute_url())


