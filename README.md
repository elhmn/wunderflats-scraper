# wunderflats-scraper
scraper for wunderflats

## Dependencies
TODO

## How to run

You can run the app using
```
make run
```

OR

```
make install-deps
source ./venv/bin/activate
python -m main
```

It generates a file containing all the flats listed on the website `hanover_all_flats.json`
 and `hanover_flats_available.json` a list of flats available from `availableFrom`. 

## Other commands
You can inspect other commands by running `make`

```
install-deps: setup your dev environment
run: run the message scraper
test: test your code
help: show help
```

## Config

You can configure the scraper by editing the `config.yaml` file.

Sample:
```yaml
#./config.yaml

#city should be written in lower case
city: "berlin"
minPrice: 0
maxPrice: 900
#availableFrom is the time from when the flats should be available
#and can be one of
#Jan <Y>, Feb Y, Mar Y, Apr Y, May Y, Jun Y, Jul Y, Aug Y, Sep Y, Oct, Nov Y, Dev Y
availableFrom: Jul 2022
```
