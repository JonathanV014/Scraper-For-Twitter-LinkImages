
# Scrapper-For-Twitter-LinkImages

This project is a link scraper of images posted on Twitter/X made with playwright but configured to receive search equations.

## Authors

- [@JonathanV014](https://github.com/JonathanV014)

## Requirements

To start this project (in a virtual environment) first download the dependencies:

```bash
    pipenv install -r requirements.txt
```

and then:

```bash
    playwright install
```

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`USER` Twitter User

`PASSWORD`  Twitter Password

## Execute Project
Once you have installed the dependencies and configured your .env you can run the project by typing:

```bash
    python runScrapper.py
```

Note: By default, the project has a search equation focused on automobile accidents.

If you want to change the scraper configuration go to `configureScrapper.py` and you can configure it:

The date range in which you want to extract the tweets:

`STARTDATE` `ENDDATE`

How often (in seconds) to move and how much (pixels) to move:

`SCROLLTIME` `DISTANCE`

Directory where you will save the .csv with the URLs of the extracted images and the file name:

`DIRSAVECSV` `NAMECSV`

More Important. The search equation you want the scraper to apply to the Twitter/X search engine:

`SEARCHEQUATION`

