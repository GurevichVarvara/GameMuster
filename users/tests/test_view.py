"""View test"""

from django.urls import reverse
from django.test.client import RequestFactory
from faker import Factory

from gameMuster.tests.base_test import BaseTest

from users.views import is_user_email_changed, UserEditView
from users.forms import UserEditForm

faker = Factory.create()


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

    def get_data_for_user_edit_form(self):
        return {
            "username": self.user.username,
            "unconfirmed_email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
        }

    def test_email_change_with_different_email(self):
        """Test email change checking with different email"""
        different_email = faker.email()

        result = is_user_email_changed(
            different_email, UserEditForm(data=self.get_data_for_user_edit_form())
        )

        self.assertTrue(result)

    def test_email_change_with_same_email(self):
        """Test email change checking with the same email"""
        result = is_user_email_changed(
            self.user.email, UserEditForm(data=self.get_data_for_user_edit_form())
        )

        self.assertFalse(result)

    def test_user_edit_view_with_changes(self):
        """Test user edit view with changed fields"""
        data_for_form = self.get_data_for_user_edit_form()
        new_first_name = faker.first_name
        data_for_form["first_name"] = new_first_name

        url = reverse("profile-edit", args=(self.user.id,))
