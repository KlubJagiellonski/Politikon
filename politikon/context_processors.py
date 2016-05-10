import productionsettings


def politikon_settings(request):
    return {
        'facebook_app_id': productionsettings.FACEBOOK_APPLICATION_ID
    }
