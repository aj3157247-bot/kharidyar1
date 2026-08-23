# -*- coding: utf-8 -*-

import os

from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from ai.assistant import KharidYarAI
from ui.menu import KharidYarMenu
from ui.rtl import RTLLabel, RTLTextInput


APP_NAME = "خریدیار"
APP_VERSION = "1.0.0"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(
    BASE_DIR,
    "assets",
    "Vazirmatn-Regular.ttf"
)

if os.path.exists(FONT_PATH):
    try:
        LabelBase.register(
            name="KharidYarFont",
            fn_regular=FONT_PATH
        )
        FONT_NAME = "KharidYarFont"
    except Exception:
        FONT_NAME = "Roboto"
else:
    FONT_NAME = "Roboto"


def label(
    text="",
    size=16,
    bold=False,
    color=(0.08, 0.09, 0.12, 1)
):
    widget = RTLLabel(
        text=text,
        font_name=FONT_NAME,
        font_size=dp(size),
        bold=bold,
        color=color
    )
    return widget


def button(
    text,
    callback=None,
    height=52
):
    widget = Button(
        text=text,
        font_name=FONT_NAME,
        font_size=dp(16),
        size_hint_y=None,
        height=dp(height),
        background_normal="",
        background_color=(0.10, 0.42, 0.90, 1),
        color=(1, 1, 1, 1)
    )

    if callback:
        widget.bind(on_release=callback)

    return widget


class Page(BoxLayout):

    def __init__(self, app, title, **kwargs):
        super().__init__(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(15),
            **kwargs
        )

        self.app = app

        header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(55),
            spacing=dp(8)
        )

        menu_button = button(
            "☰",
            self.open_menu,
            50
        )

        menu_button.size_hint_x = None
        menu_button.width = dp(55)

        header.add_widget(menu_button)

        header.add_widget(
            label(
                title,
                22,
                True,
                (0.05, 0.20, 0.45, 1)
            )
        )

        self.add_widget(header)

    def open_menu(self, *_):
        self.app.open_menu()


class HomePage(Page):

    def __init__(self, app, **kwargs):
        super().__init__(
            app,
            "خریدیار",
            **kwargs
        )

        self.add_widget(
            label(
                "خوش آمدید 👋",
                26,
                True,
                (0.05, 0.20, 0.45, 1)
            )
        )

        welcome = label(
            "خریدیار دستیار هوشمند خرید شماست.\n\n"
            "می‌توانید برای انتخاب کالا، مقایسه محصولات "
            "و تصمیم‌گیری بهتر از آن استفاده کنید.",
            17
        )

        welcome.size_hint_y = None
        welcome.height = dp(120)

        self.add_widget(welcome)

        self.add_widget(
            button(
                "🤖 دستیار هوشمند",
                lambda *_: app.show_page("ai")
            )
        )

        self.add_widget(
            button(
                "🔎 جستجوی کالا",
                lambda *_: app.show_page("search")
            )
        )

        self.add_widget(
            button(
                "⚖️ مقایسه کالا",
                lambda *_: app.show_page("compare")
            )
        )

        self.add_widget(Widget())


class AIPage(Page):

    def __init__(self, app, **kwargs):
        super().__init__(
            app,
            "دستیار هوشمند",
            **kwargs
        )

        self.ai = KharidYarAI()
        self.busy = False

        self.scroll = ScrollView()

        self.messages = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(8),
            size_hint_y=None
        )

        self.messages.bind(
            minimum_height=self.messages.setter(
                "height"
            )
        )

        self.scroll.add_widget(self.messages)
        self.add_widget(self.scroll)

        bottom = BoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(58)
        )

        self.input = RTLTextInput(
            font_name=FONT_NAME,
            font_size=dp(15),
            multiline=False,
            hint_text="سؤال خود را بنویسید..."
        )

        bottom.add_widget(self.input)

        send = button(
            "ارسال",
            self.send_message,
            58
        )

        send.size_hint_x = None
        send.width = dp(85)

        bottom.add_widget(send)

        self.add_widget(bottom)

        self.add_message(
            "خریدیار 🤖",
            "سلام 👋\n"
            "من دستیار هوشمند خریدیار هستم.\n"
            "چه چیزی می‌خواهید بخرید؟"
        )

    def add_message(self, sender, text):

        box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=dp(8)
        )

        title = label(
            sender,
            14,
            True,
            (0.05, 0.20, 0.45, 1)
        )

        title.size_hint_y = None
        title.height = dp(28)

        message = label(
            text,
            15
        )

        lines = max(
            2,
            text.count("\n") + 1
        )

        message.size_hint_y = None
        message.height = dp(32 * lines)

        box.height = (
            title.height +
            message.height +
            dp(20)
        )

        box.add_widget(title)
        box.add_widget(message)

        self.messages.add_widget(box)

        Clock.schedule_once(
            lambda *_:
            setattr(self.scroll, "scroll_y", 0),
            0.05
        )

    def send_message(self, *_):

        if self.busy:
            return

        text = self.input.text.strip()

        if not text:
            return

        self.input.text = ""

        self.add_message(
            "شما",
            text
        )

        self.busy = True

        Clock.schedule_once(
            lambda *_:
            self.get_ai_response(text),
            0.05
        )

    def get_ai_response(self, text):

        try:
            response = self.ai.ask(text)
        except Exception as error:
            response = (
                "خطایی در دستیار هوشمند رخ داد.\n\n"
                + str(error)
            )

        self.add_message(
            "خریدیار 🤖",
            response
        )

        self.busy = False


class SearchPage(Page):

    def __init__(self, app, **kwargs):
        super().__init__(
            app,
            "جستجوی کالا",
            **kwargs
        )

        self.search_input = RTLTextInput(
            font_name=FONT_NAME,
            font_size=dp(17),
            multiline=False,
            hint_text="نام کالا را وارد کنید..."
        )

        self.search_input.size_hint_y = None
        self.search_input.height = dp(55)

        self.add_widget(
            self.search_input
        )

        self.add_widget(
            button(
                "🔎 جستجو",
                self.search
            )
        )

        self.result = label(
            "نتایج جستجو در این قسمت نمایش داده می‌شود.",
            16
        )

        self.result.size_hint_y = None
        self.result.height = dp(180)

        self.add_widget(
            self.result
        )

        self.add_widget(Widget())

    def search(self, *_):

        query = self.search_input.text.strip()

        if not query:
            self.result.text = (
                "لطفاً نام کالا را وارد کنید."
            )
            return

        self.result.text = (
            "🔎 جستجوی کالا\n\n"
            "کالای موردنظر:\n"
            + query
            + "\n\n"
            "سیستم جستجوی فروشگاه‌ها و مقایسه قیمت "
            "در مرحله اتصال سرویس‌های واقعی فعال خواهد شد."
        )


class ComparePage(Page):

    def __init__(self, app, **kwargs):
        super().__init__(
            app,
            "مقایسه کالا",
            **kwargs
        )

        self.add_widget(
            label(
                "⚖️ مقایسه کالا",
                22,
                True
            )
        )

        self.add_widget(
            label(
                "در این بخش می‌توانید دو یا چند کالا را "
                "از نظر قیمت، مشخصات و ارزش خرید مقایسه کنید.",
                17
            )
        )

        self.add_widget(
            button(
                "افزودن کالا",
                self.add_product
            )
        )

        self.add_widget(Widget())

    def add_product(self, *_):
        pass


class FavoritesPage(Page):

    def __init__(self, app, **kwargs):
        super().__init__(
            app,
            "علاقه‌مندی‌ها",
            **kwargs
        )

        self.add_widget(
            label(
                "⭐ علاقه‌مندی‌ها",
                22,
                True
            )
        )

        self.add_widget(
            label(
                "هنوز کالایی ذخیره نشده است.",
                17
            )
        )

        self.add_widget(Widget())


class ShoppingListPage(Page):

    def __init__(self, app, **kwargs):
        super().__init__(
            app,
            "لیست خرید",
            **kwargs
        )

        self.add_widget(
            label(
                "🛍️ لیست خرید",
                22,
                True
            )
        )

        self.add_widget(
            label(
                "لیست خرید شما در این بخش مدیریت خواهد شد.",
                17
            )
        )

        self.add_widget(Widget())


class SettingsPage(Page):

    def __init__(self, app, **kwargs):
        super().__init__(
            app,
            "تنظیمات",
            **kwargs
        )

        self.add_widget(
            button("🌐 زبان: فارسی")
        )

        self.add_widget(
            button("🔔 اعلان‌ها")
        )

        self.add_widget(
            button("🎨 ظاهر برنامه")
        )

        self.add_widget(
            label(
                "نسخه برنامه: " + APP_VERSION,
                15
            )
        )

        self.add_widget(Widget())


class AboutPage(Page):

    def __init__(self, app, **kwargs):
        super().__init__(
            app,
            "درباره خریدیار",
            **kwargs
        )

        scroll = ScrollView()

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(10),
            size_hint_y=None
        )

        content.bind(
            minimum_height=content.setter(
                "height"
            )
        )

        content.add_widget(
            label(
                "🛒 خریدیار",
                28,
                True,
                (0.05, 0.20, 0.45, 1)
            )
        )

        content.add_widget(
            label(
                "خریدیار یک دستیار هوشمند خرید است "
                "که برای کمک به پیدا کردن، بررسی و "
                "انتخاب بهتر کالاها ساخته شده است.",
                17
            )
        )

        content.add_widget(
            label(
                "👨‍💻 سازنده\n\n"
                "عبدالله جعفری",
                18,
                True
            )
        )

        content.add_widget(
            label(
                "نسخه " + APP_VERSION,
                15
            )
        )

        scroll.add_widget(content)

        self.add_widget(scroll)


class KharidYarApp(App):

    title = APP_NAME

    def build(self):

        self.root_layout = BoxLayout(
            orientation="horizontal"
        )

        self.menu = None

        self.content = BoxLayout(
            orientation="vertical"
        )

        self.root_layout.add_widget(
            self.content
        )

        self.pages = {
            "home": HomePage(self),
            "ai": AIPage(self),
            "search": SearchPage(self),
            "compare": ComparePage(self),
            "favorites": FavoritesPage(self),
            "shopping_list": ShoppingListPage(self),
            "settings": SettingsPage(self),
            "about": AboutPage(self),
        }

        self.show_page("home")

        return self.root_layout

    def open_menu(self):

        if self.menu is not None:
            return

        self.menu = KharidYarMenu(
            on_page_selected=self.show_page,
            on_close=self.close_menu
        )

        self.root_layout.add_widget(
            self.menu,
            index=0
        )

    def close_menu(self):

        if self.menu is None:
            return

        if self.menu.parent is not None:
            self.root_layout.remove_widget(
                self.menu
            )

        self.menu = None

    def show_page(self, page_name):

        page = self.pages.get(page_name)

        if page is None:
            return

        self.close_menu()

        self.content.clear_widgets()

        self.content.add_widget(page)


if __name__ == "__main__":
    KharidYarApp().run()
