from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

@receiver(post_save, sender=User)
def ensure_admin_is_staff(sender, instance, created, **kwargs):
    """Ensure that any user with role='admin' has is_staff=True so they can access Django Admin.
    We only set is_staff=True (do not unset it), and we avoid recursive saves by using update()."""
    try:
        if getattr(instance, 'role', None) == 'admin' and not instance.is_staff:
            sender.objects.filter(pk=instance.pk).update(is_staff=True)
    except Exception:
        # Fail silently; this signal should not raise exceptions that crash app startup
        pass
