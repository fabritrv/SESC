# SESC
SESC (search engine for smart contracts) is an extension of my ContractCrawler[https://github.com/fabritrv/ContractCrawler] project that allows you to search thourgh the contracts you previously crawled by inserting a keyword.

**HOW TO USE**:
1. Enter the folder that contains all of the source code of the contracts that you previously got using ContractCrawler
2. Enter 'txt' if you files are saved as .txt or 'sol' if they're .sol
3. Enter a keyword

SESC will the return a list of smart contracts that include your keyword. The first time you search for a keyword it might take a while. After that SESC creates and alphabetical local cache to make your future search faster.

**NOTE**:
Still WIP. If you got your source codes through a different source it should still work, and it should also work with different data types but I haven't tested these options.
