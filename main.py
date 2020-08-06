import json
import codecs
from PaisSubscriber import GetLotteryList
from TelegramWrapper import TelegramWrapper

lottery_log_file_name = 'lottery.log'

def isLotteryExists(file_name, lotteryInfo):
    logfile = codecs.open(file_name, 'rb', "iso-8859-8")
    loglist = logfile.readlines()
    logfile.close()

    for line in loglist:
        decoded_data = str(line) #.("iso-8859-8")
        if str(lotteryInfo) in decoded_data:
            return True

    return False

def addLotteryToFile(file_name, lotteryInfo):
    logfile = open(file_name, 'ab')
    encodelotteryInfo = str(lotteryInfo + "\n").encode("iso-8859-8")
    # text = lotteryInfo.decode("cp1255")
    # text = lotteryInfo.decode("cp862")
    logfile.write(encodelotteryInfo)
    logfile.close()


def main():
    with open('config.json') as json_file:
        data = json.load(json_file)
        paisNumber = str(data["PaisNumber"])
        # telegram credentials
        telegram_chat_id = str(data["TelegramChatId"])
        telegram_token = str(data["TelegramToken"])

    url = r'https://www.pais.co.il/subscriber/'
    lotteryInfo, LotteryList = GetLotteryList(url)

    if(isLotteryExists(lottery_log_file_name, lotteryInfo)):
        return

    winList = []
    for lottery in LotteryList:
        if (lottery.isWin(paisNumber)):
            print("Win {}".format(lottery.description))
            winList.append(lottery)

    winListLen = len(winList)

    telegramWrapper = TelegramWrapper(telegram_chat_id, telegram_token)
    msg = lotteryInfo
    if (winListLen > 0):
        if(winListLen > 1):
            msg = msg + " -\nמנוי מספר {} זכה בהגרלה ב {} פרסים:\n".format(paisNumber, winListLen)
        else:
            msg = msg + " -\nמנוי מספר {} זכה בהגרלה בפרס אחד:\n".format(paisNumber)

        for i in range(winListLen):
            p = winList[i].prize
            if (winListLen > 1):
                msg = "{}{}. {}.\n".format(msg, i + 1 , p)
            else:
                msg = "{}{}.".format(msg, p)
    else:
        msg = msg + " -\nמנוי מספר {} לא זכה.".format(paisNumber)
    telegramWrapper.send_message(msg)
    addLotteryToFile(lottery_log_file_name, lotteryInfo)

if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
