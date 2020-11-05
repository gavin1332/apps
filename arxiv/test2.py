import arxivchecker
papers = arxivchecker.scrape_arxiv('cs',year=2016,month=6)
arxivchecker.save_many(papers, 'haha.txt')

