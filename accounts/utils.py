from .managers import UserProfileManager


def format_int(x):
    s = str(int(x))
    l = int((len(s) - 1) / 3)
    for i in range(l, 0, -1):
        s = s[:len(s) - i * 3] + ' ' + s[len(s) - i * 3:]
    return s


def save_profile(backend, user, response, *args, **kwargs):
    print user
    print response
    print backend.name

    if backend.name == 'facebook':
        user.full_name = response['name']
        user.facebook_id = response['id']
        user.save(using=UserProfileManager.db)
        print backend
    if backend.name == 'twitter':
        user.avatarURL = response['profile_image_url']
        user.full_name = response['name']
        user.save(using=UserProfileManager.db)
        print backend
