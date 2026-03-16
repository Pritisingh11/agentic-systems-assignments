from tables import create_tables
from fetch import fetch_user
from update import update_user
from delete import delete_user
from insert import create_user

#create_user("priti", 28, "gurgaon")
#create_user("rahul", 27, "pune")
#create_user("suman", 29, "delhi")


fetch_user()
update_user("rahul", "mumbai")
fetch_user()
delete_user()
fetch_user()
