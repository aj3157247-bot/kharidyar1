# -*- coding: utf-8 -*-

"""
KharidYar AI Assistant

این ماژول رابط هوش مصنوعی خریدیار است.
فعلاً بدون هیچ کتابخانه اضافی کار می‌کند تا Build پروژه
پایدار بماند.

بعداً API واقعی AI را فقط در همین فایل اضافه می‌کنیم.
"""

from typing import Optional


class KharidYarAI:
    """موتور هوش مصنوعی خریدیار."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.connected = False

    def ask(self, message: str) -> str:
        """
        دریافت سؤال کاربر و برگرداندن پاسخ.

        در نسخه اولیه پاسخ آزمایشی است.
        اتصال به AI واقعی در همین کلاس انجام خواهد شد.
        """

        message = (message or "").strip()

        if not message:
            return "لطفاً سؤال خود را وارد کنید."

        if "سلام" in message:
            return (
                "سلام 👋\n"
                "من دستیار هوشمند خریدیار هستم. "
                "چطور می‌توانم برای خرید به شما کمک کنم؟"
            )

        if "گوشی" in message:
            return (
                "📱 برای انتخاب گوشی بهتر است این موارد را مشخص کنید:\n\n"
                "• بودجه\n"
                "• کاربرد اصلی\n"
                "• برند مورد علاقه\n"
                "• اهمیت دوربین\n"
                "• اهمیت باتری\n"
                "• بازی یا استفاده روزمره\n\n"
                "مثلاً بگویید: "
                "«یک گوشی برای بازی با بودجه ۲۰ میلیون می‌خواهم.»"
            )

        if "لپتاپ" in message or "لپ‌تاپ" in message:
            return (
                "💻 برای انتخاب لپ‌تاپ، بودجه و کاربرد خود را "
                "مشخص کنید؛ مثلاً برنامه‌نویسی، بازی، طراحی یا "
                "استفاده روزمره."
            )

        if "تلویزیون" in message:
            return (
                "📺 برای انتخاب تلویزیون، اندازه صفحه، بودجه، "
                "کیفیت تصویر و برند مورد علاقه مهم هستند."
            )

        if "هدفون" in message or "هندزفری" in message:
            return (
                "🎧 برای انتخاب هدفون یا هندزفری، بودجه، کیفیت صدا، "
                "عمر باتری و نوع استفاده را مشخص کنید."
            )

        return (
            "سؤال شما دریافت شد ✅\n\n"
            "در نسخه نهایی، همین درخواست به هوش مصنوعی "
            "واقعی خریدیار ارسال می‌شود تا بتواند پاسخ "
            "هوشمند و متناسب با نیاز شما ارائه کند."
        )

    def is_ready(self) -> bool:
        """بررسی آماده بودن اتصال AI."""
        return bool(self.api_key) and self.connected

    def set_api_key(self, api_key: str) -> None:
        """تنظیم کلید API بدون ذخیره مستقیم در کد برنامه."""
        self.api_key = (api_key or "").strip()

    def clear_api_key(self) -> None:
        """پاک کردن کلید API از حافظه."""
        self.api_key = None
        self.connected = False
