import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from api import get_worker_stats
from time import strftime

app = QtWidgets.QApplication(sys.argv)

class Dashboard(QtWidgets.QWidget):


    def __init__(self, wallet):
        super().__init__()

        self.wallet = wallet
        stats = get_worker_stats(self.wallet)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda:self.refresh())
        self.timer.start(60000)

        if stats is not None:
            self.wallet = stats['miner']
            self.totalHash = stats['totalHash']
            self.totalShares = stats['totalShares']
            self.immature = stats['immature']
            self.mature = stats['mature']
            self.paid = stats['paid']
            self.workers_Name = []
            self.workers_HashString = []
            self.workers_High = []
            self.workers_Low = []
            self.workers_Sum = []
            self.workers_Avg = []
            self.workers_Shares = []
            self.workers_CurrRoundShares = []
            self.totalWorker = 0

            workers = stats['workers']
            for a, b in enumerate(workers):
                self.workers_Name.append(workers[b]['name'].replace(wallet + ".", ""))
                self.workers_HashString.append(workers[b]['hashrateString'])
                hashrate = float(workers[b]['hashrate'])
                self.workers_High.append(hashrate)
                self.workers_Low.append(hashrate)
                self.workers_Sum.append(hashrate)
                self.workers_Avg.append(hashrate)
                self.workers_Shares.append(workers[b]['shares'])
                self.workers_CurrRoundShares.append(workers[b]['currRoundShares'])
                self.totalWorker = a + 1

        else:
            print('[!] Request Failed')

        self.t = "luqman noob"

        self.count = 1

        self.init_ui()

    def init_ui(self):

        self.poolLabel = QtWidgets.QLabel('Threeeyed RVN')
        self.poolLogo = QtWidgets.QLabel()
        self.poolLogo.setPixmap(QtGui.QPixmap('logo.png'))

        self.walletLabel = QtWidgets.QLabel('Wallet Address: {}'.format(self.wallet))
        self.totalHashLabel = QtWidgets.QLabel('Total Hashrate: {}'.format(self.totalHash))
        self.totalSharesLabel = QtWidgets.QLabel('Total Shares: {}'.format(self.totalShares))
        self.paidLabel = QtWidgets.QLabel('Paid: {}'.format(self.paid))
        self.matureLabel = QtWidgets.QLabel('Mature: {}'.format(self.mature))
        self.immatureLabel = QtWidgets.QLabel('Immature: {}'.format(self.immature))

        self.workers_NameLabel = []
        self.workers_HashStringLabel = []
        self.workers_HighLabel = []
        self.workers_AvgLabel = []
        self.workers_LowLabel = []
        self.workers_SharesLabel = []
        self.workers_CurrRoundSharesLabel = []

        for x in range(0, self.totalWorker):
            self.workers_NameLabel.append(QtWidgets.QLabel('Worker {0}: {1}'.format(x+1, self.workers_Name[x])))
            self.workers_HashStringLabel.append(QtWidgets.QLabel('Hashrate: {}'.format(self.workers_HashString[x])))
            self.workers_AvgLabel.append(QtWidgets.QLabel('Average: {}'.format(self.workers_Avg[x])))
            self.workers_HighLabel.append(QtWidgets.QLabel('High: {}'.format(self.workers_High[x])))
            self.workers_LowLabel.append(QtWidgets.QLabel('Low: {}'.format(self.workers_Low[x])))
            self.workers_SharesLabel.append(QtWidgets.QLabel('Shares: {}'.format(self.workers_Shares[x])))
            self.workers_CurrRoundSharesLabel.append(QtWidgets.QLabel('Current Round Shares: {}'.format(self.workers_CurrRoundShares[x])))

        self.refreshButton = QtWidgets.QPushButton('Refresh')
        self.refreshButton.clicked.connect(self.refresh)

        v_box = QtWidgets.QVBoxLayout()
        h_box1 = QtWidgets.QHBoxLayout()
        h_box1.addWidget(self.poolLogo)
        h_box1.addWidget(self.poolLabel)
        h_box1.addStretch()
        h_box1.addWidget(self.refreshButton)
        v_box.addLayout(h_box1)
        h_box2 = QtWidgets.QHBoxLayout()
        h_box2.addStretch()
        h_box2.addWidget(self.walletLabel)
        h_box2.addStretch()
        v_box.addLayout(h_box2)
        h_box3 = QtWidgets.QHBoxLayout()
        h_box3.addWidget(self.totalHashLabel)
        h_box3.addStretch()
        h_box3.addWidget(self.totalSharesLabel)
        v_box.addLayout(h_box3)
        h_box4 = QtWidgets.QHBoxLayout()
        h_box4.addWidget(self.paidLabel)
        h_box4.addStretch()
        h_box4.addWidget(self.matureLabel)
        h_box4.addStretch()
        h_box4.addWidget(self.immatureLabel)
        v_box.addLayout(h_box4)

        for x in range(0, self.totalWorker):
            h_box5 = QtWidgets.QHBoxLayout()
            h_box5.addStretch()
            h_box5.addWidget(self.workers_NameLabel[x])
            h_box5.addStretch()
            v_box.addLayout(h_box5)
            v_box.addWidget(self.workers_HashStringLabel[x])
            h_box6 = QtWidgets.QHBoxLayout()
            h_box6.addWidget(self.workers_HighLabel[x])
            h_box6.addStretch()
            h_box6.addWidget(self.workers_AvgLabel[x])
            h_box6.addStretch()
            h_box6.addWidget(self.workers_LowLabel[x])
            v_box.addLayout(h_box6)
            v_box.addWidget(self.workers_SharesLabel[x])
            v_box.addWidget(self.workers_CurrRoundSharesLabel[x])


        print(self.t)
        self.setLayout(v_box)
        self.setWindowTitle('Threeeyed Pool Monitor')
        self.show()

    def updateAgent(self):
        self.count = self.count + 1
        stats = get_worker_stats(self.wallet)
        if stats is not None:
            self.wallet = stats['miner']
            self.totalHash = stats['totalHash']
            self.totalShares = stats['totalShares']
            self.immature = stats['immature']
            self.mature = stats['mature']
            self.paid = stats['paid']

            workers = stats['workers']
            for a, b in enumerate(workers):
                self.workers_Name[a] = workers[b]['name'].replace(wallet + ".", "")
                self.workers_HashString[a] = workers[b]['hashrateString']
                hashrate = float(workers[b]['hashrate'])
                if hashrate > self.workers_High[a]:
                    self.workers_High[a] = hashrate
                if hashrate < self.workers_Low[a]:
                    self.workers_Low[a] = hashrate
                self.workers_Sum[a] = self.workers_Sum[a] + hashrate
                self.workers_Avg[a] = self.workers_Sum[a] / self.count
                self.workers_Shares[a] = workers[b]['shares']
                self.workers_CurrRoundShares[a] = workers[b]['currRoundShares']

        else:
            print('[!] Request Failed')

    def updateDashboard(self):
        self.walletLabel.setText('Wallet Address: {}'.format(self.wallet))
        self.totalHashLabel.setText('Total Hashrate: {}'.format(self.totalHash))
        self.totalSharesLabel.setText('Total Shares: {}'.format(self.totalShares))
        self.paidLabel.setText('Paid: {}'.format(self.paid))
        self.matureLabel.setText('Mature: {}'.format(self.mature))
        self.immatureLabel.setText('Immature: {}'.format(self.immature))

        for x in range(0, self.totalWorker):
            self.workers_NameLabel[x].setText('Worker {0}: {1}'.format(x+1, self.workers_Name[x]))
            self.workers_HashStringLabel[x].setText('Hashrate: {}'.format(self.workers_HashString[x]))
            self.workers_AvgLabel[x].setText('Average: {}'.format(self.workers_Avg[x]))
            self.workers_HighLabel[x].setText('High: {}'.format(self.workers_High[x]))
            self.workers_LowLabel[x].setText('Low: {}'.format(self.workers_Low[x]))
            self.workers_SharesLabel[x].setText('Shares: {}'.format(self.workers_Shares[x]))
            self.workers_CurrRoundSharesLabel[x].setText('Current Round Shares: {}'.format(self.workers_CurrRoundShares[x]))


    def refresh(self):
        self.updateAgent()
        self.updateDashboard()
        print(self.count)


wallet = '#walletaddresshere'

d = Dashboard(wallet)



sys.exit(app.exec_())
