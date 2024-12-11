from wildBg.accounts.choices import UserLevelChoices
from wildBg.accounts.models import Profile


def give_profile_points(user, operation_type):
    if operation_type == 'post':
        ADD_POINTS = 10
    elif operation_type == 'landmark':
        ADD_POINTS = 50
    else:
        ADD_POINTS = 0

    if hasattr(user, 'profile'):
        user.profile.points += ADD_POINTS
        print(user.profile.level)

        if user.profile.points >= 1250:
            user.profile.level = UserLevelChoices.EXPERT
        elif user.profile.points >= 700:
            user.profile.level = UserLevelChoices.PROFESSIONAL
        elif user.profile.points >= 250:
            user.profile.level = UserLevelChoices.INTERMEDIATE
        else:
            user.profile.level = UserLevelChoices.BEGINNER

        user.profile.save()
    else:
        raise AttributeError("Profile does not exist for this user")
