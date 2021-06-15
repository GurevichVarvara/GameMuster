"""User forms tests"""
from faker import Factory

from django.test import TestCase

from users.forms import SignupForm, UserEditForm


faker = Factory.create()


class UserFormsTests(TestCase):
    """User forms tests"""

    def test_signup_form_valid_data(self):
        """Test signup form with valid data"""
        user_password = faker.password()
        form = SignupForm(
            data={
                "username": faker.first_name(),
                "unconfirmed_email": faker.email(),
                "birthday": faker.date_time(),
                "first_name": faker.first_name(),
                "last_name": faker.last_name(),
                "password1": user_password,
                "password2": user_password,
            }
        )

        self.assertTrue(form.is_valid())

    def test_signup_form_no_data(self):
        """Test signup form with no data"""
        form = SignupForm(data={})

        self.assertFalse(form.is_valid())

    def test_user_edit_form_valid_data(self):
        """Test user edit form with valid data"""
        form = UserEditForm(
            data={
                "username": faker.first_name(),
                "unconfirmed_email": faker.email(),
                "birthday": faker.date_time(),
                "first_name": faker.first_name(),
                "last_name": faker.last_name(),
            }
        )

        self.assertTrue(form.is_valid())

    def test_user_edit_form_no_data(self):
        """Test user edit form with no data"""
        form = UserEditForm(data={})

        self.assertFalse(form.is_valid())
