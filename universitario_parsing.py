import os, json, csv 

class universitario() :
    def __init__(self) :
        self.dir = r'C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\PARSING\Universitario'
    def itemizer(self) :
        d = {
        'has_interactionCounter':0,
        'has_itemEvaluated':'',
        'has_review':{
            'has_publisher':'',
            'has_content':'',
            'has_website':'',
            'has_date': '',
            'has_globalEvaluation':''},
        'has_publishedOn': 'TripAdvisor',
        'has_ratingValue':0}
        return d
    def create(self) :
        """Inserts comments within content""" 

        for f in os.listdir(self.dir) :
            item = self.itemizer()
            item['has_publishedOn'] = "L'Universitario"

            with open(f, encoding ='utf-8') as file :
                reader = csv.reader(file)

                i = 0
                for row in reader:
                    if (i == 0) :
                        item['has_itemEvaluated'] = row[0]
                    

                    if (i == 1) :
                    
                        item['has_review']['has_date'] = row[0] + row[-1][:5]
                        item['has_review']['has_publisher'] = row[-1][7:]

                    if (len(row)) > 0 :
                        item['has_review']['has_content'] += ' '+ ' '.join(row)
                    i += 1
                    
            with open(os.path.join(self.dir, 'universitario.json'), 'w') as writer :
                print('Writing {} to file'.format(f)) 
                json.dump(item, writer)


universitario().create()