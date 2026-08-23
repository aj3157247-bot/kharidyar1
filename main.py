# -*- coding: utf-8 -*-

import os
import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


# ============================================================
# تنظیمات اولیه
# ============================================================

APP_NAME = "خریدیار"
APP_VERSION = "1.0.0"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
FONT_PATH = os.path.join(ASSETS_DIR, "Vazirmatn-Regular.ttf")

# اطلاعات سازنده
CREATOR_NAME = "عبدالله جعفری"

# در صورت اجرای دسکتاپ، رنگ پس‌زمینه پنجره
try:
    Window.clearcolor = (0.96, 0.97, 0.98, 1)
except Exception:
    pass


# ============================================================
# فونت فارسی
# ============================================================

if os.path.exists(FONT_PATH):
    try:
        LabelBase.register(
            name="PersianFont",
            fn_regular=FONT_PATH
        )
        DEFAULT_FONT = "PersianFont"
    except Exception:
        DEFAULT_FONT = "Roboto"
else:
    DEFAULT_FONT = "Roboto"


# ============================================================
# ابزارهای UI
# ============================================================

def make_label(
    text="",
    font_size=16,
    bold=False,
    halign="right",
    valign="middle",
    color=(0.08, 0.09, 0.12, 1),
):
    label = Label(
        text=text,
        font_name=DEFAULT_FONT,
        font_size=dp(font_size),
        color=color,
        halign=halign,
        valign=valign,
        bold=bold,
    )

    label.bind(
        size=lambda instance, value: setattr(
            instance, "text_size", value
        )
    )

    return label


def make_button(
    text,
    callback=None,
    height=50,
    font_size=16,
):
    button = Button(
        text=text,
        font_name=DEFAULT_FONT,
        font_size=dp(font_size),
        size_hint_y=None,
        height=dp(height),
        background_normal="",
        background_color=(0.12, 0.45, 0.95, 1),
        color=(1, 1, 1, 1),
    )

    if callback:
        button.bind(on_release=callback)

    return button


# ============================================================
# صفحه پایه
# ============================================================

class BasePage(BoxLayout):

    def __init__(self, app, **kwargs):
        super().__init__(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(15),
            **kwargs
        )

        self.app = app

        # عنوان
        title = make_label(
            APP_NAME,
            font_size=25,
            bold=True,
            halign="right",
            color=(0.05, 0.20, 0.45, 1),
        )

        title.size_hint_y = None
        title.height = dp(55)

        self.add_widget(title)


# ============================================================
# صفحه اصلی
# ============================================================

class HomePage(BasePage):

    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)

        welcome = make_label(
            "به خریدیار خوش آمدید 👋",
            font_size=23,
            bold=True,
        )

        welcome.size_hint_y = None
        welcome.height = dp(60)

        self.add_widget(welcome)

        description = make_label(
            "دستیار هوشمند خرید برای پیدا کردن، بررسی و مقایسه کالاها.",
            font_size=17,
        )

        description.size_hint_y = None
        description.height = dp(70)

        self.add_widget(description)

        self.add_widget(
            make_button(
                "🤖 دستیار هوشمند",
                lambda *_: app.show_page("ai"),
            )
        )

        self.add_widget(
            make_button(
                "🔎 جستجوی کالا",
                lambda *_: app.show_page("search"),
            )
        )

        self.add_widget(
            make_button(
                "⭐ علاقه‌مندی‌ها",
                lambda *_: app.show_page("favorites"),
            )
        )

        self.add_widget(Label())


# ============================================================
# صفحه جستجو
# ============================================================

class SearchPage(BasePage):

    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)

        title = make_label(
            "🔎 جستجوی کالا",
            font_size=21,
            bold=True,
        )

        title.size_hint_y = None
        title.height = dp(50)

        self.add_widget(title)

        self.search_input = TextInput(
            hint_text="نام کالا را وارد کنید...",
            font_name=DEFAULT_FONT,
            font_size=dp(17),
            multiline=False,
            halign="right",
            size_hint_y=None,
            height=dp(55),
            padding=[dp(12), dp(12)],
        )

        self.add_widget(self.search_input)

        self.add_widget(
            make_button(
                "جستجو",
                self.perform_search,
            )
        )

        self.result_label = make_label(
            "نتایج جستجو در این قسمت نمایش داده می‌شود.",
            font_size=16,
        )

        self.result_label.size_hint_y = None
        self.result_label.height = dp(150)

        self.add_widget(self.result_label)

        self.add_widget(Label())

    def perform_search(self, *_):
        query = self.search_input.text.strip()

        if not query:
            self.result_label.text = (
                "لطفاً ابتدا نام کالا را وارد کنید."
            )
            return

        self.result_label.text = (
            "🔎 در حال بررسی:\n\n"
            + query
            + "\n\n"
            "در نسخه بعدی، نتایج واقعی فروشگاه‌ها و مقایسه قیمت "
            "به این بخش متصل خواهد شد."
        )


# ============================================================
# صفحه دستیار AI
# ============================================================

class AIPage(BasePage):

    busy = BooleanProperty(False)

    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)

        title = make_label(
            "🤖 دستیار هوشمند خریدیار",
            font_size=21,
            bold=True,
        )

        title.size_hint_y = None
        title.height = dp(50)

        self.add_widget(title)

        self.chat_scroll = ScrollView(
            size_hint=(1, 1)
        )

        self.chat_content = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=None,
        )

        self.chat_content.bind(
            minimum_height=self.chat_content.setter(
                "height"
            )
        )

        self.chat_scroll.add_widget(self.chat_content)

        self.add_widget(self.chat_scroll)

        input_layout = BoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(55),
        )

        self.ai_input = TextInput(
            hint_text="مثلاً: یک گوشی خوب تا ۲۰ میلیون پیشنهاد بده",
            font_name=DEFAULT_FONT,
            font_size=dp(15),
            multiline=False,
            halign="right",
        )

        send_button = make_button(
            "ارسال",
            self.send_message,
            height=55,
            font_size=15,
        )

        send_button.size_hint_x = None
        send_button.width = dp(85)

        input_layout.add_widget(self.ai_input)
        input_layout.add_widget(send_button)

        self.add_widget(input_layout)

        self.add_message(
            "خریدیار",
            "سلام! 👋\nمن دستیار هوشمند خرید شما هستم. "
            "سؤال خود را درباره خرید بپرسید."
        )

    def add_message(self, sender, message):
        box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=dp(8),
            spacing=dp(3),
        )

        sender_label = make_label(
            sender,
            font_size=14,
            bold=True,
        )

        sender_label.size_hint_y = None
        sender_label.height = dp(28)

        message_label = make_label(
            message,
            font_size=15,
            valign="top",
        )

        message_label.size_hint_y = None

        # ارتفاع تقریبی برای متن
        lines = max(
            2,
            message.count("\n") + 1
        )

        message_label.height = dp(35 * lines)

        box.add_widget(sender_label)
        box.add_widget(message_label)

        self.chat_content.add_widget(box)

        Clock.schedule_once(
            lambda *_: setattr(
                self.chat_scroll,
                "scroll_y",
                0
            ),
            0.05
        )

    def send_message(self, *_):
        if self.busy:
            return

        text = self.ai_input.text.strip()

        if not text:
            return

        self.ai_input.text = ""

        self.add_message(
            "شما",
            text
        )

        self.busy = True

        threading.Thread(
            target=self.process_ai,
            args=(text,),
            daemon=True,
        ).start()

    def process_ai(self, text):
        # فعلاً پاسخ محلی و سبک.
        # اتصال واقعی AI در ai/assistant.py قرار می‌گیرد.
        response = self.local_ai_response(text)

        Clock.schedule_once(
            lambda *_: self.finish_ai(response),
            0
        )

    def finish_ai(self, response):
        self.add_message(
            "خریدیار 🤖",
            response
        )

        self.busy = False

    @staticmethod
    def local_ai_response(text):
        lower = text.lower()

        if "گوشی" in text:
            return (
                "حتماً 📱\n"
                "برای پیشنهاد گوشی، بودجه، برند مورد علاقه و "
                "کاربرد اصلی‌تان را بگویید.\n\n"
                "مثلاً:\n"
                "«یک گوشی برای بازی تا ۲۰ میلیون می‌خواهم.»"
            )

        if "لپتاپ" in text or "لپ‌تاپ" in text:
            return (
                "برای انتخاب لپ‌تاپ 💻، بودجه و کاربردتان را بگویید؛ "
                "مثلاً برنامه‌نویسی، بازی، طراحی یا استفاده روزمره."
            )

        if "سلام" in text:
            return (
                "سلام 👋\n"
                "خوش آمدید. چه چیزی می‌خواهید بخرید؟"
            )

        return (
            "سؤال شما دریافت شد ✅\n\n"
            "در نسخه فعلی، پاسخ آزمایشی نمایش داده می‌شود. "
            "اتصال به سرویس هوش مصنوعی واقعی در ماژول AI پروژه "
            "قرار خواهد گرفت."
        )


# ============================================================
# علاقه‌مندی‌ها
# ============================================================

class FavoritesPage(BasePage):

    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)

        title = make_label(
            "⭐ علاقه‌مندی‌ها",
            font_size=21,
            bold=True,
        )

        title.size_hint_y = None
        title.height = dp(55)

        self.add_widget(title)

        text = make_label(
            "هنوز کالایی به علاقه‌مندی‌ها اضافه نشده است.\n\n"
            "در نسخه‌های بعدی می‌توانید کالاهای مورد علاقه خود "
            "را ذخیره و مقایسه کنید.",
            font_size=16,
        )

        self.add_widget(text)

        self.add_widget(Label())


# ============================================================
# تنظیمات
# ============================================================

class SettingsPage(BasePage):

    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)

        title = make_label(
            "⚙️ تنظیمات",
            font_size=21,
            bold=True,
        )

        title.size_hint_y = None
        title.height = dp(55)

        self.add_widget(title)

        self.add_widget(
            make_button(
                "🌐 زبان: فارسی",
                self.language_message,
            )
        )

        self.add_widget(
            make_button(
                "🔔 اعلان‌ها",
                self.notification_message,
            )
        )

        self.add_widget(
            make_button(
                "ℹ️ نسخه برنامه: " + APP_VERSION,
                None,
            )
        )

        self.add_widget(Label())

    def language_message(self, *_):
        pass

    def notification_message(self, *_):
        pass


# ============================================================
# درباره سازنده
# ============================================================

class AboutPage(BasePage):

    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)

        title = make_label(
            "ℹ️ درباره خریدیار",
            font_size=22,
            bold=True,
        )

        title.size_hint_y = None
        title.height = dp(55)

        self.add_widget(title)

        about = make_label(
            "خریدیار\n\n"
            "دستیار هوشمند خرید برای کمک به کاربران در "
            "پیدا کردن و انتخاب بهتر کالاها.\n\n"
            "نسخه: " + APP_VERSION,
            font_size=17,
        )

        about.size_hint_y = None
        about.height = dp(180)

        self.add_widget(about)

        creator = make_label(
            "👨‍💻 سازنده\n\n"
            + CREATOR_NAME,
            font_size=18,
            bold=True,
        )

        creator.size_hint_y = None
        creator.height = dp(130)

        self.add_widget(creator)

        self.add_widget(Label())


# ============================================================
# منوی کناری
# ============================================================

class SideMenu(BoxLayout):

    def __init__(self, app, **kwargs):
        super().__init__(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(12),
            size_hint_x=None,
            width=dp(285),
            **kwargs
        )

        self.app = app

        header = make_label(
            "🛒 خریدیار",
            font_size=25,
            bold=True,
            color=(0.05, 0.20, 0.45, 1),
        )

        header.size_hint_y = None
        header.height = dp(75)

        self.add_widget(header)

        self.add_menu_button(
            "🏠 صفحه اصلی",
            "home"
        )

        self.add_menu_button(
            "🤖 دستیار هوشمند",
            "ai"
        )

        self.add_menu_button(
            "🔎 جستجوی کالا",
            "search"
        )

        self.add_menu_button(
            "⭐ علاقه‌مندی‌ها",
            "favorites"
        )

        self.add_menu_button(
            "⚙️ تنظیمات",
            "settings"
        )

        self.add_widget(Label())

        self.add_menu_button(
            "ℹ️ درباره خریدیار",
            "about"
        )

    def add_menu_button(self, text, page):
        button = Button(
            text=text,
            font_name=DEFAULT_FONT,
            font_size=dp(16),
            size_hint_y=None,
            height=dp(52),
            background_normal="",
            background_color=(0.90, 0.93, 0.97, 1),
            color=(0.06, 0.08, 0.12, 1),
        )

        button.bind(
            on_release=lambda *_: self.app.show_page(page)
        )

        self.add_widget(button)


# ============================================================
# رابط اصلی
# ============================================================

class MainRoot(BoxLayout):

    def __init__(self, app, **kwargs):
        super().__init__(
            orientation="horizontal",
            **kwargs
        )

        self.app = app

        self.menu = SideMenu(app)

        self.content = BoxLayout(
            orientation="vertical"
        )

        self.add_widget(self.menu)
        self.add_widget(self.content)


# ============================================================
# برنامه اصلی
# ============================================================

class KharidYarApp(App):

    title = APP_NAME

    def build(self):
        self.root_layout = MainRoot(self)

        self.pages = {}

        self.create_pages()

        self.show_page("home")

        return self.root_layout

    def create_pages(self):

        self.pages["home"] = HomePage(self)
        self.pages["ai"] = AIPage(self)
        self.pages["search"] = SearchPage(self)
        self.pages["favorites"] = FavoritesPage(self)
        self.pages["settings"] = SettingsPage(self)
        self.pages["about"] = AboutPage(self)

    def show_page(self, page_name):

        if page_name not in self.pages:
            return

        self.root_layout.content.clear_widgets()

        self.root_layout.content.add_widget(
            self.pages[page_name]
        )


# ============================================================
# اجرای برنامه
# ============================================================

if __name__ == "__main__":
    KharidYarApp().run()
