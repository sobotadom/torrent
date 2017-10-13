
from PyQt4 import QtCore, QtGui
from tvInfo import seasonBuilder, episodeBuilder
from torrentSearch import torrentSearch
import sys
import time
import datetime
import webbrowser
import urllib

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_showSearch(object):

    def setupUi(self, showSearch):

        self.seasons = {}    #
        self.selected_episode = ''
        self.selected_season = ''
        self.episode_number = ''
        self.searched_name = ''
        self.torrents = {}

        # General GUI Setup
        showSearch.setObjectName(_fromUtf8("showSearch"))
        showSearch.resize(1900, 750)
        showSearch.setMouseTracking(False)
        showSearch.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        showSearch.setLayoutDirection(QtCore.Qt.RightToLeft)
        showSearch.setAutoFillBackground(False)
        showSearch.setStyleSheet(_fromUtf8(""))
        showSearch.setTabShape(QtGui.QTabWidget.Rounded)

        self.centralwidget = QtGui.QWidget(showSearch)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.searchFrame = QtGui.QFrame(self.centralwidget)
        self.searchFrame.setGeometry(QtCore.QRect(10, 0, 511, 611))
        self.searchFrame.setStyleSheet(_fromUtf8(""))
        self.searchFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.searchFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.searchFrame.setObjectName(_fromUtf8("searchFrame"))

        self.infoFrame = QtGui.QFrame(self.centralwidget)
        self.infoFrame.setGeometry(540, 0, 611, 711)
        self.infoFrame.setStyleSheet(_fromUtf8(""))
        self.infoFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.infoFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.infoFrame.setObjectName(_fromUtf8("infoFrame"))

        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 60, 511, 781))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))

        # Set up Show Search box to input show name
        self.search_query_text = QtGui.QPlainTextEdit(self.searchFrame)
        self.search_query_text.setGeometry(QtCore.QRect(10, 10, 341, 41))
        self.search_query_text.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.search_query_text.setObjectName(_fromUtf8("search_query_text"))

        # Setting up labels for GUI

        self.titleLabel = QtGui.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(580, 0, 491, 100))

        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(30)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)

        self.titleLabel.setFont(font)
        self.titleLabel.setFrameShadow(QtGui.QFrame.Raised)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setWordWrap(True)

        self.infoLabel = QtGui.QLabel(self.centralwidget)
        self.infoLabel.setGeometry(QtCore.QRect(580, 580, 491, 321))
        self.infoLabel.setWordWrap(True)

        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(14)

        self.infoLabel.setFont(font)
        self.infoLabel.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.infoLabel.setObjectName("infoLabel")

        self.listWidget = QtGui.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(1130, 60, 750, 550))
        self.listWidget.setObjectName("results")

        # Create the widget that will show the seasons and then the episodes for that season
        self.results = QtGui.QTreeWidget(self.frame)
        self.header = QtGui.QTreeWidgetItem([" "])
        self.results.setHeaderItem(self.header)

        self.results.setGeometry(5, 1, 501, 561)
        self.results.itemSelectionChanged.connect(self.extract_result)

        # After episode selected, sends torrent information to torrent application
        self.downloadButton = QtGui.QPushButton(self.centralwidget)
        self.downloadButton.setGeometry(QtCore.QRect(1130, 630, 750, 80))
        self.downloadButton.setObjectName("downloadButton")
        self.downloadButton.setText("Download")
        self.downloadButton.clicked.connect(self.handleDownload)
        self.downloadButton.setEnabled(False)

        # The button used to search for show using inputted text in search_query_text
        self.searchButton = QtGui.QPushButton(self.searchFrame)
        self.searchButton.setGeometry(QtCore.QRect(370, 10, 131, 31))
        self.searchButton.setFlat(False)
        self.searchButton.setObjectName(_fromUtf8("searchButton"))
        self.searchButton.clicked.connect(self.handleSearch)

        # the button used to pick a certain episode
        self.selectButton = QtGui.QPushButton(self.frame)
        self.selectButton.setGeometry(QtCore.QRect(6, 570, 511, 81))
        self.selectButton.setAutoDefault(False)
        self.selectButton.setObjectName(_fromUtf8("selectButton"))
        self.selectButton.clicked.connect(self.handleSelect)
        self.selectButton.setEnabled(False)

        # picture of show extracted from imdb
        self.picture = QtGui.QLabel(self.centralwidget)

        # label where the shows name will be displayed

        showSearch.setCentralWidget(self.centralwidget)

        self.toolBar = QtGui.QToolBar(showSearch)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        showSearch.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(showSearch)
        QtCore.QMetaObject.connectSlotsByName(showSearch)

        ######################################

        # if an argument is passed on command line, automatically search
        if len(sys.argv) == 2:
            self.search_query_text.appendPlainText(sys.argv[1])
            self.searchButton.click()

    def handleSearch(self):
        '''
        Takes text from search_query_text and builds the results widget to show
        the show's season and episode information
        '''

        # Reset previous search data
        self.titleLabel.setText('')
        self.infoLabel.setText('')
        self.listWidget.clear()
        self.selectButton.setEnabled(True)

        self.searched_name = self.search_query_text.toPlainText()
        # Extract relevant search data for show
        title, year, show_poster_url, tagline, self.seasons = seasonBuilder(
            self.searched_name)

        self.results.clear()

        self.header.setText(0, title)

        todays_date = datetime.datetime.today()

        for i in range(1, len(self.seasons) + 1):
            # input the season into the results list

            current_season = QtGui.QTreeWidgetItem(["Season " + str(i)])
            self.results.addTopLevelItem(current_season)
            for e in range(1, len(self.seasons[i]) + 1):
                # inputs each episode in the current season into the results list

                temp = ''
                if e in range(1, 10):
                    temp = str(i) + "0" + str(e)
                else:
                    temp = str(i) + str(e)
                episode_description = temp + ": " + str(self.seasons[i][e][0])

                # only show results for shows that have aired
                release_date = datetime.datetime.strptime(
                    self.seasons[i][e][1], '%Y-%m-%d')
                if todays_date > release_date:

                    current_episode = QtGui.QTreeWidgetItem(
                        [episode_description])
                    current_season.addChild(current_episode)

            # Set labels to appropraite information
            self.titleLabel.setText(title + '(' + str(year) + ')')
            self.infoLabel.setText(tagline)
            self.setPicture(show_poster_url)

    def extract_result(self):
        # get the season and episode selection and store it in varaibles

        selected_item = str(self.results.currentItem().text(0)).split(":")[0]

        if len(selected_item) == 3:
            self.selected_season = selected_item[0]
            self.episode_number = selected_item[1:3]

        elif len(selected_item) == 4:
            self.selected_season = selected_item[0:2]
            self.episode_number = selected_item[2:4]

    def handleSelect(self):
        # Reset label information for downloads list
        self.titleLabel.setText('')
        self.infoLabel.setText('')
        self.listWidget.clear()

        if self.episode_number[0] == '0':
            self.episode_number = self.episode_number[1]

        # Get the selected episode information from seasons
        result = self.seasons[int(self.selected_season)
                              ][int(self.episode_number)]

        title, release, imdb_id = result[0], result[1], result[2]
        plot, title = episodeBuilder(imdb_id)

        # formatting issues for single digit episode numbers
        temp1, temp2 = self.selected_season, self.episode_number
        if int(self.selected_season) in range(0, 10):
            temp1 = '0' + self.selected_season[0]
        if int(self.episode_number) in range(0, 10):
            temp2 = '0' + self.episode_number[0]

        # Get torrents based on episode

        self.torrents = torrentSearch(
            self.searched_name, 'S' + temp1 + 'E' + temp2)

        #if torrents == {}:
                # no torrents

            # pass torrents on to download list widget to handle selection of torrent
        for t in self.torrents:
            self.listWidget.addItem(self.torrents[t][0] + " --- " + self.torrents[t][1] + ' --- '
                                    + self.torrents[t][2])

        # Set the appropraite labels with information
        self.titleLabel.setText('S' + temp1 + 'E' + temp2 + ': ' + title)
        self.infoLabel.setText(plot)
        self.downloadButton.setEnabled(True)

    def handleDownload(self):
        # Pressing Download buttons will lead to torrent application to open with
        # the selected torrent
        webbrowser.open(self.torrents[self.listWidget.currentRow()][4])

    def setPicture(self, url):
        # set picutre with url from show

        data = urllib.request.urlopen(url).read()

        image = QtGui.QImage()
        image.loadFromData(data)
        pixmap = QtGui.QPixmap(image)
        self.picture.setPixmap(pixmap)

        self.picture.setGeometry(700, 180, pixmap.width(), pixmap.height())

    def retranslateUi(self, showSearch):
        showSearch.setWindowTitle(_translate("showSearch", "Torrent", None))
        self.searchButton.setText(_translate("showSearch", "Search", None))
        self.selectButton.setText(_translate("showSearch", "Select", None))

        self.toolBar.setWindowTitle(_translate("showSearch", "toolBar", None))


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    showSearch = QtGui.QMainWindow()
    ui = Ui_showSearch()
    ui.setupUi(showSearch)
    showSearch.show()
    sys.exit(app.exec_())
