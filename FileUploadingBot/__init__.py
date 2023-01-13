import os, time, multiprocessing, logging
from multiprocessing.dummy import Pool as ThreadPool
from file_preparation_funcs import choose_files, get_sitenames
from file_loading_funcs import price_loading, stocks_loading 

def main():
    start = time.time()

    os.system('mode con: cols=130 lines=45')

    filenames =  choose_files()
    site_names, filenames_ostatki = get_sitenames(filenames)
    
    logging.disable(level=logging.CRITICAL)

    #Выбор мультипоточности и запуск
    if len(filenames_ostatki) > 0:
        sites_for_filenames = list(zip(site_names, filenames_ostatki))
        if len(sites_for_filenames) < multiprocessing.cpu_count():
            pool = ThreadPool(len(sites_for_filenames))
        else:
            pool = ThreadPool(multiprocessing.cpu_count())
        pool.starmap(stocks_loading, sites_for_filenames)
        timeend = time.time() - start
        print('Успешно выполнено за:', round(timeend, 2))
    elif len(filenames) > 0:
        if len(filenames) < multiprocessing.cpu_count() // 2:
            pool = ThreadPool(len(filenames))
        else:
            pool = ThreadPool(multiprocessing.cpu_count() // 2)
        pool.map(price_loading, filenames)
        timeend = time.time() - start
        print('Успешно выполнено за:', round(timeend, 2)) 
    time.sleep(15)
    
if __name__ == '__main__': 
    main()