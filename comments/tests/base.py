from django.test import TestCase, RequestFactory, Client

from django.contrib.auth import get_user_model

from blog.models import Article, Category

from comments.models import Comment
from django.contrib.auth.models import Group

from django.utils import timezone
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

from flags.models import FlagInstance, Flag
from reactions.models import ReactionInstance, Reaction

from unittest.mock import patch

from urllib.parse import quote_plus



User = get_user_model()

class BaseCommentTest(TestCase):
    flags = 0
    readtions = 0
    content_object_1 = None
    increment = 0
    user_1 = None

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user_1 = User.objects.create_user(
                    name="test-1",
                    email="test-1@acme.edu",
                    password="1234",
                    phone = '847-296-7568',
        )
        cls.user_2 = User.objects.create_user(
            name="test-2",
            email="test-2@acme.edu",
            password="1234",
            phone = '847-296-7568',
        )

        cls.moderator = User.objects.create_user(
            name="moderator",
            email="test-s2@acme.edu",
            password="1234", 
            is_superuser=True,
            is_staff=True,
            phone = '847-296-7568',

        )


        cls.category = Category.objects.create(
            name='catergory_1'
        )

        cls.post_1 = Article.objects.create(
            author=cls.user_1,
            title="post 1",
            body="first post body",
            category_id = '1'
        )



        cls.post_2 = Article.objects.create(
            author=cls.user_1,
            title="post 2",
            body="second post body",
            category_id = '1'
        )

        content_type = ContentType.objects.get(model='article')
        cls.content_object_1 = content_type.get_object_for_this_type(id=cls.post_1.id)
        cls.content_object_2 = content_type.get_object_for_this_type(id=cls.post_2.id)
        cls.increment = 0
        cls.reactions = 0
        cls.flags = 0

    def setUp(self):
        super().setUp()
        self.client.force_login(self.user_1)
        self.addCleanup(patch.stopall)

    @classmethod
    def increase_comment_count(cls):
        cls.increment += 1
    
    @classmethod
    def create_comment(cls, ct_object, user=None, email=None, posted=None, parent=None):
        if not user:
            user = cls.user_1
        cls.increase_comment_count()
        return Comment.objects.create(
            content_object=ct_object,
            content='comment {}'.format(cls.increment),
            user=user,
            parent=parent
        )
        
    @classmethod
    def create_anonymous_comment(cls,ct_object=None, email=None, posted=None, parent=None):
        if not ct_object:
            ct_object = cls.content_object_1
        if not email:
            email = cls.user_1.email
        if not posted:
            posted = timezone.now()
        cls.increase_comment_count()
        return Comment.objects.create(
            content_object=ct_object,
            content='anonymous comment {}'.format(cls.increment),
            parent=parent,
            email=email,
            posted=posted
        )
    

    # content_object, content_type, content_type_id, dislikes, id, likes, object_id, reactions

    @classmethod
    def create_reaction_instance(cls, user, comment, reaction):
        print(comment)
        print(reaction)

        content_type = ContentType.objects.get_for_model(comment)
        print(content_type, 'ass')

        reaction_type = getattr(ReactionInstance.ReactionType, reaction.upper(), None)
        if reaction_type:

            reaction_obj = Reaction.objects.get(content_object=comment, reactions=user)
            cls.reactions += 1
            reaction_instance = ReactionInstance.objects.create(
                user=user,
                reaction_type=reaction_type.value,
                reaction=reaction_obj
            )
            comment.reaction.refresh_from_db()
            return reaction_instance
        raise ValueError('{} is not a valid reaction type'.format(reaction))

    @staticmethod
    def set_reaction(user, comment, reaction):
        ReactionInstance.objects.set_reaction(user, comment.reaction, reaction)

    @staticmethod
    def set_flag(user, comment, **kwargs):
        return FlagInstance.objects.set_flag(user, comment.flag.get(), **kwargs)

    @classmethod
    def create_flag_instance(cls, user, comment, **kwargs):
        instance = FlagInstance.objects.create(
            user=user,
            flag=comment.flag.get(),
            **kwargs
        )
        cls.flags += 1
        return instance


class BaseCommentManagerTest(BaseCommentTest):
    content_object_2 = None

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

        cls.parent_comment_1 = cls.create_comment(cls.content_object_1)
        cls.parent_comment_2 = cls.create_comment(cls.content_object_1)
        cls.parent_comment_3 = cls.create_comment(cls.content_object_1)
        cls.child_comment_1 = cls.create_comment(cls.content_object_1, parent=cls.parent_comment_1)
        cls.child_comment_2 = cls.create_comment(cls.content_object_1, parent=cls.parent_comment_2)
        cls.child_comment_3 = cls.create_comment(cls.content_object_1, parent=cls.parent_comment_2)

        cls.parent_comment_4 = cls.create_comment(cls.content_object_2)
        cls.parent_comment_5 = cls.create_comment(cls.content_object_2)
        cls.child_comment_4 = cls.create_comment(cls.content_object_2, parent=cls.parent_comment_1)
        cls.child_comment_5 = cls.create_comment(cls.content_object_2, parent=cls.parent_comment_2)



class BaseCommentUtilsTest(BaseCommentTest):
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.factory = RequestFactory()
        cls.comment_1 = cls.create_comment(cls.content_object_1)
        cls.comment_2 = cls.create_comment(cls.content_object_1)
        cls.comment_3 = cls.create_comment(cls.content_object_1)
        cls.anonymous_comment = cls.create_anonymous_comment()


class BaseCommentViewTest(BaseCommentTest):

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.client.force_login(self.user_2)
        self.data = {
            'content': 'parent comment was edited',
            'app_name': self.post_1._meta.app_label,
            'model_name': self.post_1.__class__.__name__.lower(),
            'model_id': self.post_1.id,
        }
    @staticmethod
    def get_url(reverse_name, pk=None, data=None):
        if pk:
            url = reverse(reverse_name, args=[pk])
        else:
            url = reverse(reverse_name)

        if not data:
            data = {}

        query_string = '&'.join([f'{name}={quote_plus(str(value))}' for name, value in data.items()])
        if query_string:
            return url + f'?{query_string}'
        return url