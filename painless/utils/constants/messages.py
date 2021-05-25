from django.utils.translation import ugettext_lazy as _


class Message:
    """Class based Messaging system for handling all response messages in views"""

    ######################
    ### Authentication ###
    ######################
    PASSWORD_UPDATE_SUCCESS = _('Password updated successfully.')
    PASSWORD_NOT_VALID = _("Password is not valid.")
    PASSWORD_INCORRECT = _("The current password is incorrect")
    ACCOUNT_NOT_ACTIVE = _("Dear user, Your account is not active.")
    USER_NOT_FOUND = _("User not found.")
    USER_EXISTS = _("User is Exists.")
    LOGIN_SUCCESS = _("You have been logged in successfully.")
    LOGIN_FAILURE = _("login failed.")
    USERNAME_OR_PASSWORD_INCORRECT = _("Username or password is incorrect.")
    TOKEN_VALID = _('Token is valid.')
    TOKEN_EXPIRED = _('Token Expired.')
    YOU_CAN_NOT_REGISTER = _("You Can't Register!")
    REGISTER_SUCCESS = _("User registered successfully.")
    REGISTER_FAILURE = _("Registration failed.")
    YOU_CAN_NOT_RESET_PASSWORD = _("Your Can't ResetPassword!")
    RESET_PASSWORD_SUCCESS = _('Password updated successfully')
    RESET_PASSWORD_FAILURE = _("Reset Password Failed.")
    LOGGED_OUT_SUCCESS = _('User logged out successfully.')
    FIELD_REFRESH_REQUIRED = _('Field `refresh` is required.')

    ################
    ### discount ###
    ################
    DISCOUNT_NOT_FOUND = _('Discount Not Found!')
    UNUSABLE_DISCOUNT = _('This discount is unusable for you!')
    EXPIRED_DISCOUNT = _('This discount is expired for you!')
    DISCOUNT_APPLIED = _("The discount successfully applied")

    #################
    ### education ###
    #################
    YOU_CAN_NOT_PARTICIPATE_PRACTICE = _("You can not participate in the practice.")
    MUST_START_TRAINING = _("You must start training first.")
    ALL_QUESTIONS_NOT_ANSWERED = _("You have not answered all the questions yet")
    ALL_QUESTION_IS_NOT_CORRECT = _("You could not answer all the questions correctly. Please try again")
    ALL_QUESTIONS_IS_CORRECT = _("good job . You were able to answer all the questions correctly")

    ################
    ### practice ###
    ################
    LESSON_NOT_FOUND = _('Lesson Not Found!')
    PRACTICE_PARTICIPATE_NOT_FOUND = _('Practice Participation Not Found!')
    INTERACTION_CREATE_SUCCESS = _('Interactions Created Successfully.')
    PRACTICE_NOT_FOUND = _('Practice Not Found!')
    NOT_PASSED_INTERACTION_NOT_FOUND = _('Not passed interaction not found!')
    ANSWER_CORRECT = _('Answer is correct.')
    ANSWER_INCORRECT = _('Some of the answers was incorrect!')
    NOT_PURCHASED_SUBSCRIPTION = _("You have not purchased a subscription")
    NOT_HAVE_ACTIVE_SUBSCRIPTION = _("You do not have an active subscription")
    NOT_PARTICIPATED_IN_BUNDLE = _("You have not participated in any bundle")
    YOU_HAVE_UNFINISHED_PRACTICES = _('You have unfinished practices.')

    ###############
    ### project ###
    ###############
    HAVE_NO_ACTIVE_BUNDLE = _('You have no active bundles')
    BUNDLE_NOT_FOUND = _("Bundle doesn't found.")
    PROJECT_NOT_FOUND = _("Project doesn't found.")
    TAKEN_PROJECT = _('You have already taken this project.')
    PROJECT_NOT_IN_BUNDLE = _("Project doesn't found in bundle.")
    HAVE_UNFINISHED_PROJECT = _('You have an unfinished project. You can not get another project.')
    AGREE_TERMS = _("You must agree to all terms of this project.")

    ####################
    ### subscription ###
    ####################
    SUBSCRIPTION_NOT_FOUND = _('Subscription Not Found.')
    SUBSCRIPTION_EXISTS = _('Subscription Already Exists.')
    REMAINING_DAYS = _("Remaining Days")
    CHAPTER_NOT_FOUND = _("Chapter Not Found.")
    CHAPTER_ANSWER_CORRECT = _("ChapterAnswer is Correct")
    CHAPTER_ANSWER_INCORRECT = _("Chapter Answer is not correct")
    YOU_CAN_NOT_PARTICIPATE_CHAPTER = _("You can not participate in the chapter.")

    ##############
    ### ticket ###
    ##############
    DEPARTMENT_NOT_FOUND = _('Department not found')
    DRAFT_CAN_NOT_CLOSE = _("draft ticket can't be closed!")
    TICKET_CLOSE_SUCCESS = _('Ticket successfully closed')
    TICKET_NOT_FOUND = _("Ticket Not Found")
    NOT_DRAFT_CAN_NOT_UPDATE = _('Ticket is not draft and can\'t be updated')
    DRAFT_CAN_NOT_ARCHIVE = _('draft ticket can\'t be archived!')
    TICKET_ARCHIVE_SUCCESS = _('Ticket successfully archived')
    CAN_NOT_REPLY_TO_DRAFT = _("You can't reply to a draft ticket")
    CAN_NOT_REPLY_TO_CLOSED = _("You can't reply to a closed ticket")
    DRAFT_CAN_NOT_ADD_FAVORITE = _("Draft ticket can\'t be added to favorites")
    TICKET_ADD_FAVORITE_SUCCESS = _('Ticket successfully added to favorite list')
    TICKET_REMOVE_FAVORITE_SUCCESS = _('Ticket removed from favorite')
    TICKET_REMOVE_ARCHIVE_SUCCESS = _('Ticket removed from archive')
    TICKET_NOT_DRAFT = _('Ticket is not draft')

    ##############
    ### upload ###
    ##############
    CONTENT_MUST_FORM_DATA = _('content type must be multipart/form-data')
    FIELD_IMAGE_REQUIRED = _('field `image` is required.')

    #############
    ### users ###
    #############
    USER_EMAIL_EXISTS = _('A User with this email already exists.')
    ENTER_VALID_EMAIL = _('Enter a valid Email Address')
    USER_IVAN_PROFILE_EXISTS = _('A User with this Ivan Profile already exists.')
    FIELD_AVATAR_SQUARE = _('field `avatar` must have square dimension.')
    IMAGE_NOT_FOUND = _("User image doesn't exist.")
    FIELD_TITLE_REQUIRED = _('field `title` is required')
    TAG_TITLE_NOT_FOUND = _('Tag with title {} doesn\'t exist.')
    FIELD_TITLE_ENABLE_REQUIRED = _('field `title` and `enabled` is required.')
    NOTIF_TITLE_NOT_FOUND = _('Notification with title {} does not exist.')
    FIELD_NOTIF_REQUIRED = _('field `notifications` is required.')
    USER_HAS_MEMBERSHIP = _('User already has a membership plan.')
    PLAN_NOT_FOUND = _('Plan Not Found!')
    FREE_USER_CAN_NOT_JOIN_BUNDLE = _('Free user cannot join to the bundle.')
    USER_HAS_ACTIVE_TRAINING_COURSE = _('The user currently has an active training course.')
    USER_PARTICIPATED_IN_TRAINING_COURSE = _('The user has already participated in this training course.')
    PARTICIPATION_NOT_FOUND = _('Participation Not Found.')
    CANCELLED_SUCCESS = _('Cancelled successfully.')
    USER_HAS_NO_BASKET = _('User has no active basket!')
    FIELD_SCOPE_REQUIRED = _('Field `scope` is required.')
    CHECKOUT_NOT_FOUND = _('Checkout Not Found!')
    PRODUCT_NOT_FOUND = _('Product Not Found!')
    BASKET_IS_EMPTY = _('User basket is empty!')
    NOT_DONE_PROJECT = _('There is no done project.')
    NOT_PARTICIPATED_SKILL = _('There is no participated skill.')
    NOT_DONE_BUNDLE = _('There is no done bundle.')
    BUNDlE_ADD_FAVORITE_SUCCESS = _('Bundle added to favorites successfully.')
    BUNDlE_REMOVE_FAVORITE_SUCCESS = _('Bundle removed from favorites successfully.')
    FIELD_BUNDLE_REQUIRED = _('Field `bundle` is required.')

    def get_message(self, message):
        """
        Return message
        """
        return getattr(self, message)
