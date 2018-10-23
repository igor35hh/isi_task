import getpass
import sys

from django.contrib.auth.management import get_default_username
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError
from django.utils.text import capfirst
from accounts.management import get_default_usertype
from accounts.models import USERTYPE_ADMIN


class NotRunningInTTYException(Exception):
    pass


class Command(createsuperuser.Command):
    help = 'Used to create a superuser with extra field type of user'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_type_field = self.UserModel.\
            _meta.get_field(self.UserModel.USERTYPE_FIELD)

    def handle(self, *args, **options):
        username = options[self.UserModel.USERNAME_FIELD]
        database = options['database']

        # If not provided, create the user with an unusable password
        password = None
        user_data = {}
        # Same as user_data but with foreign keys as fake model instances
        # instead of raw IDs.
        fake_user_data = {}
        verbose_field_name = self.username_field.verbose_name

        # type of user
        type_of_user = None
        verbose_type_of_user = self.user_type_field.verbose_name

        # Do quick and dirty validation if --noinput
        if not options['interactive']:
            try:
                if not username:
                    raise CommandError("You must use --%s with --noinput."
                                       % self.UserModel.USERNAME_FIELD)
                username = self.username_field.clean(username, None)

                for field_name in self.UserModel.REQUIRED_FIELDS:
                    if options[field_name]:
                        field = self.UserModel._meta.get_field(field_name)
                        user_data[field_name] = field.clean(
                            options[field_name], None)
                    else:
                        raise CommandError("You must use --%s with --noinput."
                                           % field_name)
            except exceptions.ValidationError as e:
                raise CommandError('; '.join(e.messages))

        else:
            # Prompt for username/password, and any other required fields.
            # Enclose this whole thing in a try/except to catch
            # KeyboardInterrupt and exit gracefully.
            default_username = get_default_username()
            default_usertype = get_default_usertype()
            try:

                if hasattr(self.stdin, 'isatty') and not self.stdin.isatty():
                    raise NotRunningInTTYException("Not running in a TTY")

                # Get a username
                while username is None:
                    input_msg = capfirst(verbose_field_name)
                    if default_username:
                        input_msg += " (leave blank to use '%s')" \
                            % default_username
                    username_rel = self.username_field.remote_field
                    input_msg = '%s%s: ' % (
                        input_msg,
                        ' (%s.%s)' % (
                            username_rel.model._meta.object_name,
                            username_rel.field_name
                        ) if username_rel else ''
                    )
                    username = self.get_input_data(self.username_field,
                                                   input_msg, default_username)
                    if not username:
                        continue
                    if self.username_field.unique:
                        try:
                            self.UserModel._default_manager.db_manager(
                                database).get_by_natural_key(username)
                        except self.UserModel.DoesNotExist:
                            pass
                        else:
                            self.stderr.write(
                                "Error: That %s is already\
                                taken." % verbose_field_name)
                            username = None

                if not username:
                    raise CommandError(
                        '%s cannot be blank.' % capfirst(verbose_field_name))

                # Get a type of user
                while type_of_user is None:
                    input_msg = capfirst(verbose_type_of_user)
                    if default_usertype:
                        input_msg += \
                            " (input '%s' or leave blank to use '%s')"\
                            % (USERTYPE_ADMIN, default_usertype)
                    usertype_rel = self.user_type_field.remote_field
                    input_msg = '%s%s: ' % (
                        input_msg,
                        ' (%s.%s)' % (
                            usertype_rel.model._meta.object_name,
                            usertype_rel.field_name
                        ) if usertype_rel else ''
                    )
                    type_of_user = self.get_input_data(
                        self.user_type_field, input_msg, default_usertype)
                    if not type_of_user:
                        continue

                if not type_of_user:
                    raise CommandError(
                        '%s cannot be blank.' % capfirst(verbose_type_of_user))

                for field_name in self.UserModel.REQUIRED_FIELDS:
                    field = self.UserModel._meta.get_field(field_name)
                    user_data[field_name] = options[field_name]
                    while user_data[field_name] is None:
                        message = '%s%s: ' % (
                            capfirst(field.verbose_name),
                            ' (%s.%s)' % (
                                field.remote_field.model._meta.object_name,
                                field.remote_field.field_name,
                            ) if field.remote_field else '',
                        )
                        input_value = self.get_input_data(field, message)
                        user_data[field_name] = input_value
                        fake_user_data[field_name] = input_value

                        # Wrap any foreign keys in fake model instances
                        if field.remote_field:
                            fake_user_data[field_name] =\
                                field.remote_field.model(input_value)

                # Get a password
                while password is None:
                    password = getpass.getpass()
                    password2 = getpass.getpass('Password (again): ')
                    if password != password2:
                        self.stderr.write(
                            "Error: Your passwords didn't match.")
                        password = None
                        # Don't validate passwords that don't match.
                        continue

                    if password.strip() == '':
                        self.stderr.write(
                            "Error: Blank passwords aren't allowed.")
                        password = None
                        # Don't validate blank passwords.
                        continue

                    try:
                        validate_password(
                            password2, self.UserModel(**fake_user_data))
                    except exceptions.ValidationError as err:
                        self.stderr.write('\n'.join(err.messages))
                        response = input(
                            'Bypass password validation and\
                            create user anyway? [y/N]: ')
                        if response.lower() != 'y':
                            password = None

            except KeyboardInterrupt:
                self.stderr.write("\nOperation cancelled.")
                sys.exit(1)

            except NotRunningInTTYException:
                self.stdout.write(
                    "Superuser creation skipped due to not running in a TTY. "
                    "You can run `manage.py createsuperuser` in your project "
                    "to create one manually."
                )

        if username:
            user_data[self.UserModel.USERNAME_FIELD] = username
            user_data['password'] = password
            user_data[self.UserModel.USERTYPE_FIELD] = type_of_user
            user = self.UserModel._default_manager.db_manager(
                database).create_superuser(**user_data)
            if options['verbosity'] >= 1:
                token = user.token()
                to_stdout = "Superuser created successfully, token: %s" % token
                self.stdout.write(to_stdout)
