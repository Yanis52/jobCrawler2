
import re
import bs4 as bs
from urllib.request import urlopen, Request
import pandas as pd

def scrape_jobs():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.google.com/',
        'DNT': '1'  # Do Not Track Request Header
    }

    # URL de la page Indeed à scraper
    source = 'https://www.indeed.com/jobs?q=data+scientist&l=Austin%2C+TX'
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
    
    # Récupérer tous les titres et les liens des offres d'emploi
    for tag in soup.findAll('h2', {'class': 'jobTitle'}):
        a_tag = tag.find('a')
        if a_tag:
            job_title = a_tag.get_text()
            job_link = a_tag.get('href')
            job_titles.append(job_title)
            job_links.append(f"https://www.indeed.com{job_link}")

    # Créer un DataFrame à partir des données extraites
    results = pd.DataFrame({'Job Titles': job_titles, 'Job Links': job_links})
    return results

if __name__ == '__main__':
    results = scrape_jobs()
    if results is not None:
        print(results)
        # Optionnel : Sauvegarder les résultats dans un fichier CSV
        results.to_csv('indeed_jobs.csv', index=False)
    else:
        print("No results to display.")
