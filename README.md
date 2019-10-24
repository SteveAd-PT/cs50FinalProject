FINAL PROJECT:

My final project is a Flask-App that lets the user search for birds which were "Bird of the Year" in different ways.
The data of the birds is stored in a SQLite3 database (just 12 entries for test purposes).
The navigationbar is made with bootstrap, fully responsive, and includes a searchbox. The searchbox uses autocompletion (using javascript) to search from a list of all the birds.
The navigationbar comes with two links, one for the index-page and one to see all the data (clicking on the picture in the navigationbar also redirects to the index-page).
The form is using two html-selector-tags with which the data can be filtered for the wingspan or the size of the birds or both. If no dataentries match the search it returns a flash-message.
The results of the search are displayed in a table. The rows can be sorted alphabetically by clicking on the name-tablehead.
