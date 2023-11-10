from core.validators import ContentTypeValidator, BaseValidatorMixin

from django.contrib.contenttypes.models import ContentType

from core.exceptions import BadRequest
from core.utils import get_request_data


class ParentIdValidator(BaseValidatorMixin):
    parent_comment = None

    def validate_parent_id(self, parent_id):
        try:
            parent_id = int(parent_id)
        except ValueError:
            self.error = 'Id is not a Interger'
            raise BadRequest(self.error)
        return parent_id
    
    def validate_comment_object(self, model_id, parent_id):
        from comments.models import Comment

        try:
            Comment = Comment.objects.get(id=parent_id, object_id=model_id)
        except Comment.DoesNotExist:
            self.error = 'No parent Id found'
            raise BadRequest(self.error)
        return Comment
    
    def validate(self, request):
        super().validate(request)
        model_id = get_request_data(request, 'model_id', self.api)
        parent_id = get_request_data(request, 'parent_id', self.api)
        if not parent_id or parent_id == '0':
            return
        validated_parent_id = self.validate_parent_id(parent_id)
        self.parent_comment = self.validate_comment_object(model_id, validated_parent_id)


class CommentValidateMixin(ContentTypeValidator, ParentIdValidator):
    pass