from datetime import datetime

def calc_avg_rating(reviews):
    
    avg = 0
    
    for review in reviews:
        avg+=review.rating
        
    avg/=len(review)
    
    return avg

def current_time() -> str:
    return datetime.now().getMonth()+'/'+datetime.now().getDay()+'/'+datetime.now().getYear()
