import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup

current_year = '2018'

def main():
    downloadYear(current_year)

def downloadYear(year):
    url = 'https://developer.apple.com/videos/wwdc' + str(year) +  '/'
    soup = BeautifulSoup(urllib2.urlopen(url).read(), "html.parser")
    container = soup.find_all('section', 'column large-4 small-12 no-padding-top no-padding-bottom')
    if not container:
        print 'can not find anything match.'
        return

    print 'finding...'
    for section in container:
        link = section.find('a')
        if link.has_attr('href'):
            #/videos/play/wwdc2018/416/
            href = link['href']
            session_id = href.split('/')[-2]
            downloadSessionVideo(current_year, session_id)
    print 'all done'


def downloadSessionVideo(year, sessionID):
    url = 'https://developer.apple.com/videos/play/wwdc' + year + '/' + sessionID + '/'
    page = BeautifulSoup(urllib2.urlopen(url).read(), "html.parser")
    title = page.find('title').text.split('-')[0].strip()
    print '\n\n'+title
    resource = page.find('ul', 'options')
    if not resource:
        print '%s has no videos currently' % title
        return
    all_links = resource.find_all('a')
    filename = 'wwdc%svideos_links.txt' % current_year
    with open(filename, 'a') as wf:
        for a_href in all_links:
            wf.write(a_href['href'].strip() + '\n')

if __name__ == '__main__':
    main()
