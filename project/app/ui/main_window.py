"""Main application window for the ЖКХ monitoring application."""

from __future__ import annotations

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPaintEvent, QPen
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.repositories.meter_repository import (
    delete_meter,
    get_meters,
    get_readings,
)
from app.services.meter_service import create_meter, create_reading


class GosuslugiLogo(QWidget):
    """Display a small stylized Gosuslugi logo."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the logo."""
        super().__init__(parent)
        self.setFixedSize(24, 24)

    def paintEvent(self, event: QPaintEvent) -> None:
        """Draw the Gosuslugi logo."""
        del event

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(4, 4, 16, 16)

        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor("#2454D6"), 1.5))
        painter.drawArc(rect, 20 * 16, 150 * 16)

        painter.setPen(QPen(QColor("#E5395B"), 1.5))
        painter.drawArc(rect, 205 * 16, 125 * 16)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#2454D6"))
        painter.drawEllipse(QRectF(9, 9, 6, 6))

        painter.end()


class LoginDialog(QDialog):
    """Display the authorization window."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the authorization dialog."""
        super().__init__(parent)

        self.user_name = ""

        self.setWindowTitle("Мониторинг расходов ЖКХ")
        self.setFixedSize(360, 430)
        self.setModal(True)

        self.setStyleSheet(
            """
            QDialog {
                background-color: #F4F6F8;
            }

            QLabel {
                background: transparent;
                color: #172033;
            }

            QLabel#titleLabel {
                font-size: 15px;
                font-weight: 700;
            }

            QLabel#subtitleLabel {
                color: #8A94A6;
                font-size: 9px;
            }

            QLabel#fieldLabel {
                color: #303846;
                font-size: 9px;
            }

            QLabel#orLabel {
                color: #777F8C;
                font-size: 8px;
            }

            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #D4DAE3;
                border-radius: 4px;
                padding-left: 8px;
                padding-right: 8px;
                color: #172033;
                font-size: 9px;
            }

            QLineEdit:focus {
                border: 1px solid #243F91;
            }

            QPushButton {
                background-color: #243F91;
                color: #FFFFFF;
                border: none;
                border-radius: 4px;
                font-size: 8px;
            }

            QPushButton:hover {
                background-color: #304FA5;
            }

            QPushButton:pressed {
                background-color: #1C3276;
            }
            """
        )

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the authorization interface."""
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setObjectName("loginCard")
        card.setFixedSize(245, 320)

        card.setStyleSheet(
            """
            QFrame#loginCard {
                background-color: #FFFFFF;
                border: 1px solid #222222;
                border-radius: 11px;
            }
            """
        )

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(14)
        shadow.setOffset(2, 4)
        shadow.setColor(QColor(0, 0, 0, 120))
        card.setGraphicsEffect(shadow)

        outer_layout.addWidget(card)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 15, 25, 15)
        layout.setSpacing(0)

        title = QLabel("Мониторинг расходов ЖКХ")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFixedHeight(27)
        layout.addWidget(title)

        subtitle = QLabel("Вход в систему")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setFixedHeight(24)
        layout.addWidget(subtitle)

        layout.addSpacing(5)

        login_label = QLabel("Логин")
        login_label.setObjectName("fieldLabel")
        login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        login_label.setFixedHeight(17)
        layout.addWidget(login_label)

        self.login_edit = QLineEdit()
        self.login_edit.setFixedHeight(23)
        layout.addWidget(self.login_edit)

        layout.addSpacing(5)

        password_label = QLabel("Пароль")
        password_label.setObjectName("fieldLabel")
        password_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        password_label.setFixedHeight(17)
        layout.addWidget(password_label)

        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setFixedHeight(23)
        layout.addWidget(self.password_edit)

        layout.addSpacing(17)

        register_button = QPushButton("Регистрация")
        register_button.setFixedSize(90, 22)
        register_button.clicked.connect(self._register)

        layout.addWidget(
            register_button,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )

        layout.addSpacing(16)

        login_button = QPushButton("Войти в аккаунт")
        login_button.setFixedSize(90, 25)
        login_button.clicked.connect(self._login)

        layout.addWidget(
            login_button,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )

        or_label = QLabel("Или")
        or_label.setObjectName("orLabel")
        or_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        or_label.setFixedHeight(19)
        layout.addWidget(or_label)

        gosuslugi_row = QHBoxLayout()
        gosuslugi_row.setContentsMargins(0, 0, 0, 0)
        gosuslugi_row.setSpacing(7)

        gosuslugi_row.addStretch()

        gosuslugi_button = QPushButton(
            "Войти через\nгосуслуги"
        )
        gosuslugi_button.setFixedSize(90, 32)
        gosuslugi_button.clicked.connect(
            self._login_with_gosuslugi
        )

        gosuslugi_row.addWidget(gosuslugi_button)

        logo = GosuslugiLogo()

        gosuslugi_row.addWidget(
            logo,
            alignment=Qt.AlignmentFlag.AlignVCenter,
        )

        gosuslugi_row.addStretch()

        layout.addLayout(gosuslugi_row)

    def _login(self) -> None:
        """Validate credentials and open the application."""
        login = self.login_edit.text().strip()
        password = self.password_edit.text()

        if not login:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Введите логин.",
            )
            self.login_edit.setFocus()
            return

        if not password:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Введите пароль.",
            )
            self.password_edit.setFocus()
            return

        if login == "demo" and password == "demo":
            self.user_name = "Вячеслав Карасев"
            self.accept()
            return

        QMessageBox.warning(
            self,
            "Ошибка авторизации",
            "Неверный логин или пароль.\n\n"
            "Для демонстрации:\n"
            "Логин: demo\n"
            "Пароль: demo",
        )

    def _register(self) -> None:
        """Handle registration."""
        QMessageBox.information(
            self,
            "Регистрация",
            "Регистрация нового пользователя "
            "будет доступна в следующей версии.",
        )

    def _login_with_gosuslugi(self) -> None:
        """Handle Gosuslugi authorization."""
        self.user_name = "Пользователь Госуслуг"
        self.accept()


class DonutChart(QWidget):
    """Display a circular ЖКХ expense chart."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the chart."""
        super().__init__(parent)
        self.setMinimumSize(500, 260)

    def paintEvent(self, event: QPaintEvent) -> None:
        """Draw the circular expense chart."""
        del event

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        data = [
            ("Сектор газа", 20, "720 ₽", "#68778C"),
            ("Сектор воды", 25, "960 ₽", "#2454D6"),
            (
                "Сектор электроэнергии",
                55,
                "1 200 ₽",
                "#FFBE00",
            ),
        ]

        center_x = 130
        center_y = self.height() // 2

        outer_radius = 55
        inner_radius = 39

        outer_rect = QRectF(
            center_x - outer_radius,
            center_y - outer_radius,
            outer_radius * 2,
            outer_radius * 2,
        )

        start_angle = 90.0
        gap = 3.0

        for _, percent, _, color in data:
            span = percent / 100.0 * 360.0

            draw_start = start_angle + gap / 2
            draw_span = span - gap

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(color))

            painter.drawPie(
                outer_rect,
                int(draw_start * 16),
                int(-draw_span * 16),
            )

            start_angle -= span

        painter.setBrush(QColor("#FFFFFF"))
        painter.drawEllipse(
            QRectF(
                center_x - inner_radius,
                center_y - inner_radius,
                inner_radius * 2,
                inner_radius * 2,
            )
        )

        legend_x = 205
        legend_y = center_y - 45

        painter.setFont(QFont("Arial", 9))

        for index, (
            name,
            percent,
            amount,
            color,
        ) in enumerate(data):
            y = legend_y + index * 40

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(color))

            painter.drawRect(
                QRectF(
                    legend_x,
                    y - 9,
                    18,
                    18,
                )
            )

            painter.setPen(QColor("#111111"))

            painter.drawText(
                legend_x + 25,
                y + 5,
                f"{name} — {percent}% ({amount})",
            )

        painter.end()


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(
        self,
        user_name: str = "Вячеслав Карасев",
    ) -> None:
        """Initialize the main window."""
        super().__init__()

        self.user_name = user_name

        self.setWindowTitle("Мониторинг расходов ЖКХ")
        self.resize(1180, 720)
        self.setMinimumSize(1000, 620)

        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #F5F6F8;
            }

            QWidget {
                font-family: Arial;
            }

            QLabel {
                color: #172033;
            }

            QPushButton {
                border: none;
                border-radius: 5px;
                padding: 7px 12px;
                background-color: #24479B;
                color: white;
            }

            QPushButton:hover {
                background-color: #3159B5;
            }

            QLineEdit,
            QComboBox {
                background-color: white;
                border: 1px solid #D7DCE5;
                border-radius: 5px;
                padding: 7px;
            }

            QTableWidget {
                background-color: white;
                border: 1px solid #E0E4EA;
                gridline-color: #E8EBF0;
            }

            QHeaderView::section {
                background-color: #F0F2F5;
                border: none;
                padding: 8px;
                font-weight: bold;
            }
            """
        )

        self._build_ui()
        self._show_dashboard()

    def _build_ui(self) -> None:
        """Build the main application interface."""
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        sidebar = QFrame()
        sidebar.setFixedWidth(220)

        sidebar.setStyleSheet(
            """
            QFrame {
                background-color: #FFE5E5;
                border-radius: 4px;
            }

            QPushButton {
                text-align: left;
                padding-left: 18px;
                background-color: transparent;
                color: #172033;
                border-radius: 0;
                font-size: 11px;
            }

            QPushButton:hover {
                background-color: #F8D8D8;
            }

            QPushButton:checked {
                background-color: #DCE5FA;
                color: #24479B;
                font-weight: bold;
            }
            """
        )

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 15, 0, 15)
        sidebar_layout.setSpacing(3)

        user_label = QLabel(self.user_name)
        user_label.setStyleSheet(
            """
            font-size: 11px;
            font-weight: bold;
            padding-left: 18px;
            """
        )

        sidebar_layout.addWidget(user_label)

        role_label = QLabel("Роль: Владелец")
        role_label.setStyleSheet(
            """
            color: #268A62;
            font-size: 9px;
            padding-left: 18px;
            """
        )

        sidebar_layout.addWidget(role_label)
        sidebar_layout.addSpacing(15)

        self.menu_buttons: list[QPushButton] = []

        menu_items = [
            ("Главное меню", 0),
            ("Приборы учета", 1),
            ("Аналитика и прогнозы", 2),
            ("Отчеты и экспорт", 3),
            ("Настройки", 4),
        ]

        for text, index in menu_items:
            button = QPushButton(text)
            button.setCheckable(True)
            button.setFixedHeight(36)

            button.clicked.connect(
                lambda checked=False, page=index: (
                    self._change_page(page)
                )
            )

            self.menu_buttons.append(button)
            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()

        logout_button = QPushButton("Выйти")
        logout_button.setStyleSheet(
            """
            QPushButton {
                color: #B3261E;
                background-color: transparent;
                text-align: left;
                padding-left: 18px;
            }

            QPushButton:hover {
                background-color: #F8D8D8;
            }
            """
        )

        logout_button.clicked.connect(self._logout)
        sidebar_layout.addWidget(logout_button)

        main_layout.addWidget(sidebar)

        self.pages = QStackedWidget()

        self.pages.addWidget(self._dashboard_page())
        self.pages.addWidget(self._meters_page())
        self.pages.addWidget(self._analytics_page())
        self.pages.addWidget(self._reports_page())
        self.pages.addWidget(self._settings_page())

        main_layout.addWidget(self.pages, 1)

    def _change_page(self, index: int) -> None:
        """Switch the active page."""
        self.pages.setCurrentIndex(index)

        for number, button in enumerate(self.menu_buttons):
            button.setChecked(number == index)

    def _show_dashboard(self) -> None:
        """Show the dashboard."""
        self._change_page(0)

    def _dashboard_page(self) -> QWidget:
        """Create the dashboard page."""
        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Главное меню")
        title.setStyleSheet(
            """
            font-size: 22px;
            font-weight: bold;
            """
        )

        layout.addWidget(title)

        address = QLabel(
            "Квартира № 45 · ул. Центральная, дом 10"
        )
        address.setStyleSheet(
            "color: #697386; font-size: 11px;"
        )

        layout.addWidget(address)

        cards_layout = QHBoxLayout()

        cards = [
            ("К оплате", "3 420 ₽"),
            ("Бюджет ЖКХ", "8 500 ₽"),
            ("Приборы учета", "3"),
        ]

        for title_text, value in cards:
            cards_layout.addWidget(
                self._create_info_card(
                    title_text,
                    value,
                )
            )

        layout.addLayout(cards_layout)

        section_title = QLabel(
            "Динамика расходов ресурсов"
        )
        section_title.setStyleSheet(
            """
            font-size: 15px;
            font-weight: bold;
            """
        )

        layout.addWidget(section_title)

        table = QTableWidget(4, 3)

        table.setHorizontalHeaderLabels(
            [
                "Ресурс",
                "Текущее потребление",
                "Расход",
            ]
        )

        rows = [
            (
                "Электроэнергия",
                "120 кВт·ч",
                "1 200 ₽",
            ),
            (
                "Холодная вода",
                "7,4 м³",
                "960 ₽",
            ),
            (
                "Газ",
                "20 м³",
                "720 ₽",
            ),
            (
                "Горячая вода",
                "6,2 м³",
                "540 ₽",
            ),
        ]

        for row, values in enumerate(rows):
            for column, value in enumerate(values):
                table.setItem(
                    row,
                    column,
                    QTableWidgetItem(value),
                )

        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(
            True
        )

        table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        layout.addWidget(table)

        return page

    def _create_info_card(
        self,
        title: str,
        value: str,
    ) -> QFrame:
        """Create a dashboard information card."""
        card = QFrame()

        card.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #E1E5EB;
                border-radius: 8px;
            }
            """
        )

        layout = QVBoxLayout(card)

        title_label = QLabel(title)
        title_label.setStyleSheet(
            "color: #737D8F; font-size: 10px;"
        )

        value_label = QLabel(value)
        value_label.setStyleSheet(
            """
            font-size: 22px;
            font-weight: bold;
            """
        )

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        return card

    def _meters_page(self) -> QWidget:
        """Create the meters page."""
        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)

        title_row = QHBoxLayout()

        title = QLabel("Приборы учета")
        title.setStyleSheet(
            """
            font-size: 22px;
            font-weight: bold;
            """
        )

        title_row.addWidget(title)
        title_row.addStretch()

        add_button = QPushButton(
            "+ Добавить прибор"
        )
        add_button.clicked.connect(self._add_meter)

        title_row.addWidget(add_button)
        layout.addLayout(title_row)

        self.meters_table = QTableWidget()

        self.meters_table.setColumnCount(6)
        self.meters_table.setHorizontalHeaderLabels(
            [
                "ID",
                "Ресурс",
                "Серийный номер",
                "Установка",
                "Поверка",
                "Активен",
            ]
        )

        self.meters_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        layout.addWidget(self.meters_table)

        buttons = QHBoxLayout()

        refresh_button = QPushButton("Обновить")
        refresh_button.clicked.connect(
            self._refresh_meters
        )

        reading_button = QPushButton(
            "Внести показание"
        )
        reading_button.clicked.connect(
            self._add_reading
        )

        delete_button = QPushButton(
            "Удалить выбранный"
        )
        delete_button.clicked.connect(
            self._delete_selected_meter
        )

        buttons.addWidget(refresh_button)
        buttons.addWidget(reading_button)
        buttons.addWidget(delete_button)
        buttons.addStretch()

        layout.addLayout(buttons)

        self._refresh_meters()

        return page

    def _refresh_meters(self) -> None:
        """Refresh the meters table."""
        meters = get_meters()

        self.meters_table.setRowCount(len(meters))

        for row, meter in enumerate(meters):
            values = [
                meter.get("id", ""),
                meter.get("meter_type", ""),
                meter.get("serial_number", ""),
                meter.get("installation_date", ""),
                meter.get("verification_date", ""),
                (
                    "Да"
                    if meter.get("is_active")
                    else "Нет"
                ),
            ]

            for column, value in enumerate(values):
                self.meters_table.setItem(
                    row,
                    column,
                    QTableWidgetItem(str(value)),
                )

        self.meters_table.resizeColumnsToContents()

    def _add_meter(self) -> None:
        """Open the add meter dialog."""
        dialog = MeterDialog(self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        try:
            create_meter(
                dialog.resource_type.currentText(),
                dialog.serial_number.text(),
                dialog.verification_date.text(),
            )
        except ValueError as error:
            QMessageBox.warning(
                self,
                "Ошибка",
                str(error),
            )
            return
        except RuntimeError as error:
            QMessageBox.critical(
                self,
                "Ошибка базы данных",
                str(error),
            )
            return

        self._refresh_meters()

    def _add_reading(self) -> None:
        """Open the add reading dialog."""
        meters = get_meters()

        if not meters:
            QMessageBox.information(
                self,
                "Показания",
                "Сначала добавьте прибор учета.",
            )
            return

        dialog = ReadingDialog(meters, self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        try:
            consumption = create_reading(
                dialog.get_meter_id(),
                dialog.value_edit.text(),
            )
        except ValueError as error:
            QMessageBox.warning(
                self,
                "Ошибка",
                str(error),
            )
            return

        QMessageBox.information(
            self,
            "Показание сохранено",
            f"Потребление: {consumption:.2f}",
        )

    def _delete_selected_meter(self) -> None:
        """Delete the selected meter."""
        row = self.meters_table.currentRow()

        if row < 0:
            QMessageBox.information(
                self,
                "Удаление",
                "Выберите прибор учета.",
            )
            return

        item = self.meters_table.item(row, 0)

        if item is None:
            return

        meter_id = int(item.text())

        answer = QMessageBox.question(
            self,
            "Удаление",
            "Удалить выбранный прибор учета?",
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        delete_meter(meter_id)
        self._refresh_meters()

    def _analytics_page(self) -> QWidget:
        """Create the analytics page."""
        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Аналитика и прогнозы")
        title.setStyleSheet(
            """
            font-size: 22px;
            font-weight: bold;
            """
        )

        layout.addWidget(title)

        subtitle = QLabel(
            "Распределение затрат за текущий месяц"
        )
        subtitle.setStyleSheet(
            "color: #697386; font-size: 11px;"
        )

        layout.addWidget(subtitle)

        chart_frame = QFrame()

        chart_frame.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #E2E5EA;
                border-radius: 8px;
            }
            """
        )

        chart_layout = QVBoxLayout(chart_frame)

        chart_layout.addWidget(DonutChart())

        layout.addWidget(chart_frame)

        anomaly = QFrame()

        anomaly.setStyleSheet(
            """
            QFrame {
                background-color: #FFF0F0;
                border: 1px solid #F6CCCC;
                border-radius: 6px;
            }
            """
        )

        anomaly_layout = QVBoxLayout(anomaly)

        anomaly_title = QLabel(
            "⚠ Обнаружена аномалия в потреблении!"
        )
        anomaly_title.setStyleSheet(
            """
            color: #D93025;
            font-weight: bold;
            """
        )

        anomaly_text = QLabel(
            "Расход по прибору ХВС превышает "
            "среднее нормы на 28%. Рекомендуем "
            "проверить прибор на наличие скрытых утечек."
        )

        anomaly_text.setWordWrap(True)

        anomaly_layout.addWidget(anomaly_title)
        anomaly_layout.addWidget(anomaly_text)

        layout.addWidget(anomaly)

        return page

    def _reports_page(self) -> QWidget:
        """Create the reports page."""
        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Отчеты и экспорт")
        title.setStyleSheet(
            """
            font-size: 22px;
            font-weight: bold;
            """
        )

        layout.addWidget(title)

        description = QLabel(
            "Формирование отчетов по расходам "
            "и показаниям приборов учета."
        )

        description.setStyleSheet(
            "color: #697386;"
        )

        layout.addWidget(description)
        layout.addSpacing(15)

        pdf_button = QPushButton(
            "Сформировать PDF-отчет"
        )
        pdf_button.setFixedWidth(220)
        pdf_button.clicked.connect(
            self._export_pdf
        )

        excel_button = QPushButton(
            "Экспортировать в Excel"
        )
        excel_button.setFixedWidth(220)
        excel_button.clicked.connect(
            self._export_excel
        )

        layout.addWidget(pdf_button)
        layout.addSpacing(10)
        layout.addWidget(excel_button)
        layout.addSpacing(25)

        history_title = QLabel(
            "История показаний"
        )
        history_title.setStyleSheet(
            """
            font-size: 15px;
            font-weight: bold;
            """
        )

        layout.addWidget(history_title)

        readings = get_readings()

        table = QTableWidget(
            len(readings),
            7,
        )

        table.setHorizontalHeaderLabels(
            [
                "Ресурс",
                "Серийный номер",
                "Показание",
                "Предыдущее",
                "Расход",
                "Дата",
                "Статус",
            ]
        )

        for row, reading in enumerate(readings):
            values = [
                reading.get("meter_type", ""),
                reading.get("serial_number", ""),
                reading.get("reading_value", ""),
                reading.get("previous_value", ""),
                reading.get("consumption", ""),
                reading.get("reading_date", ""),
                reading.get("status", ""),
            ]

            for column, value in enumerate(values):
                table.setItem(
                    row,
                    column,
                    QTableWidgetItem(str(value)),
                )

        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(
            True
        )

        layout.addWidget(table)

        return page

    def _export_pdf(self) -> None:
        """Show PDF export information."""
        QMessageBox.information(
            self,
            "PDF",
            "Модуль формирования PDF-отчета "
            "подготовлен для подключения.",
        )

    def _export_excel(self) -> None:
        """Show Excel export information."""
        QMessageBox.information(
            self,
            "Excel",
            "Модуль экспорта Excel "
            "подготовлен для подключения.",
        )

    # ========================================================
    # НАСТРОЙКИ — ВОЗВРАЩЕНЫ ПО МАКЕТУ
    # ========================================================

    def _settings_page(self) -> QWidget:
        """Create the settings page matching the Figma layout."""
        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(0)

        # ----------------------------------------------------
        # Профиль и аккаунт
        # ----------------------------------------------------

        profile_row = QHBoxLayout()
        profile_row.setContentsMargins(0, 0, 0, 14)
        profile_row.setSpacing(12)

        profile_icon = QLabel("👤")
        profile_icon.setFixedSize(28, 28)
        profile_icon.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        profile_icon.setStyleSheet(
            """
            font-size: 20px;
            """
        )

        profile_button = QPushButton(
            "Профиль и аккаунт"
        )
        profile_button.setFixedHeight(30)
        profile_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: #172033;
                text-align: left;
                font-size: 10px;
                font-weight: bold;
                padding: 0;
            }

            QPushButton:hover {
                color: #24479B;
            }
            """
        )

        profile_button.clicked.connect(
            self._open_profile_dialog
        )

        profile_row.addWidget(profile_icon)
        profile_row.addWidget(profile_button)
        profile_row.addStretch()

        layout.addLayout(profile_row)

        # ----------------------------------------------------
        # Безопасность
        # ----------------------------------------------------

        security_row = QHBoxLayout()
        security_row.setContentsMargins(0, 0, 0, 14)
        security_row.setSpacing(12)

        security_icon = QLabel("🛡️")
        security_icon.setFixedSize(28, 28)
        security_icon.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        security_icon.setStyleSheet(
            """
            font-size: 20px;
            """
        )

        security_button = QPushButton(
            "Безопасность"
        )
        security_button.setFixedHeight(30)
        security_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: #172033;
                text-align: left;
                font-size: 10px;
                font-weight: bold;
                padding: 0;
            }

            QPushButton:hover {
                color: #24479B;
            }
            """
        )

        security_button.clicked.connect(
            self._open_security_dialog
        )

        security_row.addWidget(security_icon)
        security_row.addWidget(security_button)
        security_row.addStretch()

        layout.addLayout(security_row)

        # ----------------------------------------------------
        # Выбор жилья
        # ----------------------------------------------------

        property_row = QHBoxLayout()
        property_row.setContentsMargins(0, 0, 0, 14)
        property_row.setSpacing(12)

        property_icon = QLabel("🏠")
        property_icon.setFixedSize(28, 28)
        property_icon.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        property_icon.setStyleSheet(
            """
            font-size: 20px;
            """
        )

        property_button = QPushButton(
            "Выбор жилья"
        )
        property_button.setFixedHeight(30)
        property_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: #172033;
                text-align: left;
                font-size: 10px;
                font-weight: bold;
                padding: 0;
            }

            QPushButton:hover {
                color: #24479B;
            }
            """
        )

        property_button.clicked.connect(
            self._open_property_dialog
        )

        property_row.addWidget(property_icon)
        property_row.addWidget(property_button)
        property_row.addStretch()

        layout.addLayout(property_row)

        # ----------------------------------------------------
        # Настройка уведомлений
        # ----------------------------------------------------

        notification_row = QHBoxLayout()
        notification_row.setContentsMargins(
            0,
            0,
            0,
            14,
        )
        notification_row.setSpacing(12)

        notification_icon = QLabel("🔔")
        notification_icon.setFixedSize(28, 28)
        notification_icon.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        notification_icon.setStyleSheet(
            """
            font-size: 20px;
            """
        )

        notification_button = QPushButton(
            "Настройка уведомлений"
        )
        notification_button.setFixedHeight(30)
        notification_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: #24479B;
                text-align: left;
                font-size: 10px;
                font-weight: bold;
                padding: 0;
            }

            QPushButton:hover {
                color: #3159B5;
            }
            """
        )

        notification_button.clicked.connect(
            self._open_notification_dialog
        )

        notification_row.addWidget(
            notification_icon
        )
        notification_row.addWidget(
            notification_button
        )
        notification_row.addStretch()

        layout.addLayout(notification_row)

        # ----------------------------------------------------
        # Банковские карты
        # ----------------------------------------------------

        cards_row = QHBoxLayout()
        cards_row.setContentsMargins(0, 0, 0, 5)
        cards_row.setSpacing(12)

        cards_icon = QLabel("💳")
        cards_icon.setFixedSize(28, 28)
        cards_icon.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        cards_icon.setStyleSheet(
            """
            font-size: 20px;
            """
        )

        cards_title = QLabel(
            "Банковские карты"
        )
        cards_title.setStyleSheet(
            """
            color: #172033;
            font-size: 10px;
            font-weight: bold;
            """
        )

        cards_row.addWidget(cards_icon)
        cards_row.addWidget(cards_title)
        cards_row.addStretch()

        layout.addLayout(cards_row)

        # ----------------------------------------------------
        # Мои банковские карты
        # ----------------------------------------------------

        my_cards_button = QPushButton(
            "Мои банковские карты"
        )
        my_cards_button.setFixedSize(125, 27)
        my_cards_button.setStyleSheet(
            """
            QPushButton {
                background-color: #E7ECF8;
                color: #172033;
                border-radius: 4px;
                text-align: left;
                padding-left: 8px;
                font-size: 8px;
            }

            QPushButton:hover {
                background-color: #DCE5FA;
            }
            """
        )

        my_cards_button.clicked.connect(
            self._open_bank_cards_dialog
        )

        layout.addWidget(
            my_cards_button,
            alignment=Qt.AlignmentFlag.AlignLeft,
        )

        # ----------------------------------------------------
        # Добавить банковскую карту
        # ----------------------------------------------------

        add_card_button = QPushButton(
            "Добавить банковскую карту"
        )
        add_card_button.setFixedSize(125, 27)
        add_card_button.setStyleSheet(
            """
            QPushButton {
                background-color: #E7ECF8;
                color: #172033;
                border-radius: 4px;
                text-align: left;
                padding-left: 8px;
                font-size: 8px;
            }

            QPushButton:hover {
                background-color: #DCE5FA;
            }
            """
        )

        add_card_button.clicked.connect(
            self._add_bank_card
        )

        layout.addWidget(
            add_card_button,
            alignment=Qt.AlignmentFlag.AlignLeft,
        )

        layout.addStretch()

        return page

    # ========================================================
    # ОБРАБОТЧИКИ НАСТРОЕК
    # ========================================================

    def _open_profile_dialog(self) -> None:
        """Open the profile and account dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Профиль и аккаунт")
        dialog.setFixedWidth(380)

        layout = QFormLayout(dialog)

        name_edit = QLineEdit(self.user_name)
        phone_edit = QLineEdit("+7 (900) 000-00-00")
        email_edit = QLineEdit("demo@example.com")

        layout.addRow(
            "Имя:",
            name_edit,
        )
        layout.addRow(
            "Телефон:",
            phone_edit,
        )
        layout.addRow(
            "Email:",
            email_edit,
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        layout.addRow(buttons)

        dialog.exec()

    def _open_security_dialog(self) -> None:
        """Open the security settings dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Безопасность")
        dialog.setFixedWidth(380)

        layout = QVBoxLayout(dialog)

        title = QLabel(
            "Настройки безопасности аккаунта"
        )
        title.setStyleSheet(
            "font-weight: bold; font-size: 13px;"
        )

        layout.addWidget(title)

        password_button = QPushButton(
            "Изменить пароль"
        )

        password_button.clicked.connect(
            lambda: QMessageBox.information(
                dialog,
                "Безопасность",
                "Функция изменения пароля "
                "будет доступна в следующей версии.",
            )
        )

        layout.addWidget(password_button)

        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(dialog.accept)

        layout.addWidget(close_button)

        dialog.exec()

    def _open_property_dialog(self) -> None:
        """Open the property selection dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Выбор жилья")
        dialog.setFixedWidth(420)

        layout = QFormLayout(dialog)

        address = QLineEdit(
            "ул. Центральная, дом 10"
        )
        apartment = QLineEdit("45")

        layout.addRow(
            "Адрес:",
            address,
        )
        layout.addRow(
            "Квартира:",
            apartment,
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        layout.addRow(buttons)

        dialog.exec()

    def _open_notification_dialog(self) -> None:
        """Open the notification settings dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle(
            "Настройка уведомлений"
        )
        dialog.setFixedWidth(380)

        layout = QVBoxLayout(dialog)

        notifications = [
            "Уведомления о задолженности",
            "Напоминания о показаниях",
            "Предупреждения об аномалиях",
        ]

        for text in notifications:
            checkbox = QPushButton(
                f"✓  {text}"
            )
            checkbox.setCheckable(True)
            checkbox.setChecked(True)
            checkbox.setStyleSheet(
                """
                QPushButton {
                    background-color: #E7ECF8;
                    color: #172033;
                    text-align: left;
                }

                QPushButton:checked {
                    background-color: #DCE5FA;
                    color: #24479B;
                }
                """
            )

            layout.addWidget(checkbox)

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(dialog.accept)

        layout.addWidget(save_button)

        dialog.exec()

    def _open_bank_cards_dialog(self) -> None:
        """Open the bank cards dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle(
            "Мои банковские карты"
        )
        dialog.setFixedWidth(420)

        layout = QVBoxLayout(dialog)

        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background-color: #F0F3F8;
                border: 1px solid #D8DEE8;
                border-radius: 6px;
            }
            """
        )

        card_layout = QVBoxLayout(card)

        number = QLabel(
            "**** **** **** 1234"
        )
        number.setStyleSheet(
            """
            font-size: 14px;
            font-weight: bold;
            """
        )

        card_layout.addWidget(number)

        card_layout.addWidget(
            QLabel("Основная банковская карта")
        )

        layout.addWidget(card)

        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(dialog.accept)

        layout.addWidget(close_button)

        dialog.exec()

    def _add_bank_card(self) -> None:
        """Open the add bank card dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle(
            "Добавить банковскую карту"
        )
        dialog.setFixedWidth(420)

        layout = QFormLayout(dialog)

        number_edit = QLineEdit()
        number_edit.setPlaceholderText(
            "Номер банковской карты"
        )

        expiry_edit = QLineEdit()
        expiry_edit.setPlaceholderText(
            "MM/YY"
        )

        layout.addRow(
            "Номер карты:",
            number_edit,
        )
        layout.addRow(
            "Срок действия:",
            expiry_edit,
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        layout.addRow(buttons)

        dialog.exec()

    def _logout(self) -> None:
        """Close the current application session."""
        answer = QMessageBox.question(
            self,
            "Выход",
            "Вы действительно хотите выйти?",
        )

        if answer == QMessageBox.StandardButton.Yes:
            self.close()


class MeterDialog(QDialog):
    """Dialog for creating a meter."""

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        """Initialize the meter dialog."""
        super().__init__(parent)

        self.setWindowTitle(
            "Добавить прибор учета"
        )
        self.setFixedWidth(360)

        layout = QFormLayout(self)

        self.resource_type = QComboBox()

        self.resource_type.addItems(
            [
                "Холодная вода",
                "Горячая вода",
                "Электроэнергия",
                "Газ",
            ]
        )

        self.serial_number = QLineEdit()

        self.verification_date = QLineEdit()
        self.verification_date.setPlaceholderText(
            "YYYY-MM-DD"
        )

        layout.addRow(
            "Ресурс:",
            self.resource_type,
        )
        layout.addRow(
            "Серийный номер:",
            self.serial_number,
        )
        layout.addRow(
            "Дата поверки:",
            self.verification_date,
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addRow(buttons)


class ReadingDialog(QDialog):
    """Dialog for adding a meter reading."""

    def __init__(
        self,
        meters: list[dict],
        parent: QWidget | None = None,
    ) -> None:
        """Initialize the reading dialog."""
        super().__init__(parent)

        self.setWindowTitle("Внести показание")
        self.setFixedWidth(360)

        layout = QFormLayout(self)

        self.meter_combo = QComboBox()

        for meter in meters:
            meter_id = meter.get("id")
            meter_type = meter.get(
                "meter_type",
                "",
            )
            serial = meter.get(
                "serial_number",
                "",
            )

            self.meter_combo.addItem(
                f"{meter_type} — {serial}",
                meter_id,
            )

        self.value_edit = QLineEdit()
        self.value_edit.setPlaceholderText(
            "Например: 4521.0"
        )

        layout.addRow(
            "Прибор:",
            self.meter_combo,
        )
        layout.addRow(
            "Показание:",
            self.value_edit,
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addRow(buttons)

    def get_meter_id(self) -> int:
        """Return the selected meter ID."""
        value = self.meter_combo.currentData()

        if value is None:
            raise ValueError(
                "Не выбран прибор учета."
            )

        return int(value)