import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from datetime import datetime, timedelta
import logging
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import newspaper

def get_todays_top_ai_news():
    """
    Searches the RSS feed for any news story mentioning "AI" specifically with todays date
    """
    news_url='https://news.google.com/rss/search?q="AI"+after:%s'%(datetime.today().strftime('%Y-%m-%d'))
    Client=urlopen(news_url)
    xml_page=Client.read()
    Client.close()
    soup_page=soup(xml_page,"xml")
    news_list=soup_page.findAll("item")
    return(news_list)

def print_story(i, news_list):
    """
    Takes a news_list object generated by a function like get_todays_top_ai_news()
    Returns the ith story in the RSS feed
    """
    text = ''.join(news_list[i].title.text.split("-")[:-1]).strip() + '\n' + news_list[i].link.text
    return(text)
    #print(text)
    
def summarise_article(url):
    """
    Use the Newspaper package to download the article by url and create an
    extractive summary of the article
    Returns string including the summary and the reduction %
    """
    article_name = newspaper.Article(url)
    article_name.download()
    article_name.parse()
    article_name.nlp()
    return(article_name.summary + '\n\n' + 'Article reduced by ' + str(round(100 * (1 - len(article_name.summary) / len(article_name.text)), 1)) + '%!')
    
def print_summary(i, news_list):
    """
    Takes a news_list object generated by a function like get_todays_top_ai_news()
    Returns a summary of the the ith story in the RSS feed
    """    
    summary_text = 'TL;DR - summarising "' + ''.join(news_list[i].title.text.split("-")[:-1]).strip() + '"...\n\n' + summarise_article(news_list[i].link.text)
    return(summary_text)
    
def print_multiple_ai_stories(n, news_list):
    """
    Print multiple stories for the AI search and compile them into a text string
    Takes a news_list item generated by get_todays_top_ai_news() and returns 
    the n top news stories
    """
    text_string = 'Your top AI News for ' + datetime.today().strftime( '%d %b %Y') + '\n\n'
    
    for i in range(n):
        text_string =  text_string + print_story(i, news_list) + '\n' + '-'*60 + '\n\n'
    return(text_string)


def get_todays_top_ai_news():
    """
    Searches the RSS feed for any news story mentioning "AI" specifically with todays date
    """
    news_url='https://news.google.com/rss/search?q="AI"+after:%s'%(datetime.today().strftime('%Y-%m-%d'))
    Client=urlopen(news_url)
    xml_page=Client.read()
    Client.close()
    soup_page=soup(xml_page,"xml")
    news_list=soup_page.findAll("item")
    return(news_list)



def print_story(i, news_list):
    """
    Takes a news_list object generated by a function like get_todays_top_ai_news()
    Returns the ith story in the RSS feed
    """
    text = ''.join(news_list[i].title.text.split("-")[:-1]).strip() + '\n' + news_list[i].link.text
    return(text)
    #print(text)
    
def summarise_article(url):
    """
    Use the Newspaper package to download the article by url and create an
    extractive summary of the article
    Returns string including the summary and the reduction %
    """
    article_name = newspaper.Article(url)
    article_name.download()
    article_name.parse()
    article_name.nlp()
    return(article_name.summary + '\n\n' + 'Article reduced by ' + str(round(100 * (1 - len(article_name.summary) / len(article_name.text)), 1)) + '%!')
    
def print_summary(i, news_list):
    """
    Takes a news_list object generated by a function like get_todays_top_ai_news()
    Returns a summary of the the ith story in the RSS feed
    """    
    summary_text = 'TL;DR - summarising "' + ''.join(news_list[i].title.text.split("-")[:-1]).strip() + '"...\n\n' + summarise_article(news_list[i].link.text)
    return(summary_text)
    
def print_multiple_ai_stories(n, news_list):
    """
    Print multiple stories for the AI search and compile them into a text string
    Takes a news_list item generated by get_todays_top_ai_news() and returns 
    the n top news stories
    """
    text_string = 'Your top AI News for ' + datetime.today().strftime( '%d %b %Y') + '\n\n'
    
    for i in range(n):
        text_string =  text_string + print_story(i, news_list) + '\n' + '-'*60 + '\n\n'
    return(text_string)


def post_to_ai_news(news_list):
    """
    Post top news stories to the AI-News channel in slack
    """
    #channel_id = "C04069VQ02H"
    num_stories = 5
    return(post_message_to_channel(print_multiple_stories(num_stories, news_list), 'ai-news', return_message_id = True))

def post_reply_to_ai_news_post(message, news_list):
    """
    Reply to the AI news post with a summary of each of the top stories as individual comments
    """
    num_stories = 5
    for i in range(num_stories):
        post_reply_to_message(message, print_summary(i, news_list))


# WebClient instantiates a client that can call API methods
# send to slack
app_id = 'A0402KG981L'
oauth_token = 'xoxb-3299368583506-3994739416871-rAYwtDuFcCFswbSe6lQuRNxA'
client = WebClient(token=oauth_token)
logger = logging.getLogger(__name__)

# create news_list object
news_list = get_todays_top_ai_news()

# pass to ai news function that creates top 5 news stories message
# and sends to the ai-news channel
ai_news = post_to_ai_news(news_list)

# Post reply to message_id as from the original AI post
post_reply_to_ai_news_post(ai_news, news_list)