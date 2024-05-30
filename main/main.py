import sys
from PyQt5.QtWidgets import QApplication
from Starter import Starter

if __name__ == "__main__":
    app = QApplication(sys.argv)
    starter = Starter()
    starter.show()
    sys.exit(app.exec_())