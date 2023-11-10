from django.shortcuts import render

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.views import View
from .models import Flag, FlagInstance
from core.messages import FlagInfo, FlagError
from .mixins import CanSetFlagMixin, CanUpdateFlagStateMixin
from core.mixins import BaseAuthPermission

from core.responses import DABResponseData, UTF8JsonResponse, JsonResponse



class SetFlag(CanSetFlagMixin, BaseAuthPermission, View, DABResponseData):
    model = None

    obj = None

    def get_object(self):
        self.obj = self.model.objects.get(pk=self.kwargs.get('pk'))
        return self.obj
    

    def post(self, request, *args, **kwargs):
        self.data = {
            'status':1
        }

        flag = Flag.objects.get_for_object(self.obj)

        try:
            if FlagInstance.objects.set_flag(request.user, flag, **request.POST.dict()):

                self.msg = FlagInfo.FLAGGED_SUCCESS
                self.data['flag'] = 1
            else:
                self.msg = FlagInfo.UNFLAGGED_SUCCESS
            
            self.data.update({'status': 0})
            self.status = 200
        except ValidationError as e:
            self.error = e.message
            self.status = 400

        return UTF8JsonResponse(self.json(), status=self.status)



class ChangeFlagState(CanUpdateFlagStateMixin, View, DABResponseData):
    
    model = None
    obj = None


    def get_object(self):
        self.obj = self.model.objects.get(pk=self.kwargs.get('pk'))

        return self.obj

    def post(self, request, *args, **kwargs):

        state = request.POST.get('state')
        try:
            self.obj.flag.get().toggle_state(state, request.user)
            self.status = 200
        except ValidationError:
            self.error = FlagError.STATE_CHANGE_ERROR
            self.status = 400
        self.data = {
            'state': self.obj.flag.get().state
        }

        return UTF8JsonResponse(self.json(), status=self.status)