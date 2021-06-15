"""View test"""

from django.urls import reverse

from gameMuster.tests.base_test import BaseTest


class ViewTestCase(BaseTest):
    """View test"""

    def test_user_profile_accessible_when_authenticated(self):
        """Test that authenticated users can access profile page"""
        self.login_user()
        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 200)

    def test_user_profile_not_accessible_when_not_authenticated(self):
        """Test that not authenticated users can't access profile page"""
        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 302)
