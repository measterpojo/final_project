from comments.tests.base import BaseCommentViewTest

from flags.models import FlagInstance

class BaseCommentFlagTest(BaseCommentViewTest):
    user_2 = None
    content_object_2 = None

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.comment = cls.create_comment(cls.content_object_1)
        cls.comment_for_change_state = cls.create_comment(cls.content_object_1)
        cls.user = cls.user_1
        cls.flag_data = {
            'reason': str(FlagInstance.objects.reason_values[0]),
            'info': None,
        }
        cls.comment_2 = cls.create_comment(cls.content_object_2)
        cls.flag_instance = cls.create_flag_instance(cls.user_2, cls.comment_2, **cls.flag_data)

        
