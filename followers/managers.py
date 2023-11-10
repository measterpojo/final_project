from django.db import models
from django.contrib.contenttypes.models import ContentType


class FollowerManager(models.Model):

    def is_following(self, email, model_object):
        content_type = ContentType.objects.get_for_model(model_object)
        return self.filter(email=email, object_id=model_object.id, content_type=content_type).exists()

    def follow(self, email, username, model_object):
        if not email or self.is_following(email, model_object):
            return None
        return self.create(email=email, username=username, content_object=model_object)
    
    def unfollow(self, email, model_object):
        content_type = ContentType.objects.get_for_model(model_object)
        self.get(email=email, object_id=model_object.id, content_type=content_type).delete()
    
    def toggle_follow(self, email, username, model_object):
        if not email:
            return False
        if self.is_following(email, model_object):
            self.unfollow(email, model_object)
            return False
        self.follow(email, username, model_object)
        return True
    

    def follow_own_thread(self, obj):
        pass

    def filter_for_model_object(self, model_obj):
        content_type = ContentType.objects.get_for_model(model_obj)
        return self.filter(content_type=content_type, object_id=model_obj.id)

    def get_emails_for_model_object(self, model_obj):
        return self.filter_for_model_object(model_obj).values_list('email', flat=True)