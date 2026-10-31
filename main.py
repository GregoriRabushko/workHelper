from datetime import datetime

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget


# =========================================================
# ОБЩИЙ ФОН ПРИЛОЖЕНИЯ
# =========================================================

Window.clearcolor = (0.82, 0.82, 0.82, 1)


# =========================================================
# ВСПОМОГАТЕЛЬНЫЕ КЛАССЫ
# =========================================================

class PaperBox(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        with self.canvas.before:

            Color(
                1,
                1,
                1,
                1
            )

            self.background = Rectangle()

        with self.canvas.after:

            Color(
                0.2,
                0.2,
                0.2,
                1
            )

            self.border_line = Line(
                width=1.2
            )

        self.bind(
            pos=self.update_canvas,
            size=self.update_canvas
        )

        self.update_canvas()

    def update_canvas(self, *args):

        self.background.pos = self.pos
        self.background.size = self.size

        self.border_line.rectangle = (
            self.x,
            self.y,
            self.width,
            self.height
        )


class TableCellLabel(Label):

    def __init__(
        self,
        bg_color=(1, 1, 1, 1),
        **kwargs
    ):

        kwargs.setdefault(
            "color",
            (0, 0, 0, 1)
        )

        kwargs.setdefault(
            "halign",
            "center"
        )

        kwargs.setdefault(
            "valign",
            "middle"
        )

        kwargs.setdefault(
            "font_size",
            14
        )

        super().__init__(**kwargs)

        with self.canvas.before:

            self.bg_color_instruction = Color(
                *bg_color
            )

            self.background = Rectangle()

        with self.canvas.after:

            Color(
                0.15,
                0.15,
                0.15,
                1
            )

            self.border_line = Line(
                width=1
            )

        self.bind(
            pos=self.update_canvas,
            size=self.update_canvas
        )

        self.update_canvas()

    def update_canvas(self, *args):

        self.background.pos = self.pos
        self.background.size = self.size

        self.border_line.rectangle = (
            self.x,
            self.y,
            self.width,
            self.height
        )

        self.text_size = (
            max(self.width - 10, 0),
            max(self.height - 6, 0)
        )


class TableCellInput(TextInput):

    def __init__(self, **kwargs):

        kwargs.setdefault("multiline", False)
        kwargs.setdefault("font_size", 15)

        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_active = ""
        self.background_color = (1, 1, 1, 1)

        self.foreground_color = (0, 0, 0, 1)
        self.cursor_color = (0, 0, 0, 1)

        self.padding = [7, 10, 7, 7]

        with self.canvas.after:
            Color(0.15, 0.15, 0.15, 1)

            self.border_line = Line(
                width=1
            )

        self.bind(
            pos=self.update_canvas,
            size=self.update_canvas
        )

        self.update_canvas()

    def update_canvas(self, *args):

        self.border_line.rectangle = (
            self.x,
            self.y,
            self.width,
            self.height
        )


class AppButton(Button):
    """
    Обычная кнопка приложения.
    """

    def __init__(self, **kwargs):

        kwargs.setdefault("background_normal", "")
        kwargs.setdefault(
            "background_color",
            (0.18, 0.20, 0.23, 1)
        )
        kwargs.setdefault(
            "color",
            (1, 1, 1, 1)
        )
        kwargs.setdefault("font_size", 15)

        super().__init__(**kwargs)


class DeleteButton(Button):
    """
    Кнопка удаления строки.
    """

    def __init__(self, **kwargs):

        kwargs.setdefault("background_normal", "")
        kwargs.setdefault(
            "background_color",
            (0.65, 0.20, 0.20, 1)
        )
        kwargs.setdefault(
            "color",
            (1, 1, 1, 1)
        )

        super().__init__(**kwargs)


# =========================================================
# ЭКРАН РАБОТ
# =========================================================

class WorkScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=10
        )

        # -------------------------------------------------
        # ПАНЕЛЬ УПРАВЛЕНИЯ
        # -------------------------------------------------

        toolbar = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=48,
            spacing=8
        )

        add_button = AppButton(
            text="+ Добавить работу"
        )

        materials_button = AppButton(
            text="Материалы →"
        )

        preview_button = AppButton(
            text="Предпросмотр"
        )

        add_button.bind(
            on_press=self.add_work_row
        )

        materials_button.bind(
            on_press=self.open_materials
        )

        preview_button.bind(
            on_press=self.open_preview
        )

        toolbar.add_widget(add_button)
        toolbar.add_widget(materials_button)
        toolbar.add_widget(preview_button)

        root.add_widget(toolbar)

        # -------------------------------------------------
        # ЛИСТ
        # -------------------------------------------------

        scroll = ScrollView()

        self.paper = PaperBox(
            orientation="vertical",
            size_hint_y=None,
            spacing=0,
            padding=[15, 12, 15, 18]
        )

        self.paper.bind(
            minimum_height=self.paper.setter("height")
        )

        # -------------------------------------------------
        # ЗАГОЛОВОК
        # -------------------------------------------------

        title = Label(
            text="[b]АКТ[/b]",
            markup=True,
            font_size=26,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=48
        )

        self.paper.add_widget(title)

        # -------------------------------------------------
        # ДАТА
        # -------------------------------------------------

        date_row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=38
        )

        date_row.add_widget(
            Widget()
        )

        date_row.add_widget(
            Label(
                text="Дата:",
                color=(0, 0, 0, 1),
                size_hint_x=None,
                width=55
            )
        )

        self.date_input = TableCellInput(
            text=datetime.now().strftime("%d.%m.%Y"),
            size_hint_x=None,
            width=135
        )

        date_row.add_widget(
            self.date_input
        )

        self.paper.add_widget(
            date_row
        )

        # небольшой отступ

        self.paper.add_widget(
            Widget(
                size_hint_y=None,
                height=10
            )
        )

        # -------------------------------------------------
        # ШАПКА ОСНОВНЫХ ДАННЫХ
        # -------------------------------------------------

        info_header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=48,
            spacing=0
        )

        header_color = (
            0.90,
            0.90,
            0.90,
            1
        )

        info_header.add_widget(
            TableCellLabel(
                text="Инвентарный\nномер",
                size_hint_x=0.16,
                bg_color=header_color
            )
        )

        info_header.add_widget(
            TableCellLabel(
                text="Наименование\nтехники",
                size_hint_x=0.30,
                bg_color=header_color
            )
        )

        info_header.add_widget(
            TableCellLabel(
                text="Вид\nдеятельности",
                size_hint_x=0.26,
                bg_color=header_color
            )
        )

        info_header.add_widget(
            TableCellLabel(
                text="Моточасы",
                size_hint_x=0.12,
                bg_color=header_color
            )
        )

        info_header.add_widget(
            TableCellLabel(
                text="Бригада",
                size_hint_x=0.16,
                bg_color=header_color
            )
        )

        self.paper.add_widget(
            info_header
        )

        # -------------------------------------------------
        # ОСНОВНЫЕ ДАННЫЕ
        # -------------------------------------------------

        info_values = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=48,
            spacing=0
        )

        self.inventory_input = TableCellInput(
            size_hint_x=0.16
        )

        self.machine_input = TableCellInput(
            size_hint_x=0.30
        )

        self.activity_input = TableCellInput(
            size_hint_x=0.26
        )

        self.motor_hours_input = TableCellInput(
            size_hint_x=0.12,
            input_filter="float"
        )

        self.brigade_input = TableCellInput(
            size_hint_x=0.16
        )

        info_values.add_widget(
            self.inventory_input
        )
        info_values.add_widget(
            self.machine_input
        )
        info_values.add_widget(
            self.activity_input
        )
        info_values.add_widget(
            self.motor_hours_input
        )
        info_values.add_widget(
            self.brigade_input
        )

        self.paper.add_widget(
            info_values
        )

        self.paper.add_widget(
            Widget(
                size_hint_y=None,
                height=18
            )
        )

        # -------------------------------------------------
        # НАЗВАНИЕ СЕКЦИИ
        # -------------------------------------------------

        section_title = TableCellLabel(
            text="[b]ВЫПОЛНЕННЫЕ РАБОТЫ[/b]",
            markup=True,
            bg_color=header_color,
            size_hint_y=None,
            height=38
        )

        self.paper.add_widget(
            section_title
        )

        # -------------------------------------------------
        # ЗАГОЛОВКИ РАБОТ
        # -------------------------------------------------

        work_header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=42,
            spacing=0
        )

        work_header.add_widget(
            TableCellLabel(
                text="№",
                size_hint_x=0.08,
                bg_color=header_color
            )
        )

        work_header.add_widget(
            TableCellLabel(
                text="Работа",
                size_hint_x=0.67,
                bg_color=header_color
            )
        )

        work_header.add_widget(
            TableCellLabel(
                text="Часы",
                size_hint_x=0.17,
                bg_color=header_color
            )
        )

        # колонка удаления
        work_header.add_widget(
            TableCellLabel(
                text="",
                size_hint_x=0.08,
                bg_color=header_color
            )
        )

        self.paper.add_widget(
            work_header
        )

        # -------------------------------------------------
        # СТРОКИ РАБОТ
        # -------------------------------------------------

        self.works = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=0
        )

        self.works.bind(
            minimum_height=self.works.setter(
                "height"
            )
        )

        self.work_rows = []

        self.add_work_row()

        self.paper.add_widget(
            self.works
        )

        # -------------------------------------------------
        # ИТОГО
        # -------------------------------------------------

        total_row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=44,
            spacing=0
        )

        total_row.add_widget(
            TableCellLabel(
                text="",
                size_hint_x=0.08
            )
        )

        total_row.add_widget(
            TableCellLabel(
                text="[b]Итого[/b]",
                markup=True,
                size_hint_x=0.67,
                halign="right"
            )
        )

        self.total_hours_value = TableCellLabel(
            text="0",
            size_hint_x=0.17
        )

        total_row.add_widget(
            self.total_hours_value
        )

        total_row.add_widget(
            TableCellLabel(
                text="",
                size_hint_x=0.08
            )
        )

        self.paper.add_widget(
            total_row
        )

        scroll.add_widget(
            self.paper
        )

        root.add_widget(
            scroll
        )

        self.add_widget(
            root
        )

    # =====================================================
    # ДОБАВИТЬ РАБОТУ
    # =====================================================

    def add_work_row(self, instance=None):

        row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=46,
            spacing=0
        )

        number = len(self.work_rows) + 1

        number_label = TableCellLabel(
            text=str(number),
            size_hint_x=0.08
        )

        work_input = TableCellInput(
            hint_text="Работа",
            size_hint_x=0.67
        )

        hours_input = TableCellInput(
            hint_text="Часы",
            input_filter="float",
            size_hint_x=0.17
        )

        row_data = {
            "row": row,
            "number": number_label,
            "work": work_input,
            "hours": hours_input
        }

        self.work_rows.append(
            row_data
        )

        hours_input.bind(
            text=self.update_total
        )

        row.add_widget(
            number_label
        )

        row.add_widget(
            work_input
        )

        row.add_widget(
            hours_input
        )

        # ---------------------------------------------
        # ПЕРВУЮ СТРОКУ УДАЛЯТЬ НЕЛЬЗЯ
        # ---------------------------------------------

        if number == 1:

            row.add_widget(
                TableCellLabel(
                    text="",
                    size_hint_x=0.08
                )
            )

        else:

            delete_button = DeleteButton(
                text="X",
                size_hint_x=0.08
            )

            delete_button.bind(
                on_press=lambda button:
                self.delete_work_row(row_data)
            )

            row.add_widget(
                delete_button
            )

        self.works.add_widget(
            row
        )

    # =====================================================
    # УДАЛИТЬ РАБОТУ
    # =====================================================

    def delete_work_row(self, row_data):

        if row_data not in self.work_rows:
            return

        index = self.work_rows.index(
            row_data
        )

        # Дополнительная защита первой строки
        if index == 0:
            return

        self.works.remove_widget(
            row_data["row"]
        )

        self.work_rows.remove(
            row_data
        )

        self.update_work_numbers()
        self.update_total()

    # =====================================================
    # НУМЕРАЦИЯ
    # =====================================================

    def update_work_numbers(self):

        for index, row_data in enumerate(
            self.work_rows,
            start=1
        ):

            row_data["number"].text = str(
                index
            )

    # =====================================================
    # ИТОГО
    # =====================================================

    def update_total(
        self,
        instance=None,
        value=None
    ):

        total = 0

        for row_data in self.work_rows:

            hours = (
                row_data["hours"]
                .text
                .strip()
            )

            if not hours:
                continue

            try:
                total += float(hours)
            except ValueError:
                pass

        self.total_hours_value.text = (
            f"{total:g}"
        )

    # =====================================================
    # НАВИГАЦИЯ
    # =====================================================

    def open_materials(self, instance):
        self.manager.current = "materials"

    def open_preview(self, instance):
        self.manager.current = "preview"


# =========================================================
# ЭКРАН МАТЕРИАЛОВ
# =========================================================

class MaterialsScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=10
        )

        # -------------------------------------------------
        # ПАНЕЛЬ
        # -------------------------------------------------

        toolbar = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=48,
            spacing=8
        )

        works_button = AppButton(
            text="← Работы"
        )

        add_button = AppButton(
            text="+ Добавить материал"
        )

        preview_button = AppButton(
            text="Предпросмотр"
        )

        works_button.bind(
            on_press=self.open_works
        )

        add_button.bind(
            on_press=self.add_material_row
        )

        preview_button.bind(
            on_press=self.open_preview
        )

        toolbar.add_widget(
            works_button
        )
        toolbar.add_widget(
            add_button
        )
        toolbar.add_widget(
            preview_button
        )

        root.add_widget(
            toolbar
        )

        # -------------------------------------------------
        # БУМАГА
        # -------------------------------------------------

        scroll = ScrollView()

        self.paper = PaperBox(
            orientation="vertical",
            size_hint_y=None,
            padding=[15, 15, 15, 18],
            spacing=0
        )

        self.paper.bind(
            minimum_height=self.paper.setter(
                "height"
            )
        )

        title = Label(
            text="[b]ИСПОЛЬЗОВАННЫЕ МАТЕРИАЛЫ[/b]",
            markup=True,
            font_size=22,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=55
        )

        self.paper.add_widget(
            title
        )

        header_color = (
            0.90,
            0.90,
            0.90,
            1
        )

        # -------------------------------------------------
        # ЗАГОЛОВОК ТАБЛИЦЫ
        # -------------------------------------------------

        header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=45,
            spacing=0
        )

        header.add_widget(
            TableCellLabel(
                text="№",
                size_hint_x=0.08,
                bg_color=header_color
            )
        )

        header.add_widget(
            TableCellLabel(
                text="Наименование материала",
                size_hint_x=0.42,
                bg_color=header_color
            )
        )

        header.add_widget(
            TableCellLabel(
                text="Код",
                size_hint_x=0.18,
                bg_color=header_color
            )
        )

        header.add_widget(
            TableCellLabel(
                text="На кого взят",
                size_hint_x=0.24,
                bg_color=header_color
            )
        )

        header.add_widget(
            TableCellLabel(
                text="",
                size_hint_x=0.08,
                bg_color=header_color
            )
        )

        self.paper.add_widget(
            header
        )

        # -------------------------------------------------
        # СТРОКИ
        # -------------------------------------------------

        self.materials = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=0
        )

        self.materials.bind(
            minimum_height=self.materials.setter(
                "height"
            )
        )

        self.material_rows = []

        self.add_material_row()

        self.paper.add_widget(
            self.materials
        )

        scroll.add_widget(
            self.paper
        )

        root.add_widget(
            scroll
        )

        self.add_widget(
            root
        )

    # =====================================================
    # ДОБАВИТЬ МАТЕРИАЛ
    # =====================================================

    def add_material_row(self, instance=None):

        row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=46,
            spacing=0
        )

        number_label = TableCellLabel(
            text=str(
                len(self.material_rows) + 1
            ),
            size_hint_x=0.08
        )

        material_input = TableCellInput(
            hint_text="Материал",
            size_hint_x=0.42
        )

        code_input = TableCellInput(
            hint_text="Код",
            size_hint_x=0.18
        )

        employee_input = TableCellInput(
            hint_text="Фамилия",
            size_hint_x=0.24
        )

        delete_button = DeleteButton(
            text="X",
            size_hint_x=0.08
        )

        row_data = {
            "row": row,
            "number": number_label,
            "material": material_input,
            "code": code_input,
            "employee": employee_input
        }

        self.material_rows.append(
            row_data
        )

        delete_button.bind(
            on_press=lambda button:
            self.delete_material_row(
                row_data
            )
        )

        row.add_widget(
            number_label
        )
        row.add_widget(
            material_input
        )
        row.add_widget(
            code_input
        )
        row.add_widget(
            employee_input
        )
        row.add_widget(
            delete_button
        )

        self.materials.add_widget(
            row
        )

    # =====================================================
    # УДАЛИТЬ МАТЕРИАЛ
    # =====================================================

    def delete_material_row(
        self,
        row_data
    ):

        if row_data not in self.material_rows:
            return

        self.materials.remove_widget(
            row_data["row"]
        )

        self.material_rows.remove(
            row_data
        )

        self.update_material_numbers()

    def update_material_numbers(self):

        for index, row_data in enumerate(
            self.material_rows,
            start=1
        ):

            row_data["number"].text = str(
                index
            )

    # =====================================================
    # НАВИГАЦИЯ
    # =====================================================

    def open_works(self, instance):
        self.manager.current = "works"

    def open_preview(self, instance):
        self.manager.current = "preview"


# =========================================================
# ПРЕДПРОСМОТР
# =========================================================

class PreviewScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=10
        )

        toolbar = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=48,
            spacing=8
        )

        works_button = AppButton(
            text="← Вернуться к редактированию"
        )

        materials_button = AppButton(
            text="Материалы"
        )

        works_button.bind(
            on_press=self.open_works
        )

        materials_button.bind(
            on_press=self.open_materials
        )

        toolbar.add_widget(
            works_button
        )

        toolbar.add_widget(
            materials_button
        )

        root.add_widget(
            toolbar
        )

        self.scroll = ScrollView()

        self.pages = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=25,
            padding=[0, 0, 0, 15]
        )

        self.pages.bind(
            minimum_height=self.pages.setter(
                "height"
            )
        )

        self.scroll.add_widget(
            self.pages
        )

        root.add_widget(
            self.scroll
        )

        self.add_widget(
            root
        )

    # =====================================================
    # ПЕРЕД ПОКАЗОМ ЭКРАНА
    # =====================================================

    def on_pre_enter(self, *args):
        self.build_preview()

    # =====================================================
    # СОЗДАТЬ ПРЕДПРОСМОТР
    # =====================================================

    def build_preview(self):

        self.pages.clear_widgets()

        works_screen = self.manager.get_screen(
            "works"
        )

        materials_screen = self.manager.get_screen(
            "materials"
        )

        self.build_front_page(
            works_screen
        )

        self.build_materials_page(
            materials_screen
        )

    # =====================================================
    # ЛИЦЕВАЯ СТОРОНА
    # =====================================================

    def build_front_page(
        self,
        works_screen
    ):

        paper = PaperBox(
            orientation="vertical",
            size_hint_y=None,
            spacing=0,
            padding=[15, 12, 15, 18]
        )

        paper.bind(
            minimum_height=paper.setter(
                "height"
            )
        )

        # Заголовок

        paper.add_widget(
            Label(
                text="[b]АКТ[/b]",
                markup=True,
                font_size=26,
                color=(0, 0, 0, 1),
                size_hint_y=None,
                height=48
            )
        )

        # Дата

        date_row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=38
        )

        date_row.add_widget(
            Widget()
        )

        date_row.add_widget(
            Label(
                text="Дата:",
                color=(0, 0, 0, 1),
                size_hint_x=None,
                width=55
            )
        )

        date_row.add_widget(
            TableCellLabel(
                text=works_screen.date_input.text,
                size_hint_x=None,
                width=135
            )
        )

        paper.add_widget(
            date_row
        )

        paper.add_widget(
            Widget(
                size_hint_y=None,
                height=10
            )
        )

        header_color = (
            0.90,
            0.90,
            0.90,
            1
        )

        # Основные данные — заголовок

        header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=48,
            spacing=0
        )

        fields = [
            ("Инвентарный\nномер", 0.16),
            ("Наименование\nтехники", 0.30),
            ("Вид\nдеятельности", 0.26),
            ("Моточасы", 0.12),
            ("Бригада", 0.16)
        ]

        for text, width in fields:

            header.add_widget(
                TableCellLabel(
                    text=text,
                    size_hint_x=width,
                    bg_color=header_color
                )
            )

        paper.add_widget(
            header
        )

        # Значения

        values = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=48,
            spacing=0
        )

        data = [
            (
                works_screen.inventory_input.text,
                0.16
            ),
            (
                works_screen.machine_input.text,
                0.30
            ),
            (
                works_screen.activity_input.text,
                0.26
            ),
            (
                works_screen.motor_hours_input.text,
                0.12
            ),
            (
                works_screen.brigade_input.text,
                0.16
            )
        ]

        for text, width in data:

            values.add_widget(
                TableCellLabel(
                    text=text,
                    size_hint_x=width
                )
            )

        paper.add_widget(
            values
        )

        paper.add_widget(
            Widget(
                size_hint_y=None,
                height=18
            )
        )

        paper.add_widget(
            TableCellLabel(
                text="[b]ВЫПОЛНЕННЫЕ РАБОТЫ[/b]",
                markup=True,
                bg_color=header_color,
                size_hint_y=None,
                height=38
            )
        )

        # Заголовок работ

        work_header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=42,
            spacing=0
        )

        work_header.add_widget(
            TableCellLabel(
                text="№",
                size_hint_x=0.08,
                bg_color=header_color
            )
        )

        work_header.add_widget(
            TableCellLabel(
                text="Работа",
                size_hint_x=0.74,
                bg_color=header_color
            )
        )

        work_header.add_widget(
            TableCellLabel(
                text="Часы",
                size_hint_x=0.18,
                bg_color=header_color
            )
        )

        paper.add_widget(
            work_header
        )

        # Строки работ

        for index, row_data in enumerate(
            works_screen.work_rows,
            start=1
        ):

            row = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=46,
                spacing=0
            )

            row.add_widget(
                TableCellLabel(
                    text=str(index),
                    size_hint_x=0.08
                )
            )

            row.add_widget(
                TableCellLabel(
                    text=row_data["work"].text,
                    size_hint_x=0.74,
                    halign="left"
                )
            )

            row.add_widget(
                TableCellLabel(
                    text=row_data["hours"].text,
                    size_hint_x=0.18
                )
            )

            paper.add_widget(
                row
            )

        # Итого

        total_row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=44,
            spacing=0
        )

        total_row.add_widget(
            TableCellLabel(
                text="",
                size_hint_x=0.08
            )
        )

        total_row.add_widget(
            TableCellLabel(
                text="[b]Итого[/b]",
                markup=True,
                halign="right",
                size_hint_x=0.74
            )
        )

        total_row.add_widget(
            TableCellLabel(
                text=works_screen.total_hours_value.text,
                size_hint_x=0.18
            )
        )

        paper.add_widget(
            total_row
        )

        self.pages.add_widget(
            paper
        )

    # =====================================================
    # ОБОРОТНАЯ СТОРОНА
    # =====================================================

    def build_materials_page(
        self,
        materials_screen
    ):

        paper = PaperBox(
            orientation="vertical",
            size_hint_y=None,
            spacing=0,
            padding=[15, 15, 15, 18]
        )

        paper.bind(
            minimum_height=paper.setter(
                "height"
            )
        )

        paper.add_widget(
            Label(
                text="[b]ИСПОЛЬЗОВАННЫЕ МАТЕРИАЛЫ[/b]",
                markup=True,
                font_size=22,
                color=(0, 0, 0, 1),
                size_hint_y=None,
                height=55
            )
        )

        header_color = (
            0.90,
            0.90,
            0.90,
            1
        )

        header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=45,
            spacing=0
        )

        columns = [
            ("№", 0.08),
            ("Наименование материала", 0.48),
            ("Код", 0.18),
            ("На кого взят", 0.26)
        ]

        for text, width in columns:

            header.add_widget(
                TableCellLabel(
                    text=text,
                    size_hint_x=width,
                    bg_color=header_color
                )
            )

        paper.add_widget(
            header
        )

        # материалы

        if materials_screen.material_rows:

            for index, row_data in enumerate(
                materials_screen.material_rows,
                start=1
            ):

                row = BoxLayout(
                    orientation="horizontal",
                    size_hint_y=None,
                    height=46,
                    spacing=0
                )

                row.add_widget(
                    TableCellLabel(
                        text=str(index),
                        size_hint_x=0.08
                    )
                )

                row.add_widget(
                    TableCellLabel(
                        text=row_data[
                            "material"
                        ].text,
                        size_hint_x=0.48,
                        halign="left"
                    )
                )

                row.add_widget(
                    TableCellLabel(
                        text=row_data[
                            "code"
                        ].text,
                        size_hint_x=0.18
                    )
                )

                row.add_widget(
                    TableCellLabel(
                        text=row_data[
                            "employee"
                        ].text,
                        size_hint_x=0.26
                    )
                )

                paper.add_widget(
                    row
                )

        else:

            # Если материалов нет — оставляем одну пустую строку

            row = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=46,
                spacing=0
            )

            row.add_widget(
                TableCellLabel(
                    text="1",
                    size_hint_x=0.08
                )
            )

            row.add_widget(
                TableCellLabel(
                    text="",
                    size_hint_x=0.48
                )
            )

            row.add_widget(
                TableCellLabel(
                    text="",
                    size_hint_x=0.18
                )
            )

            row.add_widget(
                TableCellLabel(
                    text="",
                    size_hint_x=0.26
                )
            )

            paper.add_widget(
                row
            )

        self.pages.add_widget(
            paper
        )

    # =====================================================
    # НАВИГАЦИЯ
    # =====================================================

    def open_works(self, instance):
        self.manager.current = "works"

    def open_materials(self, instance):
        self.manager.current = "materials"


# =========================================================
# ПРИЛОЖЕНИЕ
# =========================================================

class MyApp(App):

    def build(self):

        manager = ScreenManager()

        manager.add_widget(
            WorkScreen(
                name="works"
            )
        )

        manager.add_widget(
            MaterialsScreen(
                name="materials"
            )
        )

        manager.add_widget(
            PreviewScreen(
                name="preview"
            )
        )

        return manager


MyApp().run()