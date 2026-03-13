### INF601 - Advanced Programming in Python
### Benjamin Odell
### Mini Project 3
 
 
# FrogBook
 
This is a basic self-hosted website for you to rank frogs by how cute they are
 
## Getting Started
 
### Dependencies

Install the required python packages using the following command

```angular2html
pip install -r requirements.txt
```

 
### Installing
 

Download the frog images from [here](https://drive.proton.me/urls/YS66YMPTA8#t4xeitK0PU3Y).<br>
Extract the images into a folder called downloaded_frogs.<br> This folder should be in the root project folder: miniproject3BenjaminOdell <br>
The folder downloaded_frogs must contain all the frog images.<br>

Run this command to initilise the database
```
flask --app FrogBook init-db
```
Run this command to seed the database with the frog images
```angular2html
flask --app FrogBook seed-database
```
 
### Executing program
 
To run the app use the command
```angular2html
flask --app FrogBook run
```
The app will be running on [http://127.0.0.1:5000](http://127.0.0.1:5000)
 
## Authors
 
Benjamin Odell - benjamin.m.odell@proton.me

 
## Acknowledgments
 
Inspiration, code snippets, etc.
* [Flask Tutorial](https://flask.palletsprojects.com/en/stable/tutorial/)
* [Image Uploads](https://flask.palletsprojects.com/en/stable/patterns/fileuploads/)
* [Sqlite Blob](https://www.sqlitetutorial.net/sqlite-blob/)
* [Elo Rating](https://www.geeksforgeeks.org/dsa/elo-rating-algorithm/)
* [Deep Seek (Used for the Bootstrap)](https://chat.deepseek.com/share/17zn657qymh2q466yy)
* [Google Image Downloader](https://www.geeksforgeeks.org/python/how-to-download-google-images-using-python/)