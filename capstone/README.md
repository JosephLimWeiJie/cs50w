# Shopping
By: `JosephLimWeiJie` Since: `Sep 2020`

* [1. Introduction](#introduction)
* [2. Quick Start](#quickstart)
* [3. Features](#features)
* [4. Files Description](#filesdescription)
* [5. Project Justification](#justification)

<a name="introduction"></a>
## Introduction
<img align="center" src="https://user-images.githubusercontent.com/59989652/93908297-0823a500-fd31-11ea-860b-ad5a373d3304.png">

Shopping is an Ecommerce website developed using `Django`, `Python`, `JQuery` and `Javascript`, where users can buy or sell products on a common space. Users can sell products by setting up a shop. Each product will be listed on the main page where anyone can browse or make purchases.

<a name="quickstart"></a>
## Quick Start
+ Ensure that you have `Django` installed. (Note: This app requires Python `Pillow` to display the images properly.)
+ Download the `src` code.
+ Within the `capstone` folder, you should see a `manage.py` file.
+ Run the command `python manage.py runserver`.
+ Next, open your browser and enter the following url `http://127.0.0.1:8000/shopping/`.
+ For best viewing/user experience, browse the website on `Chrome` browser.

<a name="features"></a>
## Features
Here are the following features that are implemented in the shopping app. A visual demo is provided in the video below.

[![Screenshot 2020-09-22 at 11 23 42 PM](https://user-images.githubusercontent.com/59989652/93902942-b415c200-fd2a-11ea-9383-2d3f8e5fd56e.png)](https://www.youtube.com/watch?v=36ygc_wrATI&ab_channel=JosephLim)

### Features Implemented
 + **User**
    + Login
    + Logout
    + Sign Up
+ **Profile**
    + Edit user's own profile
    + Edit user's own profile picture
    + View all purchases made by user
        + Return a product after making a purchase
+ **Set up a shop**
    + View all listings made by the user
    + Update an order's status
    + View all reviews left for each listing made by the user
    + Update any order status under 'item sold' tab
+ **Listing**
    + Edit listing
    + Add the current listing into the user's cart
    + Checkout the current listing directly
    + Edit user's own review for the particular listing
    + Contains a rating score represented by the number of rating stars
+ **Notification**
    + View all pending requests (notifications that require a course of action, such as accepting a return order request)
    + View all notifications
+ **Track Order**
    + Cancel a currently tracked order
    + Receive a currently tracked order
+ **Cart**
    + Remove an item from cart
    + Increase/Decrease the item quantity
    + Checkout all the items in the current cart
+ **Review**
    + Add/Edit review for a listing
    + Notifies the listing's poster whenever an add/edit operation is done
    + Leaves a rating score for each listing
+ **Search**
    + Filter by listing's category
    + Sort by listing's popularity, price or by most recent
+ **Main Page**
    +  Categorize each listing into trending searches, top products, all products and its respective category
+ **Paginator**
    + Paginator is added for each page, where applicable
+ **Django Superuser**
    + Adminstrative superuser rights to override any data in all Models
+ **Mobile Responsiveness**
    + This app is designed to be mobile responsive when displayed in a browser

<a name="filesdescription"></a>
## Files Description
The `shopping` folder contains all necessary files/folders to run the app.

In this folder, there are:
+ `admin.py` - contains administrative permissions to access the various Models from `models.py`.
+ `apps.py` - contains the configured name for this app.
+ `forms.py` - contains `SignUpForm` (for creating new users) and `NewListingForm` (for creating new listings).
+ `models.py`- contains the following:
    + `User` - represents each user in the app.
    + `Profile` - extension of `User` model by storing more user information (e.g phone number, date of birth etc).
    + `Listing` - represents each listing in the app
    + `ListingImage` - extension of `Listing` model to store the listing's image url for easier reference.
    + `Order` - represents each order request made by the buyer to the seller.
    + `Review` - represents each review made by each user in the app/
    + `Notification` - represents each notification to be sent whenever an `Order` or `Review` is being made/cancelled/reviewed/updated/edited.
+ `urls.py` - contains all urls used by shopping app.
+ `views.py` - contains all functions necessary to interact with the Django's template.
+ `migrations` - contains all database information
+ `static/images` - stores all images (user's profile picture and listing's pictures) used by shopping app.
+ `static/shopping/` - contains several folders for each feature implemented.
+ `static/shopping/x` - contains a CSS and Javascript file necessary for that feature's template.
+ `static/styles.css` - basic CSS applied to `layout.html`.
+ `templates/shopping/` - contains all templates needed for the app.

<a name="justification"></a>
## Project Justification
The `Shopping` app contains various features for it to function as an actual Ecommerce website. As such, several features, as listed under `Features`
are implemented. Some of these features are more complicated than the others. For instance, the button to increase/decrease quantity in `listing` and `cart`
was done using Javascript. To allow ease of selecting date when creating a new profile, a calender date picker was also added.

The most notable feature implemented is the **Notification** feature. This feature overlaps all other features and serves as a primary core of the app. Whenever a user (buyer or seller) performs an action, a notification is sent to both parties. Other noteworthy features include leaving a rating score for each listing, which are then represented using the number rating stars. To enable this rating feature to work, some additional Javascript functions has to be written. Additionally, the trending searches feature in the `Main Page` tracks the click-rate of each listing asynchronously to replicate a top listing searches functionality.

Finally, all the features tie together to give a pleasant user experience. `Shopping` is designed to look clean and modern with its mobile responsive design, with various CSS for each template pages, combined with Boostrap's image carousel, modals, navigations bars and its grid system.
