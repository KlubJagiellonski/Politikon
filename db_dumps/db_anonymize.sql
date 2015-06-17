-- accounts_user
update accounts_user set password='', last_login=LOCALTIMESTAMP, created_date=LOCALTIMESTAMP;

-- accounts_user_friends
delete from accounts_user_friends;

-- django_adming_log
delete from django_admin_log;

-- django_session
delete from django_session;



