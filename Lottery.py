class Lottery(object):
    def __init__(self, description, prize, winningNumbers):
        self.description = description
        self.prize = prize
        self.winningNumbers = winningNumbers

    def isWin(self, paisNumber):
        if(len(self.winningNumbers) == 0):
            return False
        paisNumberWithMask = self.getPaisNumber(paisNumber)
        for winningNumber in self.winningNumbers:
            if(winningNumber == paisNumberWithMask):
                return True
        return False


    def getPaisNumber(self, paisNumber):
        testNumber = self.winningNumbers[0]
        if "###" in testNumber:
            return "###" + paisNumber[3:]
        if "##" in testNumber:
            return "##" + paisNumber[2:]
        if "#" in testNumber:
            return "#" + paisNumber[1:]
        return paisNumber