

from django.conf import settings



class ErrorMessage:
    LOGIN_URL_MISSING = ('Comment App: LOGIN_URL is not in the settings')
    LOGIN_REQUIRED = ('Comment App: You must be logged in to perform this action.')
    NOT_AUTHORIZED = ('You do not have permission to perform this action.')
    METHOD_NOT_IMPLEMENTED = ('Your {class_name} class has not defined a {method_name} method, which is required.')
    NON_AJAX_REQUEST = ('Only AJAX request are allowed')
    INVALID_ORDER_ARGUMENT = ((
        'Comment app: "{order}" is not a valid value for COMMENT_ORDER_BY. '
        'Please choose one among {allowed_orders}.'
        ))
    DUPLICATE_ORDER_VALUE = ((
        'Comment app: COMMENT_ORDER_BY should not have duplicated values '
        'Duplicated Values: {duplicates}. Please use one value only E.g. "{order}" or "-{order}".'
    ))
    WRAP_CONTENT_WORDS_NOT_INT = ('Comment App: settings var COMMENT_WRAP_CONTENT_WORDS must be an integer')


class ContentTypeError:
    ID_NOT_INTEGER = ('{var_name} id must be an integer, {id} is NOT')
    APP_NAME_MISSING = ('app name must be provided')
    APP_NAME_INVALID = ('{app_name} is NOT a valid app name')
    MODEL_NAME_MISSING = ('model name must be provided')
    MODEL_NAME_INVALID = ('{model_name} is NOT a valid model name')
    MODEL_ID_MISSING = ('model id must be provided')
    MODEL_ID_INVALID = ('{model_id} is NOT a valid model id for the model {model_name}')
    PARENT_ID_INVALID = ('{parent_id} is NOT a valid id for a parent comment or '
                          'the parent comment does NOT belong to the provided model object')


class ExceptionError:
    ERROR_TYPE = ('error')
    BAD_REQUEST = ('Bad Request')


class BlockUserError:
    NOT_PERMITTED = (settings.COMMENT_RESPONSE_FOR_BLOCKED_USER)
    INVALID = ('Invalid input data')


class BlockState:
    UNBLOCKED = ('Unblocked')
    BLOCKED = ('Blocked')

class ReactionError:
    TYPE_INVALID = ('Reaction must be an valid ReactionManager.RelationType. {reaction_type} is not')


class ReactionInfo:
    UPDATED_SUCCESS = ('Your reaction has been updated successfully')


class FlagState:
    UNFLAGGED = ('Unflagged')
    FLAGGED = ('Flagged')
    REJECTED = ('Flag rejected by the moderator')
    RESOLVED = ('Comment modified by the author')


class FlagError:
    SYSTEM_NOT_ENABLED = ('Flagging system must be enabled')
    NOT_FLAGGED_OBJECT = ('Object must be flagged!')
    STATE_INVALID = ('{state} is an invalid state')
    REASON_INVALID = ('{reason} is an invalid reason')
    INFO_MISSING = ('Please supply some information as the reason for flagging')
    ALREADY_FLAGGED_BY_USER = ('This comment is already flagged by this user ({user})')
    NOT_FLAGGED_BY_USER = ('This comment was not flagged by this user ({user})')
    REJECT_UNFLAGGED_COMMENT = ('This action cannot be applied on unflagged comments')
    RESOLVE_UNEDITED_COMMENT = ('The comment must be edited before resolving the flag')
    STATE_CHANGE_ERROR = ('Unable to change flag state at the moment!')


class FlagInfo:
    FLAGGED_SUCCESS = ('Obj flagged')
    UNFLAGGED_SUCCESS = ('Obj flag removed')


class FollowError:
    EMAIL_REQUIRED = ('Email is required to subscribe {model_object}')
    SYSTEM_NOT_ENABLED = ('Subscribe system must be enabled')


class BlockState:
    UNBLOCKED = ('Unblocked')
    BLOCKED = ('Blocked')


class BlockUserError:
    NOT_PERMITTED = (settings.COMMENT_RESPONSE_FOR_BLOCKED_USER)
    INVALID = ('Invalid input data')

class EmailInfo:
    CONFIRMATION_SUBJECT = ('Comment Confirmation Request')
    CONFIRMATION_SENT = ('We have sent a verification link to your email.'
                          'The comment will be displayed after it is verified.')
    INPUT_PLACEHOLDER = ('email address, this will be used for verification.')
    INPUT_TITLE = ('email address, it will be used for verification.')
    NOTIFICATION_SUBJECT = ('{username} added comment to "{thread_name}"')
    LABEL = ('email')


class EmailError:
    EMAIL_INVALID = ('Enter a valid email address.')
    EMAIL_REQUIRED_FOR_ANONYMOUS = ('Email is required for posting anonymous comments.')
    BROKEN_VERIFICATION_LINK = ('The link seems to be broken.')
    USED_VERIFICATION_LINK = ('The comment has already been verified.')
