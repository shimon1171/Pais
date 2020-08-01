from requests import get
from bs4 import BeautifulSoup
import validators
from Lottery import Lottery

def GetLotteryList(url):
    if (validators.url(url) == False):
        print("ERROR - Bad URL")
        return
    url = url

    response = get(url)
    html_soup = BeautifulSoup(response.content, 'html.parser')

    # Get lottery Info
    info = html_soup.find('div', class_='cat_h_info')
    lotteryDescription = info.h2.text
    lotteryDate = info.div.text
    lotteryInfo = lotteryDescription + " " + lotteryDate

    # Get lottery results
    members_group = html_soup.find('div', class_='cat_h_members_group')
    members_arch_title = members_group.findAll('h2', attrs={'class': 'members_arch_title'})
    category = members_group.findAll('div', attrs={'class': 'home_news_title category'})
    lot_rezults_list = members_group.findAll('ol', attrs={'class': 'lot_rezults_list w-clearfix w-list-unstyled'})

    print(len(members_arch_title))
    print(len(category))
    print(len(lot_rezults_list))

    LotteryList = []

    for i in range(len(members_arch_title)):
        text = members_arch_title[i].text
        prize = category[i].text
        description = "{} {}".format(text, prize)

        winningNumbers = []
        wins_numbers = lot_rezults_list[i].findAll('li', attrs={'class': 'lot_results_item'})
        for d in wins_numbers:
            print(d)
            subscription = d.div.get('aria-label')
            try:
                winningNumber = subscription.split()[2]
                winningNumbers.append(winningNumber)
            except:
                print(subscription)

        LotteryList.append(Lottery(description, prize, winningNumbers))

    return lotteryInfo, LotteryList



