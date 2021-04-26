from crawler import normal_crawl
# from render_crawler import render_crawl
from export_to_excel import write_to_excel
from export_to_excel import append_to_excel


# script will work only if it's run directly
if __name__ == '__main__':
    print('--- collecting data from no render required websites ---')
    results = normal_crawl()
    write_to_excel(results)

    # print('--- collecting data from render required websites ---')
    # results = render_crawl()
    # append_to_excel(results)

    print('--- everything finished ---')