import sys
from PyQt5.QtWidgets import QApplication
from admin_store import Admin_store

app = QApplication(sys.argv)
admin = Admin_store()
admin.show()
sys.exit(app.exec_())