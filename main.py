from PySide6 import QtWidgets, QtGui
import similarity


class Interface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_widget = QtWidgets.QWidget()

        self.before_btn = QtWidgets.QPushButton("Back")
        self.after_btn = QtWidgets.QPushButton("Next")

        self.menubar = self.menuBar()

        self._setup()
        self._event()
        self.after_btn.setEnabled(False)

    def _setup(self):
        self.setMinimumSize(500, 300)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(self.before_btn)
        buttons_layout.addWidget(self.after_btn)

        self.stack_layout = QtWidgets.QStackedLayout()

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(self.stack_layout)
        main_layout.addLayout(buttons_layout)

        self.main_widget.setLayout(main_layout)

        # page 1: input
        self.input_area1 = QtWidgets.QTextEdit()
        self.input_area2 = QtWidgets.QTextEdit()

        self.process_btn = QtWidgets.QPushButton("Process")

        page1_layout = QtWidgets.QVBoxLayout()

        page1_layout.addWidget(QtWidgets.QLabel("Sentence A"))
        page1_layout.addWidget(self.input_area1)

        page1_layout.addWidget(QtWidgets.QLabel("Sentence B"))
        page1_layout.addWidget(self.input_area2)

        page1_layout.addWidget(self.process_btn)

        first_page = QtWidgets.QWidget()
        first_page.setLayout(page1_layout)

        self.stack_layout.insertWidget(0, first_page)

        # page 2: tokenize & tagging
        self.listA = QtWidgets.QListWidget()
        self.listB = QtWidgets.QListWidget()

        page2_layout = QtWidgets.QHBoxLayout()
        page2_layout.addWidget(self.listA)
        page2_layout.addWidget(self.listB)

        wrapper2 = QtWidgets.QVBoxLayout()
        wrapper2.addWidget(QtWidgets.QLabel("Tokenize and Tagging"))
        wrapper2.addLayout(page2_layout)

        second_page = QtWidgets.QWidget()
        second_page.setLayout(wrapper2)

        self.stack_layout.insertWidget(1, second_page)

        # page 3: filter stopwords
        self.filteredA = QtWidgets.QListWidget()
        self.filteredB = QtWidgets.QListWidget()

        page3_layout = QtWidgets.QHBoxLayout()
        page3_layout.addWidget(self.filteredA)
        page3_layout.addWidget(self.filteredB)

        wrapper3 = QtWidgets.QVBoxLayout()
        wrapper3.addWidget(QtWidgets.QLabel("Filter Stopwords"))
        wrapper3.addLayout(page3_layout)

        third_page = QtWidgets.QWidget()
        third_page.setLayout(wrapper3)

        self.stack_layout.insertWidget(2, third_page)

        # page 4: stemming
        self.stemmedA = QtWidgets.QListWidget()
        self.stemmedB = QtWidgets.QListWidget()

        page4_layout = QtWidgets.QHBoxLayout()
        page4_layout.addWidget(self.stemmedA)
        page4_layout.addWidget(self.stemmedB)

        wrapper4 = QtWidgets.QVBoxLayout()
        wrapper4.addWidget(QtWidgets.QLabel("Stemming"))
        wrapper4.addLayout(page4_layout)

        fourth_page = QtWidgets.QWidget()
        fourth_page.setLayout(wrapper4)

        self.stack_layout.insertWidget(3, fourth_page)

        # page 5: wordnet weights
        self.weightsA = QtWidgets.QTableWidget()
        self.weightsB = QtWidgets.QTableWidget()

        page5_layout = QtWidgets.QVBoxLayout()
        page5_layout.addWidget(QtWidgets.QLabel("Weight A"))
        page5_layout.addWidget(self.weightsA)

        page5_layout.addWidget(QtWidgets.QLabel("Weight B"))
        page5_layout.addWidget(self.weightsB)

        wrapper5 = QtWidgets.QVBoxLayout()
        wrapper5.addWidget(QtWidgets.QLabel("WordNet Weightening"))
        wrapper5.addLayout(page5_layout)

        fifth_page = QtWidgets.QWidget()
        fifth_page.setLayout(wrapper5)

        self.stack_layout.insertWidget(4, fifth_page)

        # page 6: result
        self.result = QtWidgets.QLineEdit()
        page6_layout = QtWidgets.QHBoxLayout()
        page6_layout.addWidget(QtWidgets.QLabel("Similarity"))
        page6_layout.addWidget(self.result)

        sixth_page = QtWidgets.QWidget()
        sixth_page.setLayout(page6_layout)

        self.stack_layout.insertWidget(5, sixth_page)

        self.main_widget.setLayout(self.stack_layout)
        self.setCentralWidget(self.main_widget)

    def _toolbar_setup(self):
        stopword_button_action = QtGui.QAction()
        stopword_button_action.toggled.connect(lambda: print("click"))

        stopword_menu = self.menubar.addMenu("Stopword")
        stopword_menu.addAction(stopword_button_action)

    def _event(self):
        self._button_clicked()

        self.before_btn.clicked.connect(self._changeStackByClick)
        self.after_btn.clicked.connect(self._changeStackByClick)

        self.before_btn.clicked.connect(self._button_clicked)
        self.after_btn.clicked.connect(self._button_clicked)

        self.process_btn.clicked.connect(self._process)

    def _button_clicked(self):
        idx = self.stack_layout.currentIndex()

        self.before_btn.setEnabled(True)
        self.after_btn.setEnabled(True)

        if idx == 0:
            self.before_btn.setEnabled(False)

        elif idx == 5:
            self.after_btn.setEnabled(False)

    def _changeStackByClick(self):
        sender = self.sender()
        btn_text = sender.text()

        idx = self.stack_layout.currentIndex()
        if btn_text == "Back":
            self.stack_layout.setCurrentIndex(idx - 1)

        elif btn_text == "Next":
            self.stack_layout.setCurrentIndex(idx + 1)

    def _process(self):
        self.after_btn.setEnabled(True)
        s1 = self.input_area1.toPlainText()
        s2 = self.input_area2.toPlainText()
        result = similarity.calculate_verbose(s1, s2)
        self.update_result(result)
        self._update_tables(result)

    def _update_tables(self, values: dict):
        self.weightsA.clear()
        self.weightsB.clear()

        vector = values["vector"]

        stemmedA = values["stemmed"]["A"]
        stemmedB = values["stemmed"]["B"]

        vweightA = values["verbose_weight"]["A"]
        vweightB = values["verbose_weight"]["B"]

        vertical_labels = ["{}:{}".format(*label) for label in vector]

        self.weightsA.setRowCount(len(vweightA))
        self.weightsA.setColumnCount(len(vweightA[0]))
        for r, row in enumerate(vweightA):
            for c, col in enumerate(row):
                it = str(round(col, 2))
                item = QtWidgets.QTableWidgetItem(it)
                self.weightsA.setItem(r, c, item)

        self.weightsB.setRowCount(len(vweightB))
        self.weightsB.setColumnCount(len(vweightB[0]))
        for r, row in enumerate(vweightB):
            for c, col in enumerate(row):
                it = str(round(col, 2))
                item = QtWidgets.QTableWidgetItem(it)
                self.weightsB.setItem(r, c, item)

        # vertical labels
        self.weightsA.setVerticalHeaderLabels(vertical_labels)
        self.weightsB.setVerticalHeaderLabels(vertical_labels)

        # horizontal label
        self.weightsA.setHorizontalHeaderLabels(["{}:{}".format(*x) for x in stemmedA])
        self.weightsB.setHorizontalHeaderLabels(["{}:{}".format(*x) for x in stemmedB])

    def update_result(self, result: dict):
        self.listA.clear()
        self.listB.clear()

        self.filteredA.clear()
        self.filteredB.clear()

        self.stemmedA.clear()
        self.stemmedB.clear()

        # screw big O notation

        taggedA = result["tagged"]["A"]
        for lemma, tag in taggedA:
            self.listA.addItem(f"{lemma} : {tag}")

        taggedB = result["tagged"]["B"]
        for lemma, tag in taggedB:
            self.listB.addItem(f"{lemma} : {tag}")

        filteredA = result["filtered"]["A"]
        for lemma, tag in filteredA:
            self.filteredA.addItem(f"{lemma} : {tag}")

        filteredB = result["filtered"]["B"]
        for lemma, tag in filteredB:
            self.filteredB.addItem(f"{lemma} : {tag}")

        stemmedA = result["stemmed"]["A"]
        for lemma, tag in stemmedA:
            self.stemmedA.addItem(f"{lemma} : {tag}")

        stemmedB = result["stemmed"]["B"]
        for lemma, tag in stemmedB:
            self.stemmedB.addItem(f"{lemma} : {tag}")

        sim = round(result["sim"], 4)
        self.result.setText(str(sim))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ui = Interface()
    ui.show()
    app.exec()
