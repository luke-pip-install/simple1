# Process here
1. take words from articles and titles from recc.xlsx (soures of security papers)
2. logic select top relevant words (top10) in authors_logic.ipynb
3. take only 'not to many results one' (<1300) as in the barchart. saved in author_word_based folder
4. take papers from paperlist and online(download from link.py) based on relevant words 
5. from collected pdfs, collect emails via email_from_pdf.py
6. select only authors if <= 4 take all and  if > 4 take first 2 and last one. (corresponding authors needed)  
7. saved to author_file

