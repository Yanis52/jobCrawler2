
import re
import bs4 as bs
from urllib.request import urlopen, Request
import pandas as pd
# connect psotgres
import psycopg2

# Connect to your postgres DB


def scrape_jobs():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.google.com/',
        'DNT': '1'  # Do Not Track Request Header
    }
    # liste de toutes les ville de france en string
    liste_ville=['pairs','marseille']
    liste_metier=['data+scientist','data+analyst']
    
    # URL de la page Indeed à scraper
    source = 'https://www.indeed.com/jobs?q=$data+scientist&l=Marseille&radius=10'
    req = Request(url=source, headers=headers)
    try:
        html = urlopen(req).read()
    except Exception as e:
        print(f"Failed to retrieve webpage: {e}")
        return None
    
    # Créer un arbre de parsing avec BeautifulSoup
    soup = bs.BeautifulSoup(html, 'lxml')
    
    # Créer des listes pour les titres et les liens des offres d'emploi
    job_titles = []
    job_links = []
    job_descriptions = []
    job_companies = []
    # job_types = []
    
    # Récupérer tous les titres et les liens des offres d'emploi
    for tag in soup.findAll('h2', {'class': 'jobTitle'}):
        a_tag = tag.find('a')
        if a_tag:
            job_title = a_tag.get_text()
            job_link = a_tag.get('href')
            job_titles.append(job_title)
            description = scrape_job_description(job_link)
            job_descriptions.append(description)
            job_links.append(f"https://www.indeed.com{job_link}")
            compagnie= scrapCompagnie(job_link)
            job_companies.append(compagnie)
            # job_type=scrapType(job_link)
            # job_types.append(job_type)
            # Récupérer le nom de l'entreprise et le type de poste
           
           
                

    # Créer un DataFrame à partir des données extraites
    results = pd.DataFrame({'Job Titles': job_titles, 'Job Links': job_links, 'Job Descriptions': job_descriptions, 'Job Companies': job_companies,
                            #  'Job Type': job_type
                             })
    return results

def scrape_job_description(link):
        
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://www.google.com/',
    'DNT': '1'  # Do Not Track Request Header
    }
    try:
        req = Request(url='https://www.indeed.com'+link, headers=headers)
        html = urlopen(req).read()
        soup = bs.BeautifulSoup(html, 'html.parser')
        description = soup.find('div', class_='jobsearch-JobComponent-description css-16y4thd eu4oa1w0').get_text(separator=' ')
        return description
    except Exception as e:
        print(f"Failed to retrieve job description: {e}")
        return 'No description'
def scrapCompagnie(link):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://www.google.com/',
    'DNT': '1'  # Do Not Track Request Header
    }
    try:
        req = Request(url='https://www.indeed.com'+link, headers=headers)
        html = urlopen(req).read()
        soup = bs.BeautifulSoup(html, 'html.parser')
        compagnie  = soup.find('a', class_='css-1ioi40n e19afand0').get_text()
        return compagnie
    except Exception as e:
        print(f"Failed to retrieve job compagnie: {e}")
        return 'No compagnie'
# def scrapType(link):
#     headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#     'Accept-Language': 'en-US,en;q=0.9',
#     'Connection': 'keep-alive',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Referer': 'https://www.google.com/',
#     'DNT': '1'  # Do Not Track Request Header
#     }
#     try:
#         req = Request(url='https://www.indeed.com'+link, headers=headers)
#         html = urlopen(req).read()
#         soup = bs.BeautifulSoup(html, 'html.parser')
#         type = soup.find('div', class_='js-match-insights-provider-tvvxwd ecydgvn1').get_text(separator=' ')
#         return type
#     except Exception as e:
#         print(f"Failed to retrieve job type: {e}")
#         return 'No type'    
if __name__ == '__main__':
    results = scrape_jobs()
    if results is not None:
        print(results)
        # Optionnel : Sauvegarder les résultats dans un fichier CSV
        results.to_csv('indeed_jobs.csv', index=False)
    else:
        print("No results to display.")
