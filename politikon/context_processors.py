from politikon.settings import production


def politikon_settings(request):
    try:
        moderators = production.FACEBOOK_APPLICATION_MODERATORS.split(",")
    except AttributeError:
        moderators = []
    return {
        'facebook_app_id': production.FACEBOOK_APPLICATION_ID,
        'facebook_moderators': moderators
    }
