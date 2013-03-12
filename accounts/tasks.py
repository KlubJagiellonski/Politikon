from celery import task
from constance import config
from django.db import transaction

import logging
logger = logging.getLogger(__name__)


@task
def topup_accounts_task():
    logger.debug("'politikon:tasks:topup_accounts_task' worker up")
    topup_amount = config.DAILY_TOPUP

    from accounts.models import User
    with transaction.commit_on_success():
        for user in User.objects.all().iterator():
            try:
                user.topup_cash(topup_amount)
            except:
                logger.exception("Fatal error during topping up of user #%d <%s>" % (user.id, user))
