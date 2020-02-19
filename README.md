# openfoodfact
OpenClassrooms' Project "Utilisez les données publiques de l'OpenFoodFacts"

## Functionality
Here is listed all functionalities of the program.

### Find Substitutes
To find substitutes, run the program and follow these instructions :

> *Find substitutes (1) or go to the favori-list (2) ?*

`$> 1`

> *Choose a category :*
>
> - *Pizzas (1)*
> - *Pizzas (2)*
> - *Pizzas (3)*
> - *Pizzas (4)*
> - *Pizzas (5)*
> - *Pizzas (6)*
> - *Pizzas (7)*
> - *Pizzas (8)*
> - *Pizzas (9)*
> - *Pizzas (10)*
> - *Pizzas (11)*

`$> 3`

> *Choose a food*
>
> - *Pizza (1)*
> - *Pizza (2)*
> - *Pizza (3)*
> - *Pizza (4)*
> - *Pizza (5)*
> - *Pizza (6)*
> - *Pizza (7)*
> - *Pizza (8)*
> - *Pizza (9)*
> - *Pizza (10)*
> - *Pizza (11)*

`$> 5`

> *We found a substitute for 5*
>
> - *Name : ...*
> - *Description : ...*
> - *Brands : ...*
> - *View on OpenFoodFacts : ...*
>
> *Do you want to save this research ?*
> - *No (0)*
> - *Yes (1)*

### Save Substitute

When you are in the substitute's page, the program will propose you to save

> *Do you want to save this research ?*
> - *No (0)*
> - *Yes (1)*

You only have to input **1** if you want to save, **2** if you don't want.
Program exit after this input.

### Refund Substituted Food
To refund a favored substitutes, run the program and follow these instructions :

> *Find substitutes (1) or go to the favored-list (2) ?*

`$> 2`

> *Your favored food*
>
> - *Pizza (1)*
> - *Pizza (2)*
> - *Pizza (3)*
> - *Pizza (4)*
> - *Pizza (5)*

`$> 5`

> *Your substitute for 5*
>
> - *Name : ...*
> - *Description : ...*
> - *Brands : ...*
> - *View on OpenFoodFacts : ...*

The program exit after this

### Manage Input Errors

If you don't input a number, the program will print a message for you :
> *You entered a letter, please enter a number.*

If you enter a invalid number, the program will print a message for you :
> *Please enter a valid number, from 1 to X*

### MySQL Research

The program will research a substitute in a MySQL base. Please enable your
server before to use this app.

When you launch a research, the program will launch a short algorithm to find a
substitute. You can view this algorithm in the source code, file **models.py**
method **search_algorithm**

## Installation

### 1 : Clone the repo

`git clone https://github.com/GoswaTech/openfoodfact.git`

### 2 : Install MySQL

You need to install MySQL and launch the server manually

### 3 : Create Database

When your server is up, you need to create a new database and change the infos
in the settings file (openfoodfacts/settings.py).

### 4 : Fill the database

`cd openfoodfacts`

`pipenv run python -m openfoodfacts fill_database`

## Launch Program

Launch your SQL server and go in the project root to use this command :

`pipenv run python -m openfoodfacts`
