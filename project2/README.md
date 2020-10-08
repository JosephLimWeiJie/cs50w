# Network
By: `JosephLimWeiJie` Since: `Aug 2020`

* [1. Introduction](#introduction)
* [2. Quick Start](#quickstart)
* [3. Features](#features)

<a name="introduction"></a>
## Introduction
<img align="center" src="https://user-images.githubusercontent.com/59989652/95488492-33acbd80-09c8-11eb-940a-2e5a001f7461.png">

Commerce is an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

<a name="quickstart"></a>
## Quick Start
+ Ensure that you have `Django` installed. 
+ Download the `src` code.
+ Within the `capstone` folder, you should see a `manage.py` file.
+ Run the command `python manage.py runserver`.
+ Next, open your browser and enter the following url `http://127.0.0.1:8000/`.
+ For best viewing/user experience, browse the website on `Chrome` browser.

<a name="features"></a>
## Features
Here are the following features that are implemented in the Commerce app. A visual demo is provided in the video below.
+ **Models**
  + Commerce app uses `Model` to represent `User`, `Bid` and `Listing`.
+ **Create Listing**
  + Users can create a listing that is ready to be auctioned.
+ **Active Listings Page**
  + Each listing is active until the lister declares the highest winning bidder.
+ **Listing Page**
  + Users can view all open listings available in the database.
+ **Watchlist** 
  + Users can set a listing to be under their watchlist.
+ **Categories**
  + Each listing can be sorted into specific categories.
+ **"Django Admin Interface**
  + A superuser is created to have full admin access to the `Models`.

[![Screenshot 2020-09-22 at 11 23 42 PM](https://user-images.githubusercontent.com/59989652/95488807-92723700-09c8-11eb-93f1-d7f41270892b.png)](https://youtu.be/-ZmFzBEm53Y)



