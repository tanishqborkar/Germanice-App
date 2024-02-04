from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.textfield import MDTextFieldRound
from mst import genderGetter
from random import choice
from kivy.core.window import Window
from googletrans import Translator
from kivy.properties import ListProperty, BooleanProperty,  StringProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview import RecycleViewBehavior
from kivy.core.text import LabelBase
from kivmob import KivMob, TestIds

from kivymd.uix.dialog import MDDialog

LabelBase.register(name="thin", fn_regular='fonts/thinfon-bold.otf')
LabelBase.register(name='trans', fn_regular='fonts/Thicker-Regular-trial.ttf')


class TryAgainScreen(Screen):
    def show_ad(self):
        GermanApp.ads.show_interstitial()


class MenuScreen(Screen):
    pass


class GenderGameScreen(Screen):

    def build(self):
        self.noun = choice(list(genderGetter().keys()))

        return str(self.noun)

    def correcter_der(self):
        if str(self.ids.der.text) == genderGetter().get(str(self.noun)):
            self.gender_setup_correct()

        else:

            self.ids.der.disabled = True
            self.gender_setup_wrong()

    def correcter_das(self):
        if str(self.ids.das.text) == genderGetter().get(str(self.noun)):
            self.gender_setup_correct()
        else:

            self.ids.das.disabled = True
            self.gender_setup_wrong()

    def correcter_die(self):
        if str(self.ids.die.text) == genderGetter().get(str(self.noun)):
            self.gender_setup_correct()
        else:
            self.ids.die.disabled = True
            self.gender_setup_wrong()

    def show_res(self):
        if self.ids.show_label.text == 'Correct':
            self.ids.quiz_label.text = "What is the gender of" + " " + f"[b][color=de14a6ff]{self.build()}  [/color][/b]"
            self.activate()
            self.show_chances()  # show the result and get new word after next button is clicked

            self.ids.show_label.text = " "

    def show_score(self):
        self.points = 0
        self.ids.point_system.text = f"Score : {self.points}"  # show the score

    def show_chances(self):
        self.chances = 2  # show the no. of chances
        self.ids.chances.text = f"Chances : {self.chances}"

    def disabler(self):
        self.ids.der.disabled = True
        self.ids.das.disabled = True  # deactivate gender buttons
        self.ids.die.disabled = True

    def activate(self):
        self.ids.der.disabled = False
        self.ids.das.disabled = False  # activate gender buttons
        self.ids.die.disabled = False

    def next_button_shower(self):  # activate next button
        self.ids.next_button.opacity = 1
        self.ids.next_button.disabled = False

    def next_button_hider(self):
        self.ids.next_button.opacity = 0
        self.ids.next_button.disabled = True  # deactivate next button

    def gender_setup_correct(self):
        self.ids.show_label.text = "Correct"
        self.disabler()
        self.next_button_shower()
        self.points += 1  # logic of gender input ..important
        self.ids.point_system.text = f"Score : {self.points}"

    def gender_setup_wrong(self):
        self.ids.show_label.text = "Wrong"
        self.chances -= 1
        self.ids.chances.text = f"Chances : {self.chances}"

    def get_chances(self):
        return self.chances

    def request_ad(self):
        GermanApp.ads.request_interstitial()


class GenderScreen(Screen):
    pass


class GenderText(MDTextFieldRound):
    words = ListProperty(genderGetter().keys())
    gen = ListProperty(genderGetter().values())
    items = ListProperty([])

    def __init__(self, **kwargs):
        super(GenderText, self).__init__(**kwargs)

    def get_len(self):
        return len(self.get_text())

    def on_text(self, instance, value):

        self.parent.ids.rv.data = []
        if not value:
            self.parent.ids.rv.data = []

        matches = [self.words[i] for i in range(len(self.words)) if
                   self.words[i].startswith(self.text.capitalize())]
        display_data = []
        for i in matches:
            display_data.append(
                {'text': str(i) + "    " + "({gender})".format(
                    gender=genderGetter().get(str(i)))})
        self.parent.ids.rv.data = display_data
        if len(matches) <= 10:
            self.parent.height = (10 + (len(matches) * 20))
        else:
            self.parent.height = 240

    def do_backspace(self, from_undo=False, mode='bkspc'):
        self.parent.ids.rv.data = []
        self.text = self.text[:-1]
        if len(self.text) >= 1:

            matches = [self.words[i] for i in range(len(self.words)) if
                       self.words[i].startswith(self.text.capitalize())]
            display_data = []
            for i in matches:
                display_data.append({'text': str(i) + "    " + '({gender})'.format(gender=genderGetter().get(str(i)))})
            self.parent.ids.rv.data = display_data

            if len(matches) <= 10:
                self.parent.height = (10 + (len(matches) * 20))
            else:
                self.parent.height = 240
            return True
        elif len(self.text) == 0:
            self.parent.ids.rv.data = []

        return super(GenderText, self).do_backspace(from_undo, mode)





class TranslatorScreen(Screen):
    src = StringProperty('de')
    dest = StringProperty('en')
    dialog = None

    def switch(self):
        self.ids.left_side_button.text, self.ids.right_side_button.text = \
            self.ids.right_side_button.text, self.ids.left_side_button.text
        if self.ids.left_side_button.text == 'English':
            self.src = 'en'
            self.dest = 'de'
        else:
            self.src = 'de'
            self.dest = 'en'

    def show_data(self):
        if not self.dialog:
            self.dialog = MDDialog(title="Internet Error", text="connect to wifi or mobile data")
        self.dialog.open()

    def translate(self):
        try:
            if self.ids.left_text.text != " ":
                left_txt = str(self.ids.left_text.text)
                self.ids.right_text.text = Translator().translate(left_txt, dest=self.dest, src=self.src).text
            else:
                return
        except:
            self.show_data()


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    pass


class RefreshData(RecycleViewBehavior):
    pass


class SelectableLabel(RecycleDataViewBehavior, Label):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):

        self.index = index

        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):

        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):

        self.selected = is_selected
        if is_selected:
            pass


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)


class NotesScreen(Screen):
    pass


class GermanApp(MDApp):
    ads = KivMob("ca-app-pub-8486452407734047~5985885938")


    def build(self):
        screen = Builder.load_file('main.kv')
        self.ads.new_interstitial("ca-app-pub-8486452407734047/7520305367")
        return screen

    def on_start(self):
        Window.release_all_keyboards()


class PersonalPronouns(Screen):
    pass


class VerbForms(Screen):
    pass


class NounArticle(Screen):
    pass


class Preposition(Screen):
    pass


if __name__ == "__main__":
    app = GermanApp()
    app.run()