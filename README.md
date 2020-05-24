# SESC
SESC (search engine for smart contracts) is an extension of my ContractCrawler[https://github.com/fabritrv/ContractCrawler] project that allows you to search thourgh the contracts you previously crawled by inserting a keyword.


**HOW TO USE**:
1. Enter the folder that contains all of the source code of the contracts that you previously got using ContractCrawler
2. Enter 'txt' if you files are saved as .txt or 'sol' if they're .sol
3. Select "search by keyword" or "search by sentence" (see v3.x for further details)
4. Enter the keyword or a sentence, then the number of results that you want to be displayed (if there are less contract available than the number you indicated, you will see all of the contracts that satisfy your search).
5. If you choose to get functions and variables for all the contracts you will then be able to search them by simply entering 'contract_address.sol' where contract_address is the address of the contract of which you want to get functions and variables. You can now also choose to get functions and variables directly in search results.

It is also possible to delete or create the cache. If you want to create the cache you can enter 20 keywords and generate it iterating through the contracts just one time. After that you can repeat the process. The bigger the cache, the faster the execution!
If you search by keyword SESC will the return a list of smart contracts that include it. The first time you search for a keyword it might take a while. After that SESC creates and alphabetical local cache to make your future search faster.
If you search by sentence SESC will take keywords from it and look for matching contracts. See v3.x notes from a few more details.
The option to get a contract's functions and variables is now also available in search results. See v4.x for more details.

'requirements.txt' now available to quickly let users install the needed packages and libraries.


**v4.x**:
Added the ability to get all the functions and the variables of a contract: you can create a .csv containing all the contracts just by entering a path. After you did just enter the contract name and quickly get what you need! This functionality user solidity_parser by ConsenSys [https://github.com/ConsenSys/python-solidity-parser].
If you choose to, functions and variables for the contracts in search results can now be displayed both when searching by keyword and by sentence.
Please note that at the current state you will get a result only if your contract has already been parsed using 'Get functions and variables for each contract'. This is also true in the search results.
In the future this feature could be extended, so stay tuned!


**v3.x**:
Added search by sentence: it is now possible to enter a sentence and search through contracts. SESC will take 5 keywords from your sentence and show a number of results ordered by relevancy (more keywords found means higher relevancy). After the latest update SESC can search for keywords even if they're not in your cache. All the words that are not in your cache will be searched by scanning your contract directory so it could take a couple minutes, but after the first search every keyword included in your sentence will be added to the cache.
To use search by sentence it is necessary to install nltk and download a few packages. You can go ahead and install the collection "all" or install single packages as you wish. SESC does not automatically do this to avoid installing something you might not want on your machine.


**v2.x**:
This new version introduces the possibility to indicate a number of contracts that the user wants to see. It also includes some changes under the hood: multithreaded search + more detailed outputs.
Added the option to create and delete the cache.


**NOTE**:
Still WIP. If you got your source codes through a different source it should still work, and it should also work with different data types but I haven't tested these options.
