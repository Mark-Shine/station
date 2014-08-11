from django.dispatch import Signal

action_message = Signal(providing_args=["sender", "user", "instance", "action"], use_caching=True)