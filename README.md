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
 

Download the frog images from [here](https://drive.google.com/drive/folders/1JWgFTMmFs9X4cwBKa0DIlRWsXCjhCvyY?usp=sharing).<br>
Extract the images into a folder called downloaded_frogs.<br> This folder should be in the root project folder: miniproject3BenjaminOdell <br>
The folder downloaded_frogs must contain all the frog images.<br>

There is also a frog_scrapper.py file that I used to get the frog images. You can run it if my link doesn't work.

Run this command to initialize the database.
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

## Tips

### Admin acocount
There is an admin account:<br>
username: ADMIN<br>
password: root<br>

This is the account with all the frogs in it.

### Frog Battles

A user may not battle their own frogs. 



 
## Authors
 
Benjamin Odell - benjamin.m.odell@proton.me

 
## Acknowledgments
 
Inspiration, code snippets, etc.
* [Flask Tutorial](https://flask.palletsprojects.com/en/stable/tutorial/)
* [Image Uploads](https://flask.palletsprojects.com/en/stable/patterns/fileuploads/)
* [Sqlite Blob](https://www.sqlitetutorial.net/sqlite-blob/)
* [Elo Rating](https://www.geeksforgeeks.org/dsa/elo-rating-algorithm/)
* [Deep Seek Chat (Used for the Bootstrap)](https://chat.deepseek.com/share/xiy2usts4yok1httx0)
* [Google Image Downloader](https://www.geeksforgeeks.org/python/how-to-download-google-images-using-python/)
* [Frog Images](https://enjoythewild.com/types-of-frogs/)