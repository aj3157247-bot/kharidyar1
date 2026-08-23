# -*- coding: utf-8 -*-

import os
import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget


# ============================================================
# KharidYar - Version 1.0.0
# ============================================================

APP_NAME = "خریدیار"
APP_VERSION = "1.0.0"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
FONT_PATH = os.path.join(ASSETS_DIR, "Vazirmatn-Regular.ttf")


# ============================================================
# فونت فارسی
# ============================================================

DEFAULT_FONT = "Roboto"

if os.path.exists(FONT_PATH):
    try:
        LabelBase.register(
            name="KharidYarFont",
            fn_regular=FONT_PATH,
        )
        DEFAULT_FONT = "KharidYarFont"
    except Exception:
        pass


# ============================================================
# ابزارهای رابط کاربری
# ============================================================

def create_label(
    text="",
    font_size=16,
    bold=False,
    color=(0.08, 0.09, 0.12, 1),
):
    label = Label(
        text=text,
        font_name=DEFAULT_FONT,
        font_size=dp(font_size),
        color=color,
        bold=bold,
        halign="right",
        valign="middle",
    )

    label.bind(
        size=lambda instance, value:
        setattr(instance, "text_size", value)
    )

    return label


def create_button(
    text,
    callback=None,
    height=52,
    background=(0.10, 0.42, 0.90, 1),
    font_size=16,
):
    button = Button(
        text=text,
        font_name=DEFAULT_FONT,
        font_size=dp(font_size),
        color=(1, 1, 1, 1),
        background_normal="",
        background_color=background,
        size_hint_y=None,
        height=dp(height),
    )

    if callback:
        button.bind(on_release=callback)

    return button


# ============================================================
# صفحه پایه
# ============================================================

class Page(BoxLayout):

    def __init__(self, app, title, **kwargs):
        super().__init__(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(16),
            **kwargs
        )

        self.app = app

        header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(58),
            spacing=dp(8),
        )

        menu_button = create_button(
            "☰",
            self.open_menu,
            height=50,
            background=(0.10, 0.42, 0.90, 1),
            font_size=22,
        )

        menu_button.size_hint_x = None
        menu_button.width = dp(58)

        header.add_widget(menu_button)

        title_label = create_label(
            title,
            font_size=22,
            bold=True,
            color=(0.05, 0.20, 0.45, 1),
        )

        header.add_widget(title_label)

        self.add_widget(header)

    def open_menu(self, *_):
        self.app.toggle_menu()


# ============================================================
# صفحه خانه
# ============================================================

class HomePage(Page):

    def __init__(self, app, **kwargs):
        super().__init__(
            app,
            "خریدیار",
            **kwargs
        )

        welcome = create_label(
            "خوش آمدید 👋",
            font_size=25,
            bold=True,
            color=(0.05, 0.20, 0.45, 1),
        )

        welcome.size_hint_y = None
        welcome.height = dp(60)

        self.add_widget(welcome)

        intro = create_label(
            "دستیار هوشمند خرید شما برای پیدا کردن، "
            "بررسی و انتخاب بهتر کالاها.",
            font_size=17,
        )

        intro.size_hint_y = None
        intro.height = dp(75)

        self.add_widget(intro)

        self.add_widget(
            create_button(
                "🤖  دستیار هوشمند",
                lambda *_: app.show_page("ai"),
            )
        )

        self.add_widget(
            create_button(
                "🔎  جستجوی کالا",
                lambda *_: app.show_page("search"),
            )
        )

        self.add_widget(
            create_button(
                "⭐  علاقه‌مندی‌ها",
                lambda *_: app.show_page("favorites"),
            )
        )

        self.add_widget(Widget())


# ============================================================
# صفحه جستجو
# ============================================================

class SearchPage(Page):

    def __init__(self, app, **kwargs):
        super().__init__(
            app,
            "جستجوی کالا",
            **kwargs
        )

        self.input = TextInput(
            hint_text="نام کالا را وارد کنید...",
            font_name=DEFAULT_FONT,
            font_size=dp(17),
            multiline=False,
            halign="right",
            size_hint_y=None,
            height=dp(55),
            padding=[dp(12), dp(12)],
        )

        self.add_widget(self.input)

        self.add_widget(
            create_button(
                "🔎 جستجو",
                self.search,
            )
        )

        self.result = create_label(
            "نتایج جستجو اینجا نمایش داده می‌شود.",
            font_size=16,
        )

        self.result.size_hint_y = None
        self.result.height = dp(180)

        self.add_widget(self.result)

        self.add_widget(Widget())

    def search(self, *_):
        query = self.input.text.strip()

        if not query:
            self.result.text = (
                "لطفاً نام کالای موردنظر را وارد کنید."
            )
            return

        self.result.text = (
            "🔎 جستجو برای:\n\n"
            + query
            + "\n\n"
            "سیستم مقایسه کالا در مرحله بعد "
            "به سرویس‌های واقعی متصل خواهد شد."
        )


# ============================================================
# صفحه هوش مصنوعی
# ============================================================

class AIPage(Page):

    def __init__(self, app, **kwargs):
        super().__init__(
            app,
            "دستیار هوشمند",
            **kwargs
        )

        self.busy = False

        self.messages = ScrollView()

        self.message_box = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(8),
            size_hint_y=None,
        )

        self.message_box.bind(
            minimum_height=self.message_box.setter(
                "height"
            )
        )

        self.messages.add_widget(
            self.message_box
        )

        self.add_widget(self.messages)

        input_bar = BoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(58),
        )

        self.input = TextInput(
            hint_text="سؤال خود را درباره خرید بنویسید...",
            font_name=DEFAULT_FONT,
            font_size=dp(15),
            multiline=False,
            halign="right",
        )

        input_bar.add_widget(self.input)

        send = create_button(
            "ارسال",
            self.send,
            height=58,
            font_size=15,
        )

        send.size_hint_x = None
        send.width = dp(85)

        input_bar.add_widget(send)

        self.add_widget(input_bar)

        self.add_message(
            "خریدیار 🤖",
            "سلام! 👋\n"
            "من دستیار هوشمند خریدیار هستم.\n"
            "می‌توانی درباره انتخاب و خرید کالا از من سؤال کنی."
        )

    def add_message(self, sender, text):

        container = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=dp(8),
        )

        sender_label = create_label(
            sender,
            font_size=14,
            bold=True,
            color=(0.05, 0.20, 0.45, 1),
        )

        sender_label.size_hint_y = None
        sender_label.height = dp(30)

        message_label = create_label(
            text,
            font_size=15,
        )

        # ارتفاع مناسب برای پیام
        line_count = max(
            2,
            text.count("\n") + 1
        )

        message_label.size_hint_y = None
        message_label.height = dp(
            32 * line_count
        )

        container.height = (
            sender_label.height +
            message_label.height +
            dp(16)
        )

        container.add_widget(sender_label)
        container.add_widget(message_label)

        self.message_box.add_widget(container)

        Clock.schedule_once(
            self.scroll_bottom,
            0.05
        )

    def scroll_bottom(self, *_):
        self.messages.scroll_y = 0

    def send(self, *_):

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

        thread = threading.Thread(
            target=self.ai_worker,
            args=(text,),
            daemon=True,
        )

        thread.start()

    def ai_worker(self, text):

        # این بخش فعلاً یک موتور آزمایشی سبک است.
        # اتصال API واقعی AI در فایل ai/assistant.py
        # انجام خواهد شد.

        response = self.generate_demo_response(text)

        Clock.schedule_once(
            lambda *_:
            self.ai_finished(response),
            0
        )

    def ai_finished(self, response):

        self.add_message(
            "خریدیار 🤖",
            response
        )

        self.busy = False

    @staticmethod
    def generate_demo_response(text):

        if "سلام" in text:
            return (
                "سلام 👋\n"
                "خوش آمدی! چه چیزی می‌خواهی بخری؟"
            )

        if "گوشی" in text:
            return (
                "برای انتخاب گوشی 📱، بودجه و کاربردت را بگو.\n\n"
                "مثلاً:\n"
                "«یک گوشی مناسب بازی تا ۲۰ میلیون می‌خواهم.»"
            )

        if "لپ" in text:
            return (
                "برای انتخاب لپ‌تاپ 💻، بودجه و کاربرد اصلی "
                "را بگو؛ مثلاً برنامه‌نویسی، بازی یا کار روزمره."
            )

        if "تلویزیون" in text:
            return (
                "برای انتخاب تلویزیون 📺، اندازه صفحه، بودجه "
                "و برند مورد علاقه‌ات را بگو."
            )

        return (
            "سؤال شما دریافت شد ✅\n\n"
            "در نسخه نهایی، این قسمت به هوش مصنوعی واقعی "
            "خریدیار متصل می‌شود تا بتواند سؤال شما را تحلیل "
            "و برای خرید پیشنهاد مناسب ارائه کند."
        )


# ============================================================
# علاقه‌مندی‌ها
# ============================================================

class FavoritesPage(Page):

    def __init__(self, app, **kwargs):
        super().__init__(
            app,
            "علاقه‌مندی‌ها",
            **kwargs
        )

        label = create_label(
            "⭐ هنوز کالایی ذخیره نشده است.\n\n"
            "کالاهای مورد علاقه شما در این قسمت "
            "ذخیره خواهند شد.",
            font_size=17,
        )

        self.add_widget(label)

        self.add_widget(Widget())


# ============================================================
# تنظیمات
# ============================================================

class SettingsPage(Page):

    def __init__(self, app, **kwargs):
        super().__init__(
            app,
            "تنظیمات",
            **kwargs
        )

        self.add_widget(
            create_button(
                "🌐 زبان: فارسی",
                self.language,
            )
        )

        self.add_widget(
            create_button(
                "🔔 اعلان‌ها",
                self.notifications,
            )
        )

        self.add_widget(
            create_button(
                "🎨 ظاهر برنامه",
                self.appearance,
            )
        )

        version = create_label(
            "نسخه خریدیار: " + APP_VERSION,
            font_size=16,
        )

        version.size_hint_y = None
        version.height = dp(60)

        self.add_widget(version)

        self.add_widget(Widget())

    def language(self, *_):
        pass

    def notifications(self, *_):
        pass

    def appearance(self, *_):
        pass


# ============================================================
# درباره برنامه
# ============================================================

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
            spacing=dp(15),
            padding=dp(10),
            size_hint_y=None,
        )

        content.bind(
            minimum_height=content.setter(
                "height"
            )
        )

        title = create_label(
            "🛒 خریدیار",
            font_size=28,
            bold=True,
            color=(0.05, 0.20, 0.45, 1),
        )

        title.size_hint_y = None
        title.height = dp(70)

        content.add_widget(title)

        description = create_label(
            "خریدیار یک دستیار هوشمند خرید است که "
            "برای کمک به پیدا کردن، بررسی و انتخاب بهتر "
            "کالاها طراحی شده است.",
            font_size=17,
        )

        description.size_hint_y = None
        description.height = dp(130)

        content.add_widget(description)

        creator = create_label(
            "👨‍💻 سازنده\n\n"
            "عبدالله جعفری",
            font_size=18,
            bold=True,
        )

        creator.size_hint_y = None
        creator.height = dp(120)

        content.add_widget(creator)

        version = create_label(
            "نسخه " + APP_VERSION,
            font_size=15,
        )

        version.size_hint_y = None
        version.height = dp(50)

        content.add_widget(version)

        scroll.add_widget(content)

        self.add_widget(scroll)


# ============================================================
# منوی کناری
# ============================================================

class SideMenu(BoxLayout):

    def __init__(self, app, **kwargs):

        super().__init__(
            orientation="vertical",
            spacing=dp(7),
            padding=dp(12),
            size_hint_x=None,
            width=dp(285),
            **kwargs
        )

        self.app = app

        header = create_label(
            "🛒 خریدیار",
            font_size=25,
            bold=True,
            color=(0.05, 0.20, 0.45, 1),
        )

        header.size_hint_y = None
        header.height = dp(70)

        self.add_widget(header)

        self.menu_item(
            "🏠 صفحه اصلی",
            "home"
        )

        self.menu_item(
            "🤖 دستیار هوشمند",
            "ai"
        )

        self.menu_item(
            "🔎 جستجوی کالا",
            "search"
        )

        self.menu_item(
            "⭐ علاقه‌مندی‌ها",
            "favorites"
        )

        self.menu_item(
            "⚙️ تنظیمات",
            "settings"
        )

        self.add_widget(Widget())

        self.menu_item(
            "ℹ️ درباره خریدیار",
            "about"
        )

    def menu_item(self, text, page):

        button = Button(
            text=text,
            font_name=DEFAULT_FONT,
            font_size=dp(16),
            color=(0.05, 0.07, 0.10, 1),
            background_normal="",
            background_color=(0.91, 0.94, 0.98, 1),
            size_hint_y=None,
            height=dp(52),
        )

        button.bind(
            on_release=lambda *_:
            self.app.select_menu(page)
        )

        self.add_widget(button)


# ============================================================
# ریشه برنامه
# ============================================================

class RootLayout(BoxLayout):

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
# برنامه
# ============================================================

class KharidYarApp(App):

    title = APP_NAME

    def build(self):

        self.root_layout = RootLayout(self)

        self.pages = {
            "home": HomePage(self),
            "ai": AIPage(self),
            "search": SearchPage(self),
            "favorites": FavoritesPage(self),
            "settings": SettingsPage(self),
            "about": AboutPage(self),
        }

        self.show_page("home")

        return self.root_layout

    def show_page(self, page_name):

        page = self.pages.get(page_name)

        if page is None:
            return

        self.root_layout.content.clear_widgets()

        self.root_layout.content.add_widget(page)

    def select_menu(self, page_name):

        self.show_page(page_name)

    def toggle_menu(self):

        menu = self.root_layout.menu

        if menu.parent is not None:
            self.root_layout.remove_widget(menu)
        else:
            self.root_layout.add_widget(
                menu,
                index=0
            )


# ============================================================
# اجرای برنامه
# ============================================================

if __name__ == "__main__":
    KharidYarApp().run()
