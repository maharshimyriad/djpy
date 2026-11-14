"""Educational post-save receiver for task activity logging."""

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Task

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Task, dispatch_uid="tasks.log_task_saved")
def log_task_saved(sender, instance, created, **kwargs):
    """Log whether a task row was created or updated after it is saved."""
    action = "created" if created else "updated"
    logger.info("Task %s was %s", instance.pk, action)