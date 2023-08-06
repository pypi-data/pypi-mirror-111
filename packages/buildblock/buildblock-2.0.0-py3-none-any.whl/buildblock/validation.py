from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class CustomPasswordValidator(object):
    def __init__(self, min_length=8):
        self.min_length = min_length

    def get_help_text(self):
        return _('비밀번호는 대문자, 소문자, 숫자, 특수문자 중 3가지를 조합하여 8자 이상이거나 2가지를 조합하여 10자 이상이어야 합니다.')

    # 비밀번호는 대문자, 소문자, 숫자, 특수문자 중 3가지를 조합하여 8자 이상이거나 2가지를 조합하여 10자 이상이어야 합니다.
    def validate(self, password, user=None):
        characters_count = 0
        special_characters = "[~\\!@#\\$%\\^&\\*\\(\\)_\\+{}\":;'\\[\\]]"

        # 숫자 체크
        if any(char.isdigit() for char in password):
            characters_count += 1

        # 대문자 체크
        if any(char.isupper() for char in password):
            characters_count += 1

        # 소문자 체크
        if any(char.islower() for char in password):
            characters_count += 1

        # 특수문자 체크
        if any(char in special_characters for char in password):
            characters_count += 1

        # 비밀번호 체크: 30자리 이내 중 3종류, 8자리 이상 / 2종류, 10자리 이상
        if len(password) > 30:
            raise ValidationError(_('비밀번호는 30자 이내로 해주세요'))
        elif characters_count >= 3 and len(password) >= 8:
            pass
        elif characters_count >= 2 and len(password) >= 10:
            pass
        else:
            raise ValidationError(
                _('비밀번호는 대문자, 소문자, 숫자, 특수문자 중 3가지를 조합하여 8자 이상이거나 2가지를 조합하여 10자 이상이어야 합니다')
            )
