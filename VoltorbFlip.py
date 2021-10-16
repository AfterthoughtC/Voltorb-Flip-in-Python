# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 09:04:20 2020

@author: AfterthoughtC
"""

from PyQt5 import QtWidgets
from LevelGenerator import np, generate_one_level,create_level_array



class SingleCell(QtWidgets.QWidget):
    
    def __init__(self,memo_mode,button_init = '',parent = None):
        super(SingleCell,self).__init__(parent=None)
        self.initUI(memo_mode,button_init)
        
    def initUI(self,memo_mode,button_init):
        MainLayout = QtWidgets.QVBoxLayout()
        
        if memo_mode:
            self.memoLineEdit = QtWidgets.QLineEdit()
            MainLayout.addWidget(self.memoLineEdit)
        self.openPushButton = QtWidgets.QPushButton(button_init)
        MainLayout.addWidget(self.openPushButton)
        
        self.setLayout(MainLayout)


class CounterCell(QtWidgets.QWidget):
    
    def __init__(self,parent = None):
        super(CounterCell,self).__init__(parent=None)
        self.initUI()
        
    def initUI(self):
        MainLayout = QtWidgets.QVBoxLayout()
        
        self.scoreCountLabel = QtWidgets.QLabel()
        MainLayout.addWidget(self.scoreCountLabel)

        self.bombCountLabel = QtWidgets.QLabel()
        MainLayout.addWidget(self.bombCountLabel)
        
        self.setLayout(MainLayout)


class GameScreen(QtWidgets.QWidget):
    
    def __init__(self,level,grid_size,have_memo,winif,parent = None):
        super(GameScreen,self).__init__(parent=None)
        self.level = level
        self.grid_size = grid_size
        self.have_memo = have_memo
        self.winif = winif
        self.level_stages = generate_one_level(grid_size,level,3)
        self.initUI()
        self.stage_no = 1
        self.current_score = 1
        self.setStage(self.stage_no)
    
    def initUI(self):
        MainLayout = QtWidgets.QVBoxLayout()
        
        self.levelStageLabel = QtWidgets.QLabel()
        MainLayout.addWidget(self.levelStageLabel)
        
        self.currentScoreLabel = QtWidgets.QLabel()
        MainLayout.addWidget(self.currentScoreLabel)
        
        self.MainGrid = QtWidgets.QGridLayout()
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                current_cell = SingleCell(self.have_memo,button_init = 'r'+str(i)+'c'+str(j))
                current_cell.openPushButton.clicked.connect(self.openButtonPushed)
                self.MainGrid.addWidget(current_cell,i,j)
                if i == self.grid_size - 1:
                    self.MainGrid.addWidget(CounterCell(),self.grid_size,j)
            self.MainGrid.addWidget(CounterCell(),i,self.grid_size)
        
        self.backButton = QtWidgets.QPushButton("Back")
        self.MainGrid.addWidget(self.backButton,self.grid_size,self.grid_size+1)
        
        MainLayout.addLayout(self.MainGrid)
        
        self.setLayout(MainLayout)


    def setStage(self,stage):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.MainGrid.itemAtPosition(i,j).widget().openPushButton.setText('r'+str(i)+'c'+str(j))
                self.MainGrid.itemAtPosition(i,j).widget().openPushButton.setDisabled(False)
                if self.have_memo:
                    self.MainGrid.itemAtPosition(i,j).widget().memoLineEdit.setText('')
                    self.MainGrid.itemAtPosition(i,j).widget().memoLineEdit.setDisabled(False)
        self.levelStageLabel.setText('Level '+str(self.level)+' Stage '+str(stage))
        self.currentScoreLabel.setText('Score: '+str(self.current_score))
        self.goodno = sum(self.level_stages[stage-1][2:])
        self.opengood = 0
        self.safeno = sum(self.level_stages[stage-1][1:])
        self.opensafe = 0
        self.current_level_array = create_level_array(self.level_stages[stage-1])
        row_sum = np.sum(self.current_level_array,axis = 1)
        row_zeros = self.grid_size - np.count_nonzero(self.current_level_array,axis = 1)
        for i in range(self.grid_size):
            self.MainGrid.itemAtPosition(i,self.grid_size).widget().scoreCountLabel.setText('Row Sum: '+str(int(row_sum[i])))
            self.MainGrid.itemAtPosition(i,self.grid_size).widget().bombCountLabel.setText('Bomb(s): '+str(row_zeros[i]))
        
        col_sum = np.sum(self.current_level_array,axis = 0)
        col_zeros = self.grid_size - np.count_nonzero(self.current_level_array,axis = 0)
        for j in range(self.grid_size):
            self.MainGrid.itemAtPosition(self.grid_size,j).widget().scoreCountLabel.setText('Column Sum: '+str(int(col_sum[j])))
            self.MainGrid.itemAtPosition(self.grid_size,j).widget().bombCountLabel.setText('Bomb(s): '+str(col_zeros[j]))

    
    def openButtonPushed(self):
        button = self.sender()
        r,c = self.MainGrid.getItemPosition(self.MainGrid.indexOf(button.parent()))[0:2]
        multiplier = int(self.current_level_array[r,c])
        if multiplier >= 1:
            self.opensafe += 1
        if multiplier >= 2:
            self.opengood += 1
        self.current_score *= multiplier
        button.setText(str(multiplier))
        button.setDisabled(True)
        if self.have_memo:
            button.parent().memoLineEdit.setDisabled(True)
        self.currentScoreLabel.setText('Score: '+str(self.current_score))
        if self.current_score == 0:
            QtWidgets.QMessageBox.about(self, "","Boomz! You failed!")
            self.parent().load_startscreen()
        win = self.checkWin()
        if win:
            QtWidgets.QMessageBox.about(self, "","You have opened all the "+self.winif+" tiles!")
            if self.stage_no == 5:
                self.parent().load_startscreen()
            else:
                self.stage_no += 1
                self.setStage(self.stage_no)
    
    
    def checkWin(self):
        if self.winif == 'good':
            return(self.opengood >= self.goodno)
        elif self.winif == 'safe':
            return(self.opensafe >= self.safeno)


class StartScreen(QtWidgets.QWidget):
    
    def __init__(self,default_level = 1,default_size = 6,have_memo = True,parent = None):
        super(StartScreen, self).__init__(parent = None)
        self.initUI(default_level,default_size,have_memo)
    
    def initUI(self,default_level,default_size,have_memo):
        MainLayout = QtWidgets.QVBoxLayout()
        
        askwhat=QtWidgets.QLabel("Choose your game settings.")
        MainLayout.addWidget(askwhat)
        
        levelLayout = QtWidgets.QHBoxLayout()
        
        level = QtWidgets.QLabel("Level:")
        levelLayout.addWidget(level)
        
        self.levelSpinBox = QtWidgets.QSpinBox()
        self.levelSpinBox.setRange(1,8)
        self.levelSpinBox.setValue(default_level)
        levelLayout.addWidget(self.levelSpinBox)
        
        MainLayout.addLayout(levelLayout)
        
        gridSizeLayout = QtWidgets.QHBoxLayout()
        gridSize = QtWidgets.QLabel("Grid Size:")
        gridSizeLayout.addWidget(gridSize)
        
        self.sizeSpinBox = QtWidgets.QSpinBox(self)
        self.sizeSpinBox.setRange(5,10)
        self.sizeSpinBox.setValue(default_size)
        gridSizeLayout.addWidget(self.sizeSpinBox)
        
        MainLayout.addLayout(gridSizeLayout)
        
        haveMemoLayout = QtWidgets.QHBoxLayout()
        self.haveMemoCheckBox = QtWidgets.QCheckBox("Allow memo writing.")
        haveMemoLayout.addWidget(self.haveMemoCheckBox)
        if have_memo:
            self.haveMemoCheckBox.setCheckState(2)
        else:
            self.haveMemoCheckBox.setCheckState(0)
        MainLayout.addLayout(haveMemoLayout)
        
        winAtLayout = QtWidgets.QHBoxLayout()
        startText = QtWidgets.QLabel('Progress when all ')
        winAtLayout.addWidget(startText)
        self.winComboBox = QtWidgets.QComboBox()
        self.winComboBox.addItem('good')
        self.winComboBox.addItem('safe')
        winAtLayout.addWidget(self.winComboBox)
        endText = QtWidgets.QLabel(' tiles have been flipped.')
        winAtLayout.addWidget(endText)
        MainLayout.addLayout(winAtLayout)
        
        startButtonLayout = QtWidgets.QHBoxLayout()
        startButtonLayout.addStretch(1)
        
        self.startPushButton = QtWidgets.QPushButton('Start Game')
        startButtonLayout.addWidget(self.startPushButton)
        
        MainLayout.addLayout(startButtonLayout)
        
        MainLayout.addStretch(1)
        
        self.setLayout(MainLayout)


class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Voltorb Flip')
        self.load_startscreen()
        self.show()
     
    def load_startscreen(self):
        self.StartScreen = StartScreen()
        self.setCentralWidget(self.StartScreen)
        self.StartScreen.startPushButton.clicked.connect(self.load_gamescreen)
    
    def load_gamescreen(self):
        grid_size = int(self.StartScreen.sizeSpinBox.value())
        level = int(self.StartScreen.levelSpinBox.value())
        have_memo = self.StartScreen.haveMemoCheckBox.isChecked()
        winif = self.StartScreen.winComboBox.currentText()
        self.GameScreen = GameScreen(level,grid_size,have_memo,winif)
        self.GameScreen.backButton.clicked.connect(self.load_startscreen)
        self.setCentralWidget(self.GameScreen)
    
    
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())
        