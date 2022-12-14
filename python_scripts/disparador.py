import sys
from PyQt5.QtWidgets import QApplication
from admin_store import Main

app = QApplication(sys.argv)
admin = Main()
admin.show()
sys.exit(app.exec_())