from django.shortcuts import render
import json

from django.core.exceptions import ValidationError
from django.views import View
from django.contrib.contenttypes.models import ContentType

from reactions.models import Reaction, ReactionInstance

from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

from core.mixins import BasePermission
from core.responses import DABResponseData, UTF8JsonResponse
from core.context import DABContext
from core.messages import ReactionInfo

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

@method_decorator(require_POST, name='dispatch')
class SetReaction(BasePermission, View, DABResponseData):
    
    model = None

    def post(self, request, pk, reaction):

        obj = self.model.objects.get(pk=pk)
        reaction_obj = Reaction.objects.get_reaction_object(obj)


        try:
            ReactionInstance.objects.set_reaction(user=request.user,reaction_type=reaction, reaction=reaction_obj)
        except ValidationError as e:
            self.error = e.message
            self.status = 400
            return UTF8JsonResponse(self.json(), status=self.status)
        
        # obj.reaction.refresh_from_db()
        self.data = {
            'status': 0,
            'likes': obj.likes,
            'dislikes': obj.dislikes,
        }
        self.msg = ReactionInfo.UPDATED_SUCCESS
        return UTF8JsonResponse(self.json())









