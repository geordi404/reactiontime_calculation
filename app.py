import sys
import random
import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import QTimer, QElapsedTimer

class ReactionButton(QPushButton):
    def __init__(self, app_instance=None, text='', parent=None):
        super().__init__(text, parent)  # Initialize the superclass
        self.app_instance = app_instance  # Store the main application instance

    def mousePressEvent(self, event):
        # Call recordReaction on the stored app_instance if it exists
        if self.isEnabled() and self.app_instance:  # Check if app_instance is not None
            self.app_instance.recordReaction()
        super().mousePressEvent(event)

class ReactionTimeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reaction Time Quantifier")
        self.setGeometry(100, 100, 400, 200)

        # List to store reaction times
        self.reactionTimes = []

        # Timer to wait random interval before showing stimulus
        self.waitTimer = QTimer(self)
        self.waitTimer.timeout.connect(self.showStimuli)

        # Elapsed Timer for measuring reaction time
        self.reactionTimer = QElapsedTimer()

        # Timer for the total duration of the test (1 minute = 60000 ms)
        self.totalTimer = QTimer(self)
        self.totalTimer.timeout.connect(self.endTest)
        self.totalTimer.start(120000)  # Start the 1-minute timer

        # Setup UI
        self.initUI()

        # Reaction Started Flag
        self.reactionStarted = False

    def initUI(self):
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout()

        self.instructionLabel = QLabel("Wait for the signal then click as fast as you can!", self)
        self.layout.addWidget(self.instructionLabel)

        # Use ReactionButton instead of QPushButton
        self.clickButton = ReactionButton(app_instance=self, text='Click when ready', parent=self)
        self.clickButton.clicked.connect(self.prepareStimuli)
        self.clickButton.setMinimumSize(200, 200)
        button_style = """
        QPushButton {font-size: 24px; background-color: grey; color: black;}
        QPushButton:hover {background-color: lightgrey;}
        QPushButton:pressed {background-color: darkgrey;}
        """
        self.clickButton.setStyleSheet(button_style)
        self.layout.addWidget(self.clickButton)

        self.reactionTimeLabel = QLabel("", self)
        self.layout.addWidget(self.reactionTimeLabel)

        self.centralWidget.setLayout(self.layout)

    def prepareStimuli(self):
        self.clickButton.setEnabled(False)
        self.clickButton.setText('Wait...')
        button_style_inactive = """
        QPushButton {font-size: 24px; background-color: grey; color: black;}
        QPushButton:hover {background-color: lightgrey;}
        QPushButton:pressed {background-color: darkgrey;}
        """
        self.clickButton.setStyleSheet(button_style_inactive)
        self.instructionLabel.setText("Get ready...")
        self.reactionTimeLabel.setText("")
        self.reactionStarted = False
        self.waitTimer.start(random.randint(3000, 6000))  # Random interval before showing stimulus

    def showStimuli(self):
        self.waitTimer.stop()
        self.clickButton.setEnabled(True)
        self.clickButton.setText('Click NOW!')
        button_style_active = """
        QPushButton {font-size: 24px; background-color: red; color: white;}
        QPushButton:hover {background-color: darkred;}
        QPushButton:pressed {background-color: #d60000;}
        """
        self.clickButton.setStyleSheet(button_style_active)
        self.instructionLabel.setText("Now!")
        self.reactionTimer.start()  # Start timing the reaction
        self.reactionStarted = True

    def recordReaction(self):
        print("Reaction Recorded")
        if self.reactionStarted:
            reactionTime = self.reactionTimer.elapsed()
            self.reactionTimes.append(reactionTime)  # Store each reaction time
            self.reactionTimeLabel.setText(f"Reaction Time: {reactionTime} ms")
            self.prepareStimuli()  # Prepare for next stimulus
            self.reactionStarted = False

    def endTest(self):
        self.waitTimer.stop()
        self.totalTimer.stop()
        self.clickButton.setEnabled(False)
        self.clickButton.setText('Test Completed')
        self.instructionLabel.setText("Test is over, thank you for participating.")
        with open('reaction_times.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Reaction Time (ms)'])
            for time in self.reactionTimes:
                writer.writerow([time])
        self.reactionTimeLabel.setText("Data saved to reaction_times.csv")

    def mousePressEvent(self, event):
        # Check if the click is within the button and if the button is enabled
        print("Mouse Pressed")
        if self.clickButton.isEnabled() and self.clickButton.underMouse():
            self.recordReaction()
        super().mousePressEvent(event)

# Application execution
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReactionTimeApp()
    ex.show()
    sys.exit(app.exec())