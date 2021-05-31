"""Tokens"""
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailConfirmationTokenGenerator(PasswordResetTokenGenerator):
    """Token for confirmation account"""
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(EmailConfirmationTokenGenerator,
                                 cls).__new__(cls)
        return cls.instance

    def _make_hash_value(self, user, timestamp):
        """Hash the user's primary key and user active state that's sure to change
        after an email would be confirmed to produce a token that invalidated
        when it's used
        """
        return (
                str(user.pk) + str(timestamp) +
                str(user.is_active)
        )
