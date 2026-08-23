# -*- coding: utf-8 -*-

"""
ابزارهای رابط کاربری فارسی و RTL برای خریدیار.

هدف این فایل:
- تنظیم راست‌چین بودن TextInput و Label
- جلوگیری از وابستگی به کتابخانه‌های سنگین
- آماده بودن ساختار برای توسعه RTL در نسخه‌های بعدی
"""

from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class RTLLabel(Label):
    """Label مناسب برای متن فارسی."""

    def __init__(self, **kwargs):
        kwargs.setdefault("halign", "right")
        kwargs.setdefault("valign", "middle")
        super().__init__(**kwargs)

        self.bind(
            size=self._update_text_size
        )

    def _update_text_size(self, instance, size):
        self.text_size = size


class RTLTextInput(TextInput):
    """TextInput مناسب برای ورود متن فارسی."""

    def __init__(self, **kwargs):
        kwargs.setdefault("halign", "right")
        kwargs.setdefault("multiline", False)
        super().__init__(**kwargs)


def rtl_text(text):
    """
    نقطه ورود واحد برای پردازش متن فارسی.

    فعلاً متن را بدون دستکاری برمی‌گرداند.
    این کار عمداً انجام شده تا حروف فارسی توسط موتور متن
    Kivy خراب یا معکوس نشوند.
    """
    if text is None:
        return ""

    return str(text)
