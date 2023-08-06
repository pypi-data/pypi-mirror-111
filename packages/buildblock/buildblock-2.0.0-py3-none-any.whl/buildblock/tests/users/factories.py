import string
from typing import Any, Sequence

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from factory import DjangoModelFactory, Faker, LazyAttribute, RelatedFactory, SelfAttribute, SubFactory, post_generation
from factory.fuzzy import FuzzyInteger, FuzzyText

from buildblock.apps.core.constants import COUNTRY_KOREA, TENANT_ROLE
from buildblock.apps.users.models import ProfileTenant


class BaseUserFactory(DjangoModelFactory):

    username = Faker("user_name")
    email = Faker("email")

    first_name = Faker("first_name")
    last_name = Faker("last_name")

    phone_number = FuzzyText(length=11, chars=string.digits)
    nationality = LazyAttribute(lambda o: o.country)

    class Meta:
        abstract = True
        model = get_user_model()
        django_get_or_create = ["username"]

    class Params:
        country = COUNTRY_KOREA

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = Faker(
            "password",
            length=15,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        ).generate(extra_kwargs={})
        self.set_password(password)


class UserFactory(BaseUserFactory):
    pass


class EmailFactory(DjangoModelFactory):

    user = SubFactory(UserFactory)
    email = LazyAttribute(lambda o: o.user.email)
    primary = False
    verified = False

    class Meta:
        model = EmailAddress


class InvitedUserFactory(BaseUserFactory):
    is_invited = True
    need_to_change_password = True

    tmp = RelatedFactory(EmailFactory, 'user', primary=True, verified=True)


class ProfileTenantFactory(DjangoModelFactory):

    user = SubFactory(UserFactory, country=SelfAttribute('..t_country'), user_role=[TENANT_ROLE])
    emergency_contact = Faker("phone_number")
    income = FuzzyInteger(10_000, 30_000)
    occupation = Faker("sentence", nb_words=3, variable_nb_words=True, ext_word_list=None)
    ssn = FuzzyText(length=800, chars=string.ascii_lowercase)
    ssn_last4_hashed = FuzzyText(length=4, chars=string.ascii_lowercase)
    credit_score = FuzzyText(length=2, chars=string.digits)

    class Params:
        country = COUNTRY_KOREA

    class Meta:
        model = ProfileTenant
        exclude = ('t_country', )

    t_country = LazyAttribute(lambda o: o.country)
