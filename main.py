
from scraping import Scraping, parser, classe_crush, classe_visit, path

""" NOTE: IT HAS ALREADY BEEN RUN FOR CRUSHSITE DO NOT RUN AGAIN """
#DANZA E TEATRO 
#start = "https://www.crushsite.it/it"
#start = "https://www.crushsite.it/it/eventi-suggeriti"
#start =  "https://www.visittrentino.info/en"
start = "https://www.visittrentino.info/it/guida/eventi"
#categories = ['danza-teatro', 'musica', 'cinema','didattica','incontri','mostre','iniziative-bambini']
categories = [1] #Ha un motorre di ricerca particolare che non cambia URL, di conseguenza lo considero come una macro categoria
#classe = classe_crush
classe = classe_visit

for el in categories: 
     

    if __name__ == "__main__":
        scraping_object = Scraping(start, parser)
        link = scraping_object.select_link() 
        if ('crushsite' not in start) : 
            
            link = link[11:]
            link = list(set(link))
            link = [l for l in link if  l != None and 'event' in l]
            start = "https://www.visittrentino.info{}"
        try : 
            for l in link : 
                
                seed_url = start.format(l)
                print("Web scraping of page {} has begun".format(seed_url))
                scrape = Scraping(l, parser)
                title = seed_url.split('/')
                title = title[-1]
                scrape.write_to_csv(title,classe, path)
        except: 
                print('Error in page building encountered. This is the page {}'.format(seed_url))


print('Scraping has ended. No more links to visit')
