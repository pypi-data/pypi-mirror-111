from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask import render_template, url_for, flash, redirect, request
from typing import Tuple


class RegistrationForm(FlaskForm):
    """Form class for creating new account.
    """
    username = StringField(
        'Username',
        validators=[Length(min=1, max=30)])
    password = PasswordField(
        'Password',
        validators=[Length(min=4, max=20)])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username: StringField):
        """Check whether the submitted username is valid.

        The username must satisfy following requirements.
            - Length is between 2 and 30.
            - Contains only alphabets, numbers and symbols in ascii.

        Args:
            username (StringField): Username field.

        Raises:
            ValidationError: Field is invalid.
        """
        if username.data == "":
            flash("The user name is empty", "danger")
            raise ValidationError("")
        if len(username.data) < 2 or 30 < len(username.data):
            flash("The user name must be between 2 and 30 characters.", "danger")
            raise ValidationError("")
        if not str(username.data).isascii():
            flash(
                "Only alphabets, numbers and symbols in ascii can be used for user name ",
                "danger")
            raise ValidationError("")

    def validate_password(self, password: PasswordField):
        """Check whether the submitted password is valid.

        The password must satisfy following requirements.
            - Length is between 4 and 20.
            - Contains only alphabets, numbers and symbols in ascii.

        Args:
            password (StringField): password field.

        Raises:
            ValidationError: Field is invalid.
        """
        if password.data == "":
            flash("The password is empty", "danger")
            raise ValidationError("")
        if len(password.data) < 4 or 20 < len(password.data):
            flash("The password must be between 4 and 20 characters.", "danger")
            raise ValidationError("")
        if not str(password.data).isascii():
            flash(
                "Only alphabets, numbers and symbols in ascii can be used for password.",
                "danger")
            raise ValidationError("")

    def check_validate(self) -> bool:
        """Validates the sumbmitted form.

        Returns:
            bool: True if the form is valid, otherwise False.
        """
        try:
            self.validate_username(self.username)
            self.validate_password(self.password)
            return True
        except ValidationError:
            return False


class LoginForm(FlaskForm, ValidationError):
    """Form class for login.
    """
    username = StringField("username")
    password = PasswordField('Password')
    submit = SubmitField('Login')

    def validate_username(self, username: StringField):
        """Check whether the submitted username is empty.
        """
        if username.data == "":
            flash("The user name is empty", "danger")
            raise ValidationError("Input username")

    def validate_password(self, password):
        """Check whether the submitted password is empty.
        """
        if password == "":
            flash("The password is empty", "danger")
            raise ValidationError("")

    def check_validate(self) -> bool:
        """Validates the sumbmitted form.

        Returns:
            bool: True if the form is valid, otherwise False.
        """
        try:
            self.validate_username(self.username)
            self.validate_password(self.password)
            return True
        except ValidationError:
            return False
