import sys
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QComboBox, QListWidget, QPushButton,
    QLabel, QMessageBox, QHBoxLayout, QApplication, QListWidgetItem
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import psycopg2
from database.config import db_config

class MaterialApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список материалов")
        self.setGeometry(100, 100, 800, 600)
        font = QFont("Verdana")
        self.setFont(font)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.material_list = QListWidget(self)
        self.material_list.setSpacing(10)
        self.layout.addWidget(self.material_list)
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Введите для поиска")
        self.search_input.textChanged.connect(self.on_search_changed)
        self.layout.addWidget(self.search_input)
        self.update_button = QPushButton("Обновить", self)
        self.update_button.clicked.connect(self.load_materials)
        self.layout.addWidget(self.update_button)
        self.load_materials()

    def load_material_types(self):
        try:
            conn = psycopg2.connect(
                dbname=db_config['dbname'],
                user=db_config['user'],
                password=db_config['password'],
                host=db_config['host'],
                port=db_config['port']
            )
            cursor = conn.cursor()
            cursor.execute("SELECT type_name FROM materials_types")
            types = cursor.fetchall()
            self.filter_combo.addItem("Все типы")
            for type_tuple in types:
                self.filter_combo.addItem(type_tuple[0])
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить типы материалов: {e}")

    def load_materials(self):
        if not hasattr(self, "material_list"):
            QMessageBox.critical(self, "Ошибка", "Список материалов не создан.")
            return

        try:
            conn = psycopg2.connect(
                dbname=db_config['dbname'],
                user=db_config['user'],
                password=db_config['password'],
                host=db_config['host'],
                port=db_config['port']
            )
            cursor = conn.cursor()
            materials = self.get_materials(cursor)
            self.material_list.clear()

            for material in materials:
                material_widget = QWidget()
                item_layout = QVBoxLayout(material_widget)
                item_layout.setContentsMargins(10, 10, 10, 10)
                title_label = QLabel(f"{material[5]} | {material[1]}", material_widget)
                title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
                item_layout.addWidget(title_label)

                quantity_label = QLabel(f"Минимальное количество: {material[2]} шт", material_widget)
                item_layout.addWidget(quantity_label)

                suppliers_label = QLabel(f"Поставщики: {material[3]}", material_widget)
                item_layout.addWidget(suppliers_label)

                material_widget.setStyleSheet("border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 5px 0;")

                list_item = QListWidgetItem()
                list_item.setSizeHint(material_widget.sizeHint())
                self.material_list.addItem(list_item)
                self.material_list.setItemWidget(list_item, material_widget)

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {e}")

    def get_materials(self, cursor):
        query = """
            SELECT 
                m.material_id, 
                mn.material_name, 
                m.min_quantity, 
                string_agg(sn.supplier_name, ', ') AS suppliers, 
                m.image, 
                mt.type_name
            FROM 
                materials m
            JOIN 
                materials_names mn ON m.material_id = mn.material_id
            JOIN 
                potential_suppliers ps ON m.material_id = ps.material_id
            JOIN 
                suppliers s ON ps.potential_supplier_id = s.supplier_id
            JOIN 
                suppliers_names sn ON s.supplier_id = sn.supplier_id  
            JOIN 
                materials_types mt ON m.type_id = mt.type_id
            GROUP BY 
                m.material_id, mn.material_name, m.min_quantity, m.image, mt.type_name
        """
        cursor.execute(query)
        return cursor.fetchall()

    def on_search_changed(self):
        self.load_materials()
