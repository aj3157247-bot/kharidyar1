# -*- coding: utf-8 -*-

"""
KharidYar - Main Menu

منوی اصلی برنامه خریدیار.
این فایل مستقل طراحی شده تا بتوان آن را بدون وابستگی
به صفحات اصلی برنامه استفاده و توسعه داد.
"""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from ui.rtl import RTLLabel


class KharidYarMenu(BoxLayout):
    """
    منوی اصلی خریدیار.

    callback باید تابعی باشد که نام صفحه را دریافت کند.
    مثال:

        menu = KharidYarMenu(
            on_page_selected=self.show_page
        )
    """

    MENU_ITEMS = [
        ("🏠  صفحه اصلی", "home"),
        ("🤖  دستیار هوشمند", "ai"),
        ("🔎  جستجوی کالا", "search"),
        ("⭐  علاقه‌مندی‌ها", "favorites"),
        ("⚖️  مقایسه کالا", "compare"),
        ("🛍️  لیست خرید", "shopping_list"),
        ("⚙️  تنظیمات", "settings"),
        ("ℹ️  درباره خریدیار", "about"),
    ]

    def __init__(
        self,
        on_page_selected=None,
        on_close=None,
        **kwargs
    ):
        super().__init__(
            orientation="vertical",
            spacing=dp(7),
            padding=dp(14),
            size_hint_x=None,
            width=dp(290),
            **kwargs
        )

        self.on_page_selected = on_page_selected
        self.on_close = on_close

        self.build_menu()

    # ========================================================
    # ساخت منو
    # ========================================================

    def build_menu(self):

        # ----------------------------------------------------
        # سربرگ
        # ----------------------------------------------------

        header = BoxLayout(
            orientation="vertical",
            spacing=dp(2),
            size_hint_y=None,
            height=dp(92),
        )

        title = RTLLabel(
            text="🛒 خریدیار",
            font_size=dp(25),
            bold=True,
            color=(0.05, 0.20, 0.45, 1),
            halign="right",
            valign="middle",
        )

        title.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        subtitle = RTLLabel(
            text="دستیار هوشمند خرید",
            font_size=dp(14),
            color=(0.35, 0.38, 0.42, 1),
            halign="right",
            valign="middle",
        )

        subtitle.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        header.add_widget(title)
        header.add_widget(subtitle)

        self.add_widget(header)

        # ----------------------------------------------------
        # جداکننده
        # ----------------------------------------------------

        self.add_widget(
            self.create_separator()
        )

        # ----------------------------------------------------
        # آیتم‌های اصلی
        # ----------------------------------------------------

        for text, page_name in self.MENU_ITEMS:
            self.add_menu_button(
                text,
                page_name
            )

        # ----------------------------------------------------
        # فضای خالی
        # ----------------------------------------------------

        self.add_widget(
            Widget()
        )

        # ----------------------------------------------------
        # پایین منو
        # ----------------------------------------------------

        self.add_widget(
            self.create_separator()
        )

        creator = RTLLabel(
            text="ساخته شده برای تجربه خرید هوشمند",
            font_size=dp(12),
            color=(0.45, 0.47, 0.50, 1),
            halign="right",
            valign="middle",
            size_hint_y=None,
            height=dp(35),
        )

        creator.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        self.add_widget(creator)

    # ========================================================
    # دکمه منو
    # ========================================================

    def add_menu_button(self, text, page_name):

        button = Button(
            text=text,
            font_name="KharidYarFont",
            font_size=dp(16),
            color=(0.06, 0.08, 0.12, 1),
            background_normal="",
            background_color=(0.92, 0.95, 0.98, 1),
            size_hint_y=None,
            height=dp(52),
            halign="right",
            valign="middle",
        )

        button.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        button.bind(
            on_release=lambda *_:
            self.select_page(page_name)
        )

        self.add_widget(button)

    # ========================================================
    # انتخاب صفحه
    # ========================================================

    def select_page(self, page_name):

        if callable(self.on_page_selected):
            self.on_page_selected(page_name)

        if callable(self.on_close):
            self.on_close()

    # ========================================================
    # خط جداکننده
    # ========================================================

    @staticmethod
    def create_separator():

        separator = Widget(
            size_hint_y=None,
            height=dp(1),
        )

        return separator
