import json

from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IconRightWidget, \
    OneLineRightIconListItem
from kivymd.uix.pickers import MDDatePicker

from database import Database

db = Database()


# db.create_task("Pomme")
# db.create_task("Mangue")
# db.create_task("Piment")


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


    def add_task(self):
        tasks = self.root.ids.task.text  # On recupere la saisir de l'utilisateur
        if self.root.ids.task.text == '':
            toast("Le champ de texte vide !")
        else:
            db.create_task(tasks.capitalize())
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
        toast(f"{instance.parent.parent.text} supprimer avec succes !")
        self.root.ids.list_task.remove_widget(instance.parent.parent)
        db.delete_task(instance.parent.parent.text)




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
        data = db.get_tasks()
        if data != []:
            for element in data:
                items = OneLineRightIconListItem(
                    IconRightWidget(icon='trash-can-outline', on_press=self.remove_item, icon_color='red',
                                        theme_icon_color="Custom"),
                                        # on_press=self.remove_items,
                                        text=f'{element[0]}',
                                        theme_text_color='Custom',
                                        text_color='white'
                )
                self.root.ids.list_task.add_widget(items)


if __name__ == '__main__':
    MainApp().run()
