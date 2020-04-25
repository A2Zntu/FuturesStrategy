# FuturesStrategy

Member
--------------
I-Fan Chiang

Data
-------------- 
* TX: The Nearby month Taiwan Futures
* MTXOpenInterest: The daily Open Interest of MTX
* ForOpenOI: The Option Open Interest of foreign institution investors (Call and Put)
* SumOpenOI: The Option Open Interest of 3 big Institutional investors (Call and Put)



Strategy Development 
-------------- 
* Strategy1: Buy and Hold  

* Strategy2: Based on dailyOIchange
   * Buy @ OpenPrice_T+1 and offset at the @ closePrice_T+1 if 
       * the dailyOIchange is positive;  
   * Sell @ OpenPrice_T+1 and offset at the @ closePrice_T+1 if 
       * the dailyOIchange is negative

* Strategy3: Based on ForOIchange
   * Buy @ OpenPrice_T+1 and offset at the @ closePrice_T+1 if 
       * the Foreign Investor's Call OIchange is positive
       * the Foreign Investor's Put OIchange is negative
   * Sell @ OpenPrice_T+1 and offset at the @ closePrice_T+1 if 
       * the Foreign Investor's Call OIchange is negative
       * the Foreign Investor's Put OIchange is positive
   * Else, do nothing

* Strategy4: 
    Combine strategy2 and strategy3
    * Buy @ OpenPrice_T+1 and offset at the @ closePrice_T+1 if 
        * Strategy2 says buy and Strategy3 says buy
    * Sell @ OpenPrice_T+1 and offset at the @ closePrice_T+1 if 
        * Strategy2 says sell and Strategy3 says sell  


Performance
-------------- 
* Strategy1: 
 ![alt text](https://github.com/A2Zntu/FuturesStrategy/blob/master/Graph/BuyandHold.png "BuyandHold")
  * HPR: 0.0531
  * APR: 0.0179
  * Sharp Ratio: 0.0434
  * mdd: -0.314
 
* Strategy2: 
 ![alt text](https://github.com/A2Zntu/FuturesStrategy/blob/master/Graph/Strategy2.png "Strategy2")
  * HPR: 0.2135
  * APR: 0.0686
  * Sharp Ratio: 0.5171
  * mdd: -0.164

* Strategy3: 
 ![alt text](https://github.com/A2Zntu/FuturesStrategy/blob/master/Graph/Strategy3.png "Strategy3")
  * HPR: 0.0396
  * APR: 0.0134
  * Sharp Ratio: 0.033
  * mdd: -0.1384

* Strategy4: 
 ![alt text](https://github.com/A2Zntu/FuturesStrategy/blob/master/Graph/Strategy4.png "Strategy4")
  * HPR: 0.1710
  * APR: 0.0556
  * Sharp Ratio: 0.6735
  * mdd: -0.0869

Conclusion
-------------- 
* From Sharp Ratio: We could see that the Strategy4 has the highest Sharp Ratio



Improvement
-------------- 
* Could consider about the transaction fee and taxes
* Could use ANN or other machine learning skills to improve
