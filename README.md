# PyWeekPlaner 

Just little and cosy tool that will draw you picture or some pictures which show your events on calendar exactly on needed hours in a week view.
You can choose  10-hours format like this below: 
![result0](https://user-images.githubusercontent.com/113614995/190493531-7b221dba-4c61-4d8f-95da-eaa0dd526200.png)


Or your choice can be 24 hours like this:
![result0](https://user-images.githubusercontent.com/113614995/190488120-292b587a-94bd-49e9-a031-c7f4f750de47.png)

Or you can set custom start-hour and finish-hour.

### Autosize
Package supports dynamical size of words in phrases. So the size depends of length of phrase(description of event) and a phrase splits on lines. But remember: the more length of phrase the less this phrase looks especially it refers to 24-hors mode.

### Localization
The standard font supports only english language. Actually package supports russian language as argument of class CalendarDrawer - lang_ru

### How to use?
```
from PyWeekPlanner import CalendarDrawer
calendar = CalendarDrawer(YOUR SETTINGS OR EMPTY)
calendar.draw_calendar(YOUR DATA)
```
### settings

```
CalendarDrawer(print_all_hours=True, lang_ru=True)
```
Flag lang_ru means you choose russian language, flag print_all_hours means you choose 24-hours mode. As well you can pass the class list of custom hours in format: [start_hour, finish_hour], like this 

```
CalendarDrawer(min_hour_and_max_hour=[9,19])
```

### Passed data's format
Function draw_calendar takes data as format [datetime.datetime, str]. You can see below of in example/example.py.

```
data_set_en = [
        [datetime.datetime.strptime('2022-08-15 11:00:00', '%Y-%m-%d %H:%M:%S'), 'What is love?'],
        [datetime.datetime.strptime('2022-08-16 13:00:00', '%Y-%m-%d %H:%M:%S'), 'Baby dont hurt me']
        }
```

### Format package returns
You can take a pictures in 2 formats: saved in folder 'png' or BytesIO.

Made pictures appears in folder /Results with names 'result{0 and etc...}.png'
