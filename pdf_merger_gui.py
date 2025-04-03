import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QPushButton, QListWidget, QFileDialog, QMessageBox,
                            QLabel, QHBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from PyPDF2 import PdfMerger

class PDFListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event: QDropEvent):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        for file_path in files:
            if file_path.lower().endswith('.pdf'):
                self.addItem(file_path)
        event.accept()

class PDFMergerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF 합치기")
        self.setMinimumSize(600, 400)
        
        # 메인 위젯과 레이아웃 설정
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # 설명 레이블
        instruction_label = QLabel("PDF 파일을 드래그 앤 드롭하거나 '파일 추가' 버튼을 클릭하세요.")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instruction_label)
        
        # PDF 리스트 위젯
        self.pdf_list = PDFListWidget()
        layout.addWidget(self.pdf_list)
        
        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        
        # 파일 추가 버튼
        add_button = QPushButton("파일 추가")
        add_button.clicked.connect(self.add_files)
        button_layout.addWidget(add_button)
        
        # 선택 항목 제거 버튼
        remove_button = QPushButton("선택 항목 제거")
        remove_button.clicked.connect(self.remove_selected)
        button_layout.addWidget(remove_button)
        
        # 위로 이동 버튼
        move_up_button = QPushButton("↑")
        move_up_button.clicked.connect(self.move_up)
        button_layout.addWidget(move_up_button)
        
        # 아래로 이동 버튼
        move_down_button = QPushButton("↓")
        move_down_button.clicked.connect(self.move_down)
        button_layout.addWidget(move_down_button)
        
        # 합치기 버튼
        merge_button = QPushButton("PDF 합치기")
        merge_button.clicked.connect(self.merge_pdfs)
        button_layout.addWidget(merge_button)
        
        layout.addLayout(button_layout)
        
    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "PDF 파일 선택",
            "",
            "PDF Files (*.pdf)"
        )
        for file_path in files:
            self.pdf_list.addItem(file_path)
            
    def remove_selected(self):
        for item in self.pdf_list.selectedItems():
            self.pdf_list.takeItem(self.pdf_list.row(item))
            
    def move_up(self):
        current_row = self.pdf_list.currentRow()
        if current_row > 0:
            item = self.pdf_list.takeItem(current_row)
            self.pdf_list.insertItem(current_row - 1, item)
            self.pdf_list.setCurrentRow(current_row - 1)
            
    def move_down(self):
        current_row = self.pdf_list.currentRow()
        if current_row < self.pdf_list.count() - 1:
            item = self.pdf_list.takeItem(current_row)
            self.pdf_list.insertItem(current_row + 1, item)
            self.pdf_list.setCurrentRow(current_row + 1)
            
    def merge_pdfs(self):
        if self.pdf_list.count() == 0:
            QMessageBox.warning(self, "경고", "합칠 PDF 파일을 추가해주세요.")
            return
            
        # 저장할 파일 경로 선택
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "PDF 저장",
            "",
            "PDF Files (*.pdf)"
        )
        
        if not save_path:
            return
            
        try:
            merger = PdfMerger()
            
            # 리스트에 있는 모든 PDF 파일을 순서대로 합치기
            for i in range(self.pdf_list.count()):
                file_path = self.pdf_list.item(i).text()
                merger.append(file_path)
                
            # 결과 저장
            merger.write(save_path)
            merger.close()
            
            QMessageBox.information(self, "성공", "PDF 파일이 성공적으로 합쳐졌습니다!")
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"PDF 합치기 중 오류가 발생했습니다: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFMergerApp()
    window.show()
    sys.exit(app.exec()) 