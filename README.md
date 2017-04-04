# crawler: XPath driven web visiting robot

Small tool for parsing web pages in batch. Useful to be called from shell scripts.

## Why
Sometimes you want to print all links on page. Sometimes you need to click on many pages just to get tiny bit you're interested in. If you can express the part with XPath, crawler will visit all the pages for you.

## How

crawler can do 3 basic actions

* print result of XPath matching on page
* obtain part maching XPath from page and pass it as an argument to command (replace each occurence of '{}')
* follow to next URL (represented as XPath) - as long as XPath is matching, crawler continues to visit pages

## Usage

$ crawler.py --help
Usage: crawler.py [OPTIONS] [URL]...

Options:
  --version                    Show the version and exit.
  -n, --next TEXT              XPath pointing to URL to follow while it
                               matches
  -p, --print TEXT             XPath pointing to region which should be
                               printed to screen
  -a, --action <TEXT TEXT>...  XPath (first parameter) pointing to region
                               which should be passed to a command (second
                               parameter). Use '{}' to indicate positions,
                               wher it should be replaced.
  -s, --silent                 do not print any output
  --help                       Show this message and exit.

Any of options can be repeated.

## Examples

If you wonder who has name-day today, you can ask seznam.cz:

    $ ./crawler.py -s -p '//a[@class="name-link"]/text()' https://www.seznam.cz
    Ivana

If you would like quickly check headlines of novinky.cz:

    $ ./crawler.py -p '//div[@class="item"]/h3/a/text()' https://www.novinky.cz/stalo-se/
    url (1/1): https://www.novinky.cz/stalo-se/
    Přijdou a vmžiku vybílí celý bankomat. Během jedné noci ukradli přes 20 miliónů
    Spojeným státům vládne idiot, okomentoval Trumpa Islámský stát
    Rusko má podle Pentagonu nové rakety, před nimiž se USA ani Evropa neubrání
    Ústavní činitelé na Hradě: Británie musí plnit závazky k EU až do roku 2020
    Svět je v šoku z chemického útoku v Sýrii. Politici mluví o válečném zločinu
    Senátní verze daňového balíčku neprošla, poslanci podpořili vládní návrh
    Prezident omilostnil muže s rakovinou potrestaného za majektovou trestnou činnost a ozbrojování
    Zeman prohrál, veto zákona o národních parcích poslanci přehlasovali

In following example it walk all 25 pages with episode of anime by walking the 'next episode' link and on each page it will find link from mega.nz and run megadl for each:

    $ ./crawler.py --next '//div[@class="navig-button-after"]/a/@href' \
	    --action '//div[@class="listRow"]/a[contains(@href, "mega.nz")]/@href' \
		         'megadl {}' \
		http://shirai.cz/preklad-zobraz/11987/re-zero-kara-hajimeru-isekai-seikatsu/1/
    Re: Zero Kara Hajimeru Isekai Seikatsu - 01A.mp4: 2% - 4,4 MiB of 152,4 MiB

## License
Published under [GPL 3.0 license](https://opensource.org/licenses/GPL-3.0).


