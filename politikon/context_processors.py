from politikon.settings import production


def politikon_settings(request):
    return {
        'facebook_app_id': production.FACEBOOK_APPLICATION_ID
    }
