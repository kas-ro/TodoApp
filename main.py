import json

from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IconRightWidget, \
    OneLineRightIconListItem
from kivymd.uix.pickers import MDDatePicker

Window.size = (400, 600)


class TodoApp(MDBoxLayout):
    # list_task = ObjectProperty(None)
    # task = StringProperty()
    # items = StringProperty()
    # def __init__(self, **kwargs):
    #     super(TodoApp, self).__init__(**kwargs)
    #     # self.read_file()
    #     # self.charge_data()
    #     # bg_color=[.1, .5, .6]
    pass


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return TodoApp()

    @staticmethod
    def read_file():
        with open('data.json', 'r') as f:
            datas = json.load(f)
        return datas

    @staticmethod
    def write_file(data):
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)

    def add_task(self):
        data = self.read_file()  # Appelle de la fonction read_file pour recuperer les elements
        tasks = self.root.ids.task.text  # On recupere la saisir de l'utilisateur
        if tasks.capitalize() in data:
            toast(f"{tasks} est deja dans votre liste de course !")
            return True
        if self.root.ids.task.text == '':
            toast("Le champ de texte vide !")
        else:
            data.append(tasks.capitalize())
            self.write_file(data)
            toast(f"{tasks.capitalize()} ajouter avec succes !")
            items = OneLineRightIconListItem(
                IconRightWidget(icon='trash-can-outline', on_press=self.remove_item, icon_color='red',
                                    theme_icon_color="Custom"),
                # on_press=self.remove_items,
                text=f'{tasks.capitalize()}',
                theme_text_color='Custom',
                text_color='white'
            )
            self.root.ids.list_task.add_widget(items)
            self.root.ids.task.text = ''

            # Supprimer un element de la liste

    def remove_item(self, instance):
        data = self.read_file()
        data.remove(instance.parent.parent.text)
        self.write_file(data)
        print("Le nom de l'element est: ", instance.parent.parent.text)
        toast(f"{instance.parent.parent.text} supprimer avec succes !")
        self.root.ids.list_task.remove_widget(instance.parent.parent)

    # Show date selected
    def show_date_picker(self):
        date_dialog = MDDatePicker(title_input="Selction la date",
                                   title="Selection la date",
                                   radius=[15, 15, 15, 15],
                                   mode="picker",
                                   min_year=2022,
                                   max_year=2035)

        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    # Recuperer la date selction
    def on_save(self, instance, value, date_range):
        print(f"Instance: {instance}, Valeur: {value}, Date: {date_range}")
        month = value.month
        day = value.day
        year = value.year
        self.root.ids.date_text.text = f"{day}/{month}/{year}"
        self.root.ids.date_text.line_color_focus = 'green'

    # Quitter la boite de dialogue une fois la date selectionner
    @staticmethod
    def on_cancel(instance, value):
        print(f"Instance: {instance}, Valeur: {value}")

    # Show the elements
    def on_start(self):
        # self.fps_monitor_start()
        datas = self.read_file()

        for element in datas:
            items = OneLineRightIconListItem(
                IconRightWidget(icon='trash-can-outline', on_press=self.remove_item, icon_color='red',
                                    theme_icon_color="Custom"),
                                    # on_press=self.remove_items,
                                    text=f'{element}',
                                    theme_text_color='Custom',
                                    text_color='white'
            )
            self.root.ids.list_task.add_widget(items)


if __name__ == '__main__':
    MainApp().run()
