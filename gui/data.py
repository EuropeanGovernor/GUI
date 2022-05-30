# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import Qt
# from PyQt5.QtSql import *
#
# class Child(QTabWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("记录")
#         self.resize(1000,618)
#         self.tab2 = QWidget()
#         self.addTab(self.tab2, 'Tab2')
#         self.tab2UI()
#         self.setWindowTitle("记录")
#     def tab2UI(self):
#         e=DataGrid()
#         hbox=QHBoxLayout()
#         hbox.addWidget(e)
#         self.tab2.setLayout(hbox)
#         self.setTabText(0, "早餐")
# class DataGrid(QWidget):
#     def createTableAndInit(self):
#         # 添加数据库
#         self.db = QSqlDatabase.addDatabase('QSQLITE')
#         # 设置数据库名称
#         self.db.setDatabaseName('./1.db')
#         self.db.open()
#
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("分页查询例子")
#         self.resize(1000, 618)
#         self.createTableAndInit()
#
#         # 当前页
#         self.currentPage = 0
#         # 总页数
#         self.totalPage = 0
#         # 总记录数
#         self.totalRecrodCount = 0
#         # 每页显示记录数
#         self.PageRecordCount = 10
#
#         self.initUI()
#
#     def initUI(self):
#         # 创建窗口
#         self.createWindow()
#         # 设置表格
#         self.setTableView()
#
#         # 信号槽连接
#         self.prevButton.clicked.connect(self.onPrevButtonClick)
#         self.nextButton.clicked.connect(self.onNextButtonClick)
#
#
#     def closeEvent(self, event):
#         # 关闭数据库
#         self.db.close()
#
#     # 创建窗口
#     def createWindow(self):
#         # 操作布局
#         operatorLayout = QHBoxLayout()
#         self.prevButton = QPushButton("前一页")
#         self.nextButton = QPushButton("后一页")
#
#
#         operatorLayout.addWidget(self.prevButton)
#         operatorLayout.addWidget(self.nextButton)
#
#
#
#         # 状态布局
#         statusLayout = QHBoxLayout()
#         self.totalPageLabel = QLabel()
#         self.totalPageLabel.setFixedWidth(100)
#         self.currentPageLabel = QLabel()
#         self.currentPageLabel.setFixedWidth(100)
#
#         self.totalRecordLabel = QLabel()
#         self.totalRecordLabel.setFixedWidth(100)
#
#         statusLayout.addWidget(self.totalPageLabel)
#         statusLayout.addWidget(self.currentPageLabel)
#         statusLayout.addWidget(QSplitter())
#         statusLayout.addWidget(self.totalRecordLabel)
#
#         # 设置表格属性
#         self.tableView = QTableView()
#         # 表格宽度的自适应调整
#         self.tableView.horizontalHeader().setStretchLastSection(True)
#         self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
#
#         # 创建界面
#         mainLayout = QVBoxLayout(self);
#         mainLayout.addLayout(operatorLayout);
#         mainLayout.addWidget(self.tableView);
#         mainLayout.addLayout(statusLayout);
#         self.setLayout(mainLayout)
#
#     # 设置表格
#     def setTableView(self):
#         # 声明查询模型
#         self.queryModel = QSqlQueryModel(self)
#
#         # 设置当前页
#         self.currentPage = 1;
#         # 得到总记录数
#         self.totalRecrodCount = self.getTotalRecordCount()
#         # 得到总页数
#         self.totalPage = self.getPageCount()
#         # 刷新状态
#         self.updateStatus()
#         # 设置总页数文本
#         self.setTotalPageLabel()
#         # 设置总记录数
#         self.setTotalRecordLabel()
#         # 记录查询
#         self.recordQuery(0)
#         # 设置模型
#         self.tableView.setModel(self.queryModel)
#         self.tableView.doubleClicked.connect(self.doubleClickedHandle)
#         self.tableView.setAlternatingRowColors(True)
#         self.tableView.setStyleSheet("alternate-background-color: rgb(209, 209, 209)"
#                                      "; background-color: rgb(244, 244, 244);")
#         self.tableView.setSortingEnabled(True)
#         self.tableView.horizontalHeader().setStyleSheet(
#             "::section{background-color: pink; color: blue; font-weight: bold}")
#         self.tableView.verticalHeader().hide()
#         # 设置表格表头
#         self.queryModel.setHeaderData(0, Qt.Horizontal, "菜名")
#
#
#     def doubleClickedHandle(self, index):
#         num,ok= QInputDialog.getDouble(self, '记录', '请输入份数：', min=0)
#         print(num)
#         print(index.row())
#
#
#     # 得到记录数
#     def getTotalRecordCount(self):
#         self.queryModel.setQuery("select * from recipe")
#         rowCount = self.queryModel.rowCount()
#         return rowCount
#
#     # 得到页数
#     def getPageCount(self):
#         if self.totalRecrodCount % self.PageRecordCount == 0:
#             return (self.totalRecrodCount / self.PageRecordCount)
#         else:
#             return (self.totalRecrodCount //self.PageRecordCount + 1)
#
#     # 记录查询
#     def recordQuery(self, limitIndex):
#         szQuery = ("select * from recipe limit %d,%d" % (limitIndex, self.PageRecordCount))
#         self.queryModel.setQuery(szQuery)
#
#     # 刷新状态
#     def updateStatus(self):
#         szCurrentText = ("当前第%d页" % self.currentPage)
#         self.currentPageLabel.setText(szCurrentText)
#         # 设置按钮是否可用
#         if self.currentPage == 1:
#             self.prevButton.setEnabled(False)
#             self.nextButton.setEnabled(True)
#         elif self.currentPage == self.totalPage:
#             self.prevButton.setEnabled(True)
#             self.nextButton.setEnabled(False)
#         else:
#             self.prevButton.setEnabled(True)
#             self.nextButton.setEnabled(True)
#
#     # 设置总数页文本
#     def setTotalPageLabel(self):
#         szPageCountText = ("总共%d页" % self.totalPage)
#         self.totalPageLabel.setText(szPageCountText)
#
#     # 设置总记录数
#     def setTotalRecordLabel(self):
#         szTotalRecordText = ("共%d条" % self.totalRecrodCount)
#         self.totalRecordLabel.setText(szTotalRecordText)
#
#     # 前一页按钮按下
#     def onPrevButtonClick(self):
#         limitIndex = (self.currentPage - 2) * self.PageRecordCount
#         self.recordQuery(limitIndex)
#         self.currentPage -= 1
#         self.updateStatus()
#
#     # 后一页按钮按下
#     def onNextButtonClick(self):
#         limitIndex = self.currentPage * self.PageRecordCount
#         self.recordQuery(limitIndex)
#         self.currentPage += 1
#         self.updateStatus()
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     # 创建窗口
#     example = Child()
#     # 显示窗口
#     example.show()
#     sys.exit(app.exec_())

