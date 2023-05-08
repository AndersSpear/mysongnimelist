from datetime import datetime

def calc_avg_rating(reviews):
    
    avg = 0
    
    for review in reviews:
        avg+=review.rating
        
    avg/=len(review)
    
    return avg

def current_time() -> str:
    print(type(datetime))
    print(type(datetime.now()))
    return str(datetime.now().month)+'/'+str(datetime.now().day)+'/'+str(datetime.now().year)
