"""User backend tests"""

from gameMuster.tests.base_test import BaseTest


class UserBackendTestCase(BaseTest):
    """User backend tests"""

    def test_user_with_no_active_time_login(self):
        """Test that user with empty active time could not login"""
        self.user.active_time = None
        self.user.save()

        login_result = self.login_user()

        self.assertFalse(login_result)

    def test_user_with_active_time_login(self):
        """Test that user with not empty active time could login"""
        login_result = self.login_user()

        self.assertTrue(login_result)

    def test_admin_with_no_active_time_login(self):
        """Test that admin with empty active time could login"""
        self.user.is_staff = True
        self.user.active_time = None
        self.user.save()

        login_result = self.login_user()

        self.assertTrue(login_result)
