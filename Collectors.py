from scraping import Scraping, parser, path


class CrushCollector():
    def __init__(self):

        self.categories = ['danza-teatro', 'musica', 'cinema', 'didattica', 'incontri', 'mostre', 'iniziative-bambini']
        self.classe = 'colonna-1-5007'
        self.path = path

    def collect(self):
        """Creates links to each subcategory containing events"""
        start = "https://www.crushsite.it/{}"

        links = []
        for c in self.categories:
            category_main = start.format(c)
            links.append(category_main)
        return links

    def visit_event_and_write(self):
        """ Visits each subcategory link's event """
        links = self.collect()
        events = []
        for l in links:
            scrape = Scraping(l, parser)
            events = scrape.select_link()
            for e in events:
                print("Scraping {} and writing it to file".format(e))
                title = e.split('/')
                title = title[-1]
                scrape.write_to_csv(title, self.classe, path)
                print("{} Written to {}, mission accomplished!".format(e, title))


class EsnCollector():
    def __init__(self):

        self.classe = ['field-name-body field-type-text-with-summary field-label-hidden',
                       'group-details field-group-div']
        self.path = path
        self.start = "https://trento.esn.it/?q=events"
        self.categories = [l for l in Scraping(self.start, parser).select_link()]
        self.past = []

    def collect(self, iterator):
        """Creates links to each subcategory containing events"""
        events = []
        start = "https://trento.esn.it{}"

        for c in iterator:
            category_main = start.format(c)
            events.append(category_main)
        return events

    def visit_event_and_write(self):
        """ Visits each subcategory link's event """
        events = self.collect(self.categories)

        for e in events:
            if ('page' in e):
                self.past.append(e)

            else:
                try:
                    scrape = Scraping(e, parser)
                    print("Scraping {} and writing it to file".format(e))
                    title = e.split('/')
                    title = title[-1]
                    scrape.write_to_csv(title, self.classe, path)
                    print("{} Written to {}, mission accomplished!".format(e, title))
                except:
                    print('Issue with {} encountered'.format(e))
        self.past_events()

    def past_events(self):
        for p in self.past:
            past_scraping = Scraping(p, parser)
            past_events = past_scraping.select_link()
            past = self.collect(past_events)  # Link intero
            for e in past:
                try:
                    scrape = Scraping(e, parser)
                    print("Scraping {} and writing it to file".format(e))
                    title = e.split('/')
                    title = title[-1]
                    scrape.write_to_csv(title, self.classe, path)
                    print("{} Written to {}, mission accomplished!".format(e, title))
                except:
                    print('Issue with {} encountered'.format(e))
