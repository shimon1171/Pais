import sys
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


def main(jsonFilePath):
    with open(jsonFilePath) as json_file:
        data = json.load(json_file)
        paisNumber = str(data["PaisNumber"])
        # telegram credentials
        telegram_chat_id = str(data["TelegramChatId"])
        telegram_token = str(data["TelegramToken"])

    url = r'https://www.pais.co.il/subscriber/'
    # url = r'https://www.pais.co.il/Subscriber/showMoreResults.aspx?fromIndex=0&amount=1&fromDate=2020&toDate=44/2020'
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

if __name__ == "__main__":
    print("Start")
    if(len(sys.argv) != 2):
        print("The script input is json file path, we will set the jsom file to local folder")
        jsonFilePath = 'config.json'
    else:
        jsonFilePath = sys.argv[1]
    print(jsonFilePath)
    main(jsonFilePath)