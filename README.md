# SESC
SESC (search engine for smart contracts) is an extension of my ContractCrawler[https://github.com/fabritrv/ContractCrawler] project that allows you to search thourgh the contracts you previously crawled by inserting a keyword.


**HOW TO USE**:
1. Enter the folder that contains all of the source code of the contracts that you previously got using ContractCrawler
2. Enter 'txt' if you files are saved as .txt or 'sol' if they're .sol
3. Enter a keyword
4. Enter the number of results that you want to be displayed (if there are less contract available than the number you indicated, you will see all of the contracts that satisfy your search)

SESC will the return a list of smart contracts that include your keyword. The first time you search for a keyword it might take a while. After that SESC creates and alphabetical local cache to make your future search faster.


**v2.0**:
This new version introduces the possibility to indicate a number of contracts that the user wants to see. It also includes some changes under the hood: multithreaded search + more detailed outputs


**NOTE**:
Still WIP. If you got your source codes through a different source it should still work, and it should also work with different data types but I haven't tested these options.
