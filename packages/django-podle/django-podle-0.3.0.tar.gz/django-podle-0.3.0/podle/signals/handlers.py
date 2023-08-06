import logging

from django.conf import settings
from django.db.models.signals import pre_save, pre_delete, post_save
from django.dispatch import receiver

from ..models import Dictionary, RssFeed
from ..podle import PodleHelper

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Dictionary)
def create_or_update_dictionary_word(sender, instance, *args, **kwargs):
    response = PodleHelper().create_or_update_word(
        {"value": instance.pronunciation, "raw": instance.word}
    )
    if "added" not in response:
        logger.error(response)
        raise Exception(response)

    logger.info(response)


@receiver(pre_delete, sender=Dictionary)
def delete_dictionary_word(sender, instance, *args, **kwargs):
    response = PodleHelper().delete_word(instance.word)
    if "deleted" not in response:
        logger.error(response)
        raise Exception(response)

    logger.info(response)


@receiver(post_save, sender=RssFeed)
def create_rss_feed(sender, instance, created, *args, **kwargs):
    if not instance.feed:
        response = PodleHelper().create_private_rss(
            {
                "subscriberId": instance.user.pk,
                "newsletterName": settings.PODLE_NEWSLETTER_NAME,
            }
        )

        feed = response.get(str(instance.user.pk), None)

        if not feed:
            logger.error(response)
            raise Exception(response)

        instance.feed = feed
        instance.save()

        logger.info(response)


@receiver(pre_delete, sender=RssFeed)
def delete_rss_feed(sender, instance, *args, **kwargs):
    response = PodleHelper().delete_private_rss(
        instance.user.pk, settings.PODLE_NEWSLETTER_NAME
    )
    if "deleted" not in response.get(str(instance.user.pk)):
        logger.error(response)
        raise Exception(response)

    logger.info(response)
