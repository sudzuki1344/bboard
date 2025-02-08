from django.core.exceptions import ValidationError


class NoForbiddenCharsValidator:
    def __init__(self, forbidden_chars=(' ',)):
        self.forbidden_chars = forbidden_chars

    def validate(self, password, user=None):
        for fc in self.forbidden_chars:
            if fc in password:
                raise ValidationError(
                    f'Пароль не должен содержать недопустимые символы '
                    f'{", ".join(self.forbidden_chars)}',
                    code='forbidden_chars_present')

    def get_help_text(self):
        return (f'Пароль не должен содержать недопустимые символы '
                f'{", ".join(self.forbidden_chars)}')

def validate_non_negative(value):
    """
    Валидатор, который принимает только неотрицательные числа (включая 0)
    """
    if value < 0:
        raise ValidationError(
            '%(value)s должно быть неотрицательным числом',
            params={'value': value},
        )
