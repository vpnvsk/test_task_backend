# test_task_backend
# Data Parser CLI DOCS


## How to use

### Installation

1. Clone the repository
2. Install requirements to the virtual enviroment`pip install requirements.txt` 
3. `python script.py [comand] --login [login] --password [password]` in the directory whith files you want to parse(if you want to parse data that are not in root dir of project - specify path to script.py)

## Usage
### 1. Create Database
`python script.py create-database`
this command parse all the data from files, create sqlite database, and save all data into it.
use it as a first command
### 2. Admin action
Access for this group of commands have only users with admin role. `Invalid credentials` for bad credentials, `Access denied` for user without admin permitions.
#### 1. Print The Number of All Valid Accounts
`python script.py print-all-accounts --login [login] --password [password]` Prints number of users.
#### 2. Print The Longest Existing Account
`python script.py print-oldest-account --login [login] --password [password]` Prints information about oldest account.
#### 3. Group Children by Age
`python script.py group-by-age --login [login] --password [password]` Prints count of children of each age.
### 3. User action
Access for users and admins. `Invalid credentials` for bad credentials.
#### 1. Print Children
`python script.py print-children --login [login] --password [password]` Prints information about all user children.
#### 2. Find Users with Children of Same Age
`python script.py find-similar-children-by-age --login [login] --password [password]` Prints information about another and their children whose kids are the same age. 

## Quick overview
Application architecture was build with using of dependecy injection. There are handler and database objects. This provide the ability to change components of the app easily.
I have not used ORM because decided that it is unnecesary in such small project, and raw SQL gives more flexibility. Password in database are hashed, because it is unsave to store them in raw form. 
