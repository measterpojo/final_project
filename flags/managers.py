from collections import namedtuple

from django.db import models, IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from django.conf import settings

from core.messages import FlagError


class FlagManager(models.Manager):
    def get_for_object(self, obj):
        try:
            flag = obj.flag.get()
        except ObjectDoesNotExist:
            flag = self.create(content_object=obj)
        return flag


class FlagInstanceManager(models.Manager):
    
    REASONS  = getattr(settings, 'FLAG_REASONS')
    REASONS.append((100, ('Something else')))

    Reason = namedtuple('Reasons', ['value', 'reason'])
    reason_list = []
    for res in REASONS:
        reason_list.append(Reason(*res))

    reason_values = [reason.value for reason in reason_list]

    def _clean_reason(self, reason):
        err = ValidationError(FlagError.REASON_INVALID.format(reason=reason))
        try:
            reason = int(reason)
            if reason in self.reason_values:
                return reason
            raise err
        except (ValueError, TypeError):
            raise err
    
    def _clean(self, reason, info):
        cleaned_reason = self._clean_reason(reason)
        cleaned_info = None

        if cleaned_reason == self.reason_values[-1]:
            cleaned_info = info
            if not cleaned_info:
                raise ValidationError(FlagError.INFO_MISSING, code='required')
        return cleaned_reason, cleaned_info
    
    def create_flag(self, user, flag, reason, info):
        err = ValidationError(FlagError.ALREADY_FLAGGED_BY_USER.format(user=user), code='invalid')
        cleaned_reason, cleaned_info = self._clean(reason, info)
        try:
            self.create(flag=flag, user=user, reason=cleaned_reason, info=cleaned_info)
        except IntegrityError:
            raise err

    def delete_flag(self, user, flag):
        err = ValidationError(FlagError.NOT_FLAGGED_BY_USER.format(user=user), code='invalid')
        try:
            self.get(user=user, flag=flag).delete()
        except self.model.DoesNotExist:
            raise err

    def set_flag(self, user, flag, **kwargs):
        reason = kwargs.get('reason', None)
        info = kwargs.get('info', None)
        if reason:
            self.create_flag(user, flag, reason, info)
            created = True
        else:
            self.delete_flag(user, flag)
            created = False
        return created