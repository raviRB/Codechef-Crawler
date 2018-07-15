import urllib2
from bs4 import BeautifulSoup
import urlparse
import os, sys
import re
import timeit

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)


def solution_url(sub_url):
    req = urllib2.Request(urlparse.urljoin("https://www.codechef.com",sub_url),headers={'User-Agent': 'Mozilla/5.0'})
    socket_connection = urllib2.urlopen(req)
    soup = BeautifulSoup(socket_connection, 'html.parser')
    links = soup.findAll("table", class_="dataTable")
    all_sol = links[0].findAll("tbody")
    all_sol = all_sol[0].findAll('tr')
    accepted_solution = all_sol[0].findAll('a')
    get_accepted_solution(accepted_solution[1]['href'])


def get_accepted_solution(sub_url):
    req = urllib2.Request(urlparse.urljoin("https://www.codechef.com", sub_url), headers={'User-Agent': 'Mozilla/5.0'})
    socket_connection = urllib2.urlopen(req)
    # print(data)
    soup = BeautifulSoup(socket_connection, 'html.parser')
    lang = soup.findAll("pre")
    lang = lang[0]["class"]
    extension =lang[0]
    soup = soup.find("div",id="solutiondiv")
    soup = soup.findAll('li')
    f = open(user+"/Codechef-Solutions/"+problem_code+"."+extension, "w+")
    try:
        print "Fetching Solution - ", problem_code
        for line in soup:
            f.write(line.text)
            f.write("\n")
    except:
        print "Error while fetching Solution - ",problem_code



def get_users_solution():
    global user
    print("<---------------CODECHEF CRAWLER--------------->")
    user = raw_input("Enter user name: ")
    print("Fetching Solutions of user : "+user)
    createFolder(user+"/Codechef-Solutions")
    URL = "https://www.codechef.com/users/"+user
    start = timeit.default_timer()
    req = urllib2.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    socket_connection = urllib2.urlopen(req)
    soup = BeautifulSoup(socket_connection, 'html.parser')
    all_solutions = soup.find("section", class_="rating-data-section problems-solved")
    all_solutions_links = all_solutions.find_all('a')
    print len(all_solutions_links)," solutions found !!"
    for link in all_solutions_links:
        global problem_code
        problem_code = re.findall('/status/([A-Za-z0-9]+)', link['href'])
        problem_code = problem_code[0]
        solution_url(link['href'])
    stop = timeit.default_timer()
    print "All Problems Fetched in - ",stop-start," seconds "

get_users_solution()