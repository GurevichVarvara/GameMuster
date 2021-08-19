"""View test"""

from django.urls import reverse
from django.utils import timezone
from faker import Factory

from gameMuster.tests.base_test import BaseTest

from users.views import is_user_email_changed
from users.forms import UserEditForm, SignupForm

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
        """Data for edit form"""
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
        self.login_user()

        data_for_form = self.get_data_for_user_edit_form()
        new_first_name = faker.first_name()
        data_for_form["first_name"] = new_first_name
        form = UserEditForm(data=data_for_form)

        url = reverse("profile-edit", args=(self.user.id,))
        response = self.client.post(url, form=form)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("users/user_update_form.html")

    def get_data_for_signup_form(self):
        """Data for signup form"""
        password = self.faker.password()
        new_user_form = {
            "username": self.faker.first_name(),
            "unconfirmed_email": self.faker.email(),
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "birthday": timezone.now(),
            "password1": password,
            "password2": password,
        }

        return new_user_form

    def test_create_user(self):
        """Test user creation"""
        form = SignupForm(data=self.get_data_for_signup_form())

        response = self.client.post(reverse("signup"), form=form)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.is_valid())

    def test_create_user_without_username(self):
        """Test user creation with no username"""
        data_for_form = self.get_data_for_signup_form()
        data_for_form["username"] = None
        form = SignupForm(data=data_for_form)

        response = self.client.post(reverse("signup"), form=form)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertFormError(response, "form", "username", "This field is required.")

    def test_create_user_without_first_name(self):
        """Test user creation with no first name"""
        data_for_form = self.get_data_for_signup_form()
        data_for_form["first_name"] = None
        form = SignupForm(data=data_for_form)

        response = self.client.post(reverse("signup"), form=form)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertFormError(response, "form", "first_name", "This field is required.")

    def test_create_user_without_last_name(self):
        """Test user creation with no last name"""
        data_for_form = self.get_data_for_signup_form()
        data_for_form["last_name"] = None
        form = SignupForm(data=data_for_form)

        response = self.client.post(reverse("signup"), form=form)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertFormError(response, "form", "last_name", "This field is required.")

    def test_create_user_without_email(self):
        """Test user creation with no email"""
        data_for_form = self.get_data_for_signup_form()
        data_for_form["unconfirmed_email"] = None
        form = SignupForm(data=data_for_form)

        response = self.client.post(reverse("signup"), form=form)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertFormError(
            response, "form", "unconfirmed_email", "This field is required."
        )
