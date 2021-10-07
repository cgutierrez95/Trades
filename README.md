# Trade Interface

## Video: https://youtu.be/rzBQLCvlKow

### Description:

#### Context:

Before explaining may project per se, I will explain why I chose this project and a little bit of context.

First of all, me and some friends started trading with cryptocurrency using Binance, after getting used to it,
we decided to get a little further and started learning the basics like: what is blockchain, how does crypto works,
how Bitcoin works, etc. After that we decided to deepen more about this topic and ended learning how to read graphs
and other signals in the cryptocurrency's market.

With that information, we started estimating and trying to predict the criptocurrencies' prices (using fundamental
and technical analysis) to know when to buy and when to sell. With that being said we estimated several predictions
but we started to get lost with so many trades. So I came up with the idea to create a tool that let us to add as 
many trades as we want and have a better tracking of each trade just by having a simple glimpse to the app.

#### Project:

My project is a desktop app, it was created using python (for the logic), kivy (for the GUI) and a SQL (to store and
query the trades). The app is divided in two main parts: the Add Trade and the Active Trades.

##### Add Trade:

This is where the user adds manually and one by one the trades created after the analysis explained before.
For a trade to be added to the database it must fulfill some requirements:
    1. Date: The date when trade was created or loaded (depends on the user). (mandatory)
    2. Symbol: The symbols as known by Binance and from which the trade will take place. (mandatory)
    3. Direction: The direction of a trade, can be long (for buying operations) or short (for selling operations). (mandatory)
    4. Entry Price: The price when reached, will mark the beginning of our trade. (mandatory)
    5. Exit 1: The price when reached, will mark the possible end of a trade. (mandatory) 
    6. Exit 2: The price when reached, will mark the possible end of a trade.
    7. Exit 3: The price when reached, will mark the possible end of a trade.
    8. Exit 4: The price when reached, will mark the possible end of a trade.
    9. Stop Loss: The price when reached, you must end the trade with minimal losses. (mandatory)
    
Regarding the exits, the trades must have at least one exit but can have more than one, this means that you as trader and user 
have the choice to end your trade once the price of exit 'n' has been reached.

Regarding the stop loss, is a security mechanism in case the cryptocurrency behaves in a different way as expected and end the
trade in the most secure way possible.

Each field has a validator to make sure the user writes the correct information when loading a trade, in case some information
is wrong the program will not let the user continue and save the trade in the database.

After all validations are correct, then the app proceeds to save all the trade information in the database for the further
queries.

##### Active Trades:

This is where the user consults the information that has previously typed. In this window the user can see all the information
he typed in the Add Trade window and one more piece of information, "current price". The user in this window has one "update"
button that when clicked the app makes a request to the Binance API to "ask" the price of each symbol of all the trades in screen.
Once Binance has answered and returned the information in a JSON, the information is read and updated where it belongs.

The app has visual aids for the user, once the current price of a trade is near either the entry price or one of the exits,
the cell is highlighted with a color indicating its proximity to each set price.

These calculations are as follows:
    
    percentage = (current price / exit or entry price) * 100 
    
If the percentage is between 90 and 98 the cell is highlighted with a yellow color to alert the user that said event is near.
If the percentage is greater than 98 the cell is highlighted with a green color to alert the user that said event is "happening" right now.

#### Conclusion:

This may be an overly specific application for me and my friends that just like that will help us to resolve the specific issue to have
a neat way on which keep track of our trades, even though the developing of this simple app required a great understanding of python and kivy
and a basic understanding of SQL. All in all, this was a fun project to develop and I know that when implemented it will have to have its upgrades
and fixes. And I am up for the challenge :) This was CS50!



