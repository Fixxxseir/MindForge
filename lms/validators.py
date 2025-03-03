import re

from rest_framework.serializers import ValidationError


class CustomURLValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile(r"^https?://(?:[a-z0-9-]+\.)?youtube\.com(/|$)")

        if not isinstance(value, str) or not reg.match(value):
            raise ValidationError("Сторонние ресурсы кроме youtube.com запрещены")

        # tmp_dict = dict(value).get(self.field)
        # if tmp_dict is None:
        #     return
        #
        # if not bool(reg.match(tmp_dict)):
        #     raise ValidationError("Сторонние ресурсы кроме youtube.com запрещены")
