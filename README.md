
<!--Introduction-->
<h2>Fintracker</h2>

<!-- 1. What is it used for? -->
<p>This application is used to track your stock, crypto, and option trading online. It will aid in giving you a broader view of all of your trades. For example you could be doing bad one day and you forget that you've been doing well in the previous week. This application is meant to journal your trades so that you can reflect on what worked and what didn't.</p>

<p><b>Note:</b> There are some features that haven't been implemented yet like the offline mode and the news button. These
    will be implemented in the future as of writing this (12/15/2021)</p>

<!--Requirements-->
<h2>Requirements</h2>
<p><b>Note:</b> I've also made a distributable located in the dist folder <a
        href="https://github.com/gnikkoch96/Fintracker-GUI/tree/main/dist">here</a>. You can clone this repo and
    just launch the app directly through the .exe file</p>
<ul>
    <li>Python 3.8+ (Haven't tested on earlier vers.)</li>
    <li> <a href="https://github.com/hoffstadt/DearPyGui">Dearpygui Module (v1.1) </a> </li>
    <li><a href="https://github.com/ranaroussi/yfinance">yfinance Module</a></li>
    <li><a href="https://github.com/man-c/pycoingecko">pycoingecko Module</a></li>
    <li><a href="https://github.com/nhorvath/Pyrebase4"> pyrebase4 Module</a></li>
</ul>

<!--Demonstration -->
<h2>Demonstration</h2>

<!-- Login -->
<h3>Logging In</h3>
<div>
    <img src="https://github.com/gnikkoch96/Fintracker-GUI/blob/main/resources/read_me%20stuff/login_demo.gif"
        alt="logging in"">
</div>

<!--Register -->
<h3>Register</h3>
<p>Feel free to enter a fake email and password as there is no validation implemented</p>
<div>
    <img src="https://github.com/gnikkoch96/Fintracker-GUI/blob/main/resources/read_me%20stuff/register_demo.gif"
        alt="register"">
</div>

<!--Adding Trade -->
<h3>Adding a Trade </h3>
<div>
    <img src="https://github.com/gnikkoch96/Fintracker-GUI/blob/main/resources/read_me%20stuff/add_trade_demo.gif"
        alt="add trade"">
</div>

<!--Adding Crypto -->
<h4>Adding Crypto Trade</h4>
<p>It is possible to look for more information about the cryptocurrency by clicking on the ticker info button.</p>
<div>
    <img src="https://github.com/gnikkoch96/Fintracker-GUI/blob/main/resources/read_me%20stuff/add_crypto_demo.gif"
        alt="add crypto trade"">
</div>

<!--Adding Stock-->
<h4>Adding Stock Trade</h4>
<p>It is possible to look for more information about the stock by clicking on the ticker info button.</p>
<div>
    <img src="https://github.com/gnikkoch96/Fintracker-GUI/blob/main/resources/read_me%20stuff/add_stock_demo.gif"
        alt="add stock trade"">
</div>

<!--Adding Options -->
<h4>Adding Option Trade</h4>
<p>Currently I have made it only possible to just add naked calls and puts.</p>
<div>
    <img src="https://github.com/gnikkoch96/Fintracker-GUI/blob/main/resources/read_me%20stuff/add_option_demo.gif"
        alt="add option trade"">
</div>

<!--View Trade -->
<h3>View Trades</h3>
<p>You will be able to view all the information of your trade along with other information not able to be shown on the table like the reason portion</p>
<div>
    <img src="https://github.com/gnikkoch96/Fintracker-GUI/blob/main/resources/read_me%20stuff/view_trade_demo.gif"
        alt="view trade"">
</div>

<!--Edit Trade -->
<h3>Edit Trades</h3>
<div>
    <img src="https://github.com/gnikkoch96/Fintracker-GUI/blob/main/resources/read_me%20stuff/edit_trade_demo.gif"
        alt="edit open trade"">
</div>

<p>Editing the sold price from the closed trade table will recalculate the net profit and the profit percentage for that trade</p>

<div>
    <img src="https://github.com/gnikkoch96/Fintracker-GUI/blob/main/resources/read_me%20stuff/edit_closed_trade.gif"
        alt="edit closed trade"">
</div>

<!--Sell Trade -->
<h3>Sell Trades</h3>
<p>Selling a trade affects the count value, so if you sell a partial amount of your trades, your open trade will still exists</p>
<p>Also any trades that enter the closed trade table will affect the total profit and win-rate values located at the top part of the app.</p>
<div>
    <img src="https://github.com/gnikkoch96/Fintracker-GUI/blob/main/resources/read_me%20stuff/sell_trade_demo_one.gif"
        alt="sell trade one">
</div>

<p>Selling all your holdings of a stock/crypto/option deletes the trade from the open table</p>
<div>
    <img src="https://github.com/gnikkoch96/Fintracker-GUI/blob/main/resources/read_me%20stuff/sell_trade_demo_two.gif"
        alt="sell trade two">
</div>

<!--Remove Trade -->
<h3>Removing Trades</h3>
<p>Removing a closed trade will affect the total profit and win-rate which will get adjusted after doing so.
    Removing an open trade does not affect anything</p>

<div>
    <img src="https://github.com/gnikkoch96/Fintracker-GUI/blob/main/resources/read_me%20stuff/remove_trade_demo.gif"
        alt="removing trade">
</div>

<!--Credit-->
<h2>Credit</h2>
<ul>
    <li> <a href=" https://www.canva.com/">Canva (Used to Create Logo)</a></li>
</ul>

