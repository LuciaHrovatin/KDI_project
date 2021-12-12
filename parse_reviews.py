import os, json, csv
import pprint as pp
dir = r'C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\PARSING\TripAdvisor'
# Review :
# Content
# GlobalEvaluation
# PublishedOn
# ----------------
# Ranking :
# isDistant
# interactionCounter
# itemEvaluated
# CreativeWork: facility
# ratingValue

class ReviewParser() : 

    def __init__(self, dir) : 
        self.dir = dir 

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
    
    def read_parse(self) : 
        """
        Reads the review and parses it into a json file
        """
        lst = []
        for v in os.listdir(self.dir) : 
            item = self.itemizer()
           

            with open(os.path.join(self.dir, v), encoding ='utf-8') as f :
                read = csv.reader(f, delimiter=',') 
               
                for row in read:
                    for el in row:
                        if ('<div class="ui_column is-9">') in el and ('<span class="ui_bubble_rating bubble_' in el):
                            lst = el.split('>')
                            date = lst[3].replace('<span class="ratingDate" title="','').replace('"','')
                            idx1 = lst.index('<span class="noQuotes"') + 1
                            idx2 = lst.index('<div class="prw_rup prw_reviews_stay_date_hsx" data-prwidget-init="" data-prwidget-name="reviews_stay_date_hsx"')
                            content = ' '.join(lst[idx1:idx2]).replace('</p','').replace('</div','').replace('<div','').replace('</span','')
                            item['has_review']['has_content'] = content.replace('</a   class="prw_rup prw_reviews_text_summary_hsx" data-prwidget-init="handlers" data-prwidget-name="reviews_text_summary_hsx"  class="entry" <p class="partial_entry"','').replace('class="entry" <p','') 
                            item['has_review']['has_date'] = date 
                            item['has_itemEvaluated'] = v.replace('.csv','').lower()
                if ('bookique' in v.lower()) : 
                    item['has_review']['has_website'] = 'https://www.tripadvisor.com/Restaurant_Review-g187861-d10304321-Reviews-Bookique-Trento_Province_of_Trento_Trentino_Alto_Adige.html'
                if ('pedavena' in v.lower()) : 
                    item['has_review']['has_website'] = 'https://www.tripadvisor.it/Restaurant_Review-g187861-d1128166-Reviews-Antica_Birreria_Pedavena-Trento_Province_of_Trento_Trentino_Alto_Adige.html'
                if ('mart' in v.lower()) : 
                    item['has_review']['has_website'] = 'https://www.tripadvisor.it/ShowUserReviews-g194889-d2054642-r140669078-Museo_di_Arte_Moderna_e_Contemporanea_di_Trento_e_Rovereto-Rovereto_Province_of_.html'
                if ('buonconsiglio' in v.lower()):
                    item['has_review']['has_website'] = 'https://www.tripadvisor.com/Attraction_Review-g187861-d600982-Reviews-Castello_del_Buonconsiglio_Monumenti_e_Collezioni_Provinciali-Trento_Province_of_T.html'

               
            with open(os.path.join(self.dir,'parsed_reviews.json'), 'a', encoding =' utf-8') as f :
                print('Writing {} to file'.format(item))
                json.dump(item,f)

                            

ReviewParser(r'C:\Users\Anna Fetz\Desktop\Data_Science\third_semester\KDI_2021\PARSING\TripAdvisor').read_parse()