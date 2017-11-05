# sentiment-analysis

情感分析

Based on API of IBM Tone Analyzer and Prepared Data of English songs' lyrics from QQ music
In order to match up songs and input texts

Features:

1.Filter out songs involving non English symbols
    --> too few efficient result, to be fixed in future
    
2.Totally local (data & computation)
    --> not strong enough and costy
    
3.output json style result
    --> completion of matching text analysis result and songs' is underway

Data: 
    ./qqMusic1.xlsx |
    ./FemaleA.xlsx

Code:
    ./process.py        process music lyrics to output reference for further matching   |
    ./processText.py    match songs with text       not finished.
