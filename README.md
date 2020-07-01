# SESC
SESC (search engine for smart contracts) is an extension of my [ContractCrawler](https://github.com/fabritrv/ContractCrawler) project that allows you to search through the contracts you previously crawled.


**HOW TO USE**:
1. Enter the directory that contains all of the source code of the contracts that you previously got using ContractCrawler.
2. Enter 'txt' if you files are saved as .txt or 'sol' if they have .sol extension.
3. Select one of the options available.
4. I suggets you to create the cache and run the parser first.

The available options are:

0. Create graph --> See v.5.x notes.
1. Create cache --> Enter 20 keyword and search them at once to create the cache. This will speed up your next searches.
2. Search by keyword --> Enter a keyword and the number of results you want to see. If you already parsed the contracts you'll be able to get even more details.
3. Search by sentence --> See v.3.x notes.
4. Delete cache.
5. Parse each contract present in the directory you specified when launching SESC.
6. Parse a single contract --> Just enter its address and get its functions and variables.
7. Exit.


I highly reccomed reading the rest of the notes before using this software.
The results for options number 0, 2 and 3 can be displayed in a cooler way, more details below.
'requirements.txt' now available to quickly let users install the needed packages and libraries. Finally trimmed down the list.



**DISPLAY BETTER RESULTS**:

SESC now shows results in a better and more intuitive way. When you run one of the functionalities a JSON will be produced, in particular
1. Graph --> generates a JSON that can create a dendrogram
2. Search by sentence --> generates a JSON that can create a circle packing
3. Search by keyword --> generates a JSON that can create an indented tree
by using and adapting [D3's founder Mike Bostock work](https://observablehq.com/@mbostock). You can find full details on what I edited, links to Mike original work as well as a thank you message to him and a couple other brief details in the localh directory.

To display the results, run then function and wait for the completion as usual, then cd to localh and enter 
```python
python3 -m http.server
```
then open your browser and go to localhost:8000. A small menu will appear, now you just have to select what you want to visualize and that's it. Credits, notes and details as well.

Remember to interrupt the http server when done with the operations. At times browsers tend to cache web pages for longer than expected so if some of the results aren't updating consider clearing you browser's cache.



**v5.x**:
Added graph functionality: select a contract and SESC will create a graph, where different nodes represent different contracts, and different edges represent the percentage of similarity between variables and functions of two contracts.
The minimum number of similarity required to show a relation is 70%.
After the graph is shown, you can see the results listed and sorted by matching percentages, for easier navigation porpuses.
The similarity is determined using edlib.align(), which uses Levenshtein distance between strings. Basically it is the number of char you have to edit in the first string to make it become the second.
I then used the distance to calculate a similarity coefficient, dividing it by the length of the string that contaions functions and variables, that the parser returned eariler. This coefficient was then turned into a number that indicates a percentage of difference between the parser results for two contracts.
As Levenshtein distance represents difference the weight of the edges is (100-similarity coeff.).
The graph is then used to produced the JSON that generates the dendrogram. In this case the max number of results is 200 as otherwise it would look messy.
One last note: to create the graph you must run the parser first!


**v4.x**:
Added the ability to get all the functions and the variables of a contract: you can create a .csv containing all the contracts just by entering a path. After you did just enter the contract name and quickly get what you need. This functionality uses [solidity_parser by ConsenSys](https://github.com/ConsenSys/python-solidity-parser).
If you choose to, functions and variables for the contracts in search results can now be displayed both when searching by keyword and by sentence.
Please note that you will get a result only if your contract has already been parsed using 'Get functions and variables for each contract'. This is also true in the search results.


**v3.x**:
Added search by sentence: it is now possible to enter a sentence and search through contracts. SESC will take 5 keywords from your sentence and show a number of results ordered by relevancy (more keywords found means higher relevancy). After the latest update SESC can search for keywords even if they're not in your cache. All the words that are not in your cache will be searched by scanning your contract directory so it could take a couple minutes, but after the first search every keyword included in your sentence will be added to the cache.
To use search by sentence it is necessary to install nltk and download a few packages. You can go ahead and install the collection "all" or install single packages as you wish. SESC does not automatically do this to avoid installing something you might not want on your machine.


**v2.x**:
This new version introduces the possibility to indicate a number of contracts that the user wants to see. It also includes some changes under the hood: multithreaded search + more detailed outputs.
Added the option to create and delete the cache.


**NOTE**:
If you got your source codes through a different source it should still work as long as the source code of the smart contracts is well written.
For any question, clarification or need (especially if you need contracts source codes etc.) email me and I will hit you back!