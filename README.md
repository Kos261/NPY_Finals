# Package Alco analysis
Author: Konstanty Kłosiewicz

The alco-analysis tool combines alcohol-concession data, State Fire Service incident records, population counts, and city coordinates to produce interactive density maps and risk counters that quantify the relationship between the number of concessions and fire risk.

All code is packaged as a Python library ( src layout ) and can be installed in editable mode with ```$ pip install -e .``` command while the production version is delivered to the repository via Pull Request.

The CLI accepts file paths as parameters, so no directories are hard-coded; the same core module also powers the companion notebook analysis_report.ipynb.

Profiling is done with the built-in cProfile, and results can be inspected with snakeviz.

Outputs — an HTML map, a correlation table, and a CSV report — are saved to the user-specified output folder.



### Helpful data links to download:

* [Events data](https://dane.gov.pl/pl/dataset/4695/resource/64720/table?page=1&per_page=20&q=&sort=)
* [Concessions data](https://dane.gov.pl/pl/dataset/1191,informacja-o-przedsiebiorcach-posiadajacych-zezwolenia-na-handel-hurtowy-napojami-alkoholowymi-1/resource/64402/table?page=1&per_page=20&q=&sort=)
* [Polish towns geographic location](https://astronomia.zagan.pl/art/wspolrzedne.html)

* [Population](https://stat.gov.pl/obszary-tematyczne/ludnosc/ludnosc/rezydenci-ludnosc-rezydujaca,19,1.html)

* [Or you can download ready to go 'data' folder](https://drive.google.com/drive/folders/1YpepJwagoZTy9JdwIZYNYpXifwrZj_aP?usp=drive_link)

### TODO
- pip package
- install as pull request

# How to run script in different modes (examples):
RUN
```
        $ python run_analysis.py    \
        -f1 data/concession.csv     \
        -f2 data/events.csv         \
        -f3 data/cities.csv         \
        -f4 data/rezydenci_2023.xlsx\
        -o output/
```
CPROFILE
```
        $ python -m cProfile        \
        -o output/temp.dat          \
        run_analysis.py             \
        -f1 data/concession.csv     \
        -f2 data/events.csv         \
        -f3 data/cities.csv         \
        -f4 data/rezydenci_2023.xlsx\
        -o output/

    SHOW PROFILE snakeviz output/temp.dat
```