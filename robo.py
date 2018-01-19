# for grabing
from lxml import html
import requests
# for telegram 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# PYTHON TELEGRAM SCRIPT 

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('Help!')


def echo(bot, update):
	post=""
	pltoshow=""
	altshow=""
	tagshow=""
	searched=update.message.text
	urlsearched="http://alternativeto.net/browse/search/?q="+searched+"&ignoreExactMatch=true"
	searchedpage = requests.get(urlsearched)
	searchedtree = html.fromstring(searchedpage.content)
	searchedlink=searchedtree.xpath('//a[@data-link-action="Search"]/@href')
	url="http://alternativeto.net"+searchedlink[0]
	page = requests.get(url)
	tree = html.fromstring(page.content)
	title=tree.xpath('//h1[@itemprop="name"]/text()')
	tags=tree.xpath('//span[@class="label label-default"]/text()')
	platforms=tree.xpath('//li[@class="label label-default "]/text()')
	#image=tree.xpath('//div[@class="image-wrapper"]/img[@src]')
	alternativs=tree.xpath('//a[@data-link-action="Alternatives"]/text()')
	creatorwebsite=tree.xpath('//a[@class="ga_outgoing"]/@href')
	post+="Titles:"+title[0]
	for x in range(0,len(platforms)):
		pltoshow+="#"+platforms[x]+"\n"
	post+="Platforms :"+"\n"+pltoshow+"\n"
	for y in range(0,len(alternativs)):
		altshow+=alternativs[y]+"\n"
	post+="Alternatives :"+"\n"+altshow+"\n"
	for z in range(0,len(tags)):
		tagshow+="#"+tags[z]+"\n"
	post+="genres:"+"\n"+tagshow
	try:
		post+="Website:"+"\n"+creatorwebsite[0]
	except IndexError:
		print(title[0]+"Not Found !")
	update.message.reply_text(post)
	



def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("93874105:AAHfF-V6VkeqODiOX3K1LwsKu_e7VlJHRCI")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
	main()
	