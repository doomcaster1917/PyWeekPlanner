import random
from datetime import datetime

from PIL import ImageDraw, Image, ImageFont
import math
import datetime
import textwrap
from io import BytesIO
from collections import Counter

class CalendarDrawer:


    def __init__(self, min_hour_and_max_hour: list = None, lang_ru: bool = False,
                 print_all_hours: bool = False):

        # we cant divide exact ru_lang and en_lang conditions out of print_all_dates,
        # because we have custom dynamical-sizes settings
        # on print_all_dates for each lang_condition. So yes, must hardcode here.
        self.print_all_hours = print_all_hours
        self.lang_ru = lang_ru
        self.ru_font = 'fonts/Airfool.otf'
        self.en_font = 'fonts/blueberrydays/Blueberry Days.ttf'
        self.font_size = 60
        if not print_all_hours:
            self.min_hour = 10
            self.max_hour = 20
            self.start_items_x = 548
            self.start_items_y = 400  # 415  #380
            self.x_column_step = 475
            self.y_drawing_hours_start = 328
            self.y_drawing_lines_start = 430
            if lang_ru:
                self.raw_img = 'raw_pictures/ru_lang_picture.png'

                self.font = ImageFont.truetype(self.ru_font, size=int(self.font_size))
                self.daynames = ['Пон ', 'Вторн ', 'Сред ', 'Четв ', 'Пятн ', 'Суб ', 'Воск ']
                self.x_column_start = 395
                self.y_column_start = 263
                self.fontsize_coefficient = 0.504
                self.chars_per_line_coefficient = 0.45
                self.extra_y_limit = 34

                self.changing_y_after_overcome_extra_y_limit = 0
                self.coefficient_when_overcome_extra_y_limit = 1.4

                self.coefficient_when_overcome_three_lines = 1.2
            else:
                self.raw_img = 'raw_pictures/english_lang_picture.png'

                self.font = ImageFont.truetype(self.en_font, size=int(self.font_size))
                self.daynames = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                self.x_column_start = 435
                self.y_column_start = 260
                self.fontsize_coefficient = 0.6#0.7  #
                self.chars_per_line_coefficient = 0.65  #
                self.extra_y_limit = 34

                self.changing_y_after_overcome_extra_y_limit = 12
                self.coefficient_when_overcome_extra_y_limit = 1.55
                self.coefficient_when_overcome_three_lines = 1

        elif print_all_hours:
            self.start_items_x = 548
            self.start_items_y = 415  # 415  #380
            self.min_hour = 0
            self.max_hour = 24
            self.x_column_step = 475
            self.y_drawing_hours_start = 347
            self.y_drawing_lines_start = 430
            if lang_ru:
                self.raw_img = 'raw_pictures/ru_lang_picture.png'

                self.font = ImageFont.truetype(self.ru_font, size=int(self.font_size))
                self.daynames = ['Пон ', 'Вторн ', 'Сред ', 'Четв ', 'Пятн ', 'Суб ', 'Воск ']
                self.x_column_start = 395
                self.y_column_start = 263
                self.fontsize_coefficient = 0.78  # 0.504
                self.chars_per_line_coefficient = 0.35
                self.extra_y_limit = 34  # 40 #If len(text) more self.extral_y_limit
                # script starts decrese y and change y_central cord
                self.changing_y_after_overcome_extra_y_limit = 0
                self.coefficient_when_overcome_extra_y_limit = 1.2  # set between 1.0 and 1.4
                self.coefficient_when_overcome_three_lines = 0.05
            else:
                self.raw_img = 'raw_pictures/english_lang_picture.png'

                self.font = ImageFont.truetype(self.en_font, size=int(self.font_size))
                self.daynames = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                self.x_column_start = 435
                self.y_column_start = 260
                self.fontsize_coefficient = 0.7  #
                self.chars_per_line_coefficient = 0.5  # 0.5 #
                self.extra_y_limit = 34  # 40  #If len(text) more self.extral_y_limit script starts
                # decrese y and change y_central cord
                self.changing_y_after_overcome_extra_y_limit = 0
                self.coefficient_when_overcome_extra_y_limit = 1
                self.coefficient_when_overcome_three_lines = 0.75




        if min_hour_and_max_hour:

            self.min_hour = min_hour_and_max_hour[0]
            self.max_hour = min_hour_and_max_hour[1] + 1

        
        self.coefficient_y = 2040
        self.interval = self.max_hour - self.min_hour
        self.x_step = 475
        self.y_step = self.coefficient_y / self.interval
        self.coefficient_slot_y = 1560
        self.slot_height = self.coefficient_slot_y/self.interval
        self.slot_width = 410
        self.start_font_for_calculations = ImageFont.truetype('fonts/blueberrydays/Blueberry Days.ttf', size=int(65))
        self.day_start = datetime.datetime.strptime('00:00', '%H:%M')
        self.color = (195, 124, 180)
        self.start_font_size_for_items = 65

    def draw_columns(self, week: list, draw: ImageDraw):

        x_column_start_russian = self.x_column_start
        start_week = week[0][0] - datetime.timedelta(days=week[0][0].weekday())

        for count, day_name in enumerate(self.daynames):
            draw.text((x_column_start_russian, self.y_column_start),
                           f'{day_name} {datetime.datetime.strftime(start_week + datetime.timedelta(days=count), "%d.%m")}',
                           font=self.font,
                           stroke_fill='black', stroke_width=5)
            x_column_start_russian += self.x_column_step



    def some_calculations(self, date: datetime):

        filtered_date = datetime.datetime.strptime(datetime.datetime.strftime(date, '%Y-%m-%d %H:00'),
                                                 '%Y-%m-%d %H:00')
        week_start = filtered_date - datetime.timedelta(days=filtered_date.weekday(), hours=filtered_date.hour)

        total = []
        count = 0
        day_number = 0
        for i in range(7 * self.interval):

            if count >= self.interval:
                count = 0
                day_number += 1
            dat = datetime.datetime.strptime(datetime.datetime.strftime(week_start,
                                                                        f'%Y-%m-{week_start.day + day_number} {self.min_hour}:00'),
                                             '%Y-%m-%d %H:00') + datetime.timedelta(hours=count)
            total.append(dat)
            count += 1
        index = total.index(filtered_date)

        return index

    def exception_filter(self, data):
        dates = []
        texts = []
        for i in data:

            if i[0].hour < self.min_hour or i[0].hour > self.max_hour and not self.print_all_hours:
                raise Exception(
                    "The datetime doesnt belong to chosen time interval. If you didnt set min and max times, by default "
                    "min time is 10:00 and max is 20:00. Change min_hour and max_hour to remove error, or you can set print_all_dates"
                    "in arguments of class")

            elif self.min_hour > self.max_hour:
                raise Exception(
                    "Min_hour is more than max_hour. Change min_hour and max_hour to remove error")
            dates.append(datetime.datetime.strftime(i[0], '%Y-%m-%d %H:00'))
            texts.append(i[1])


        unicq_dates = list(set(dates))
        c_dates = Counter(dates)
        c_uniq_dates = Counter(unicq_dates)
        results = c_dates - c_uniq_dates
        indexes = []
        for i in tuple(results):
            indexes.append(dates.index(i))
        if results:
            raise Exception(f"Can't draw items with equal dates. The dates: {[result for result in tuple(results)]} texts: {[texts[index] for index in indexes]}")


    def draw_lines_and_hours(self, draw: ImageDraw):

            y_drawing_hours_start = self.y_drawing_hours_start + (624/self.interval)
            y_drawing_lines_start = self.y_drawing_lines_start + (824/self.interval)
            for i in range(self.interval):

                draw.text((125, y_drawing_hours_start),
                f'{datetime.datetime.strftime(datetime.datetime.strptime(f"{self.min_hour}:00", "%H:%M") + datetime.timedelta(hours=i), "%H:%M")}',
                          font=self.font,
                          stroke_fill='black', stroke_width=5)
                y_drawing_hours_start += self.y_step

                #draw 7(like on each weekday) lines on each hour
                x = 350
                for i in range(7):
                    draw.line(((x, y_drawing_lines_start), (x + 400, y_drawing_lines_start)), fill=self.color, width=3)
                    x += 475
                y_drawing_lines_start += self.y_step

    def draw_items(self, data: list, draw: ImageDraw):

        for item in data:
            text = item[1]
            date = item[0]
            index = self.some_calculations(date)
            column_index = index // self.interval
            row_index = index % self.interval
            x_central  = self.start_items_x + (self.x_step * column_index)
            y_central = self.start_items_y + (self.y_step * row_index)
            slot_area = self.slot_width * self.slot_height
            letter_area = slot_area / len(text)
            dynamic_font_size = self.fontsize_coefficient * math.sqrt(1.6 * letter_area)

            if self.lang_ru:
                font = ImageFont.truetype(self.ru_font, size=int(dynamic_font_size))
            else:
                font = ImageFont.truetype('fonts/blueberrydays/Blueberry Days.ttf', size=int(dynamic_font_size))

            average_font_width = sum([font.getsize(word)[0] for word in text])/len(text)
            chars_per_line = (self.slot_width // average_font_width) / (self.chars_per_line_coefficient*(len(text)/12))

            lines = textwrap.wrap(text, width=round(chars_per_line), break_long_words=False)

            num_lines = len(lines)

            if len(text) > self.extra_y_limit:
                y_central -= self.changing_y_after_overcome_extra_y_limit

                if self.lang_ru:
                    font = ImageFont.truetype(self.ru_font, size=int(dynamic_font_size *
                                                                     self.coefficient_when_overcome_extra_y_limit))  # * 0.6
                else:
                    font = ImageFont.truetype('fonts/blueberrydays/Blueberry Days.ttf',
                                              size=int(dynamic_font_size * self.coefficient_when_overcome_extra_y_limit))

            for line in lines:
                line_height = font.getsize(line)[1]

                if line_height*num_lines >= self.slot_height:
                    lines = textwrap.wrap(text, width=len(text)//2, break_long_words=False)

                    if self.lang_ru:
                        font = ImageFont.truetype(self.ru_font , size=int(dynamic_font_size * 0.6)) # * 0.6
                    else:
                        font = ImageFont.truetype('fonts/blueberrydays/Blueberry Days.ttf',
                                                  size=int(dynamic_font_size * self.coefficient_when_overcome_three_lines))

            random_color = (random.randint(100, 255), random.randint(170, 255), random.randint(80, 255))
            step = 0
            lines_num = len(lines)

            for line in lines:
                 line_width, line_height = font.getsize(line)
                 y_calc = (line_height * lines_num)/2
                 finish_y = y_central - y_calc + y_calc*step
                 finish_x = x_central - (line_width/2)
                 draw.text((finish_x, finish_y), line, font=font, fill=random_color, stroke_fill='black', stroke_width=5)
                 step += 1


            x_central += (self.x_step * column_index)
            y_central += self.y_step * row_index

    def define_weeks(self, data: list):
        dates = [date[0] for date in data]
        week_numbers = set(date.isocalendar().week for date in dates)
        weeks = []
        for number in week_numbers:
            week = []
            for item in data:
                date = item[0]
                if date.isocalendar().week == number:
                    week.append(item)
            weeks.append(week)

        return weeks


    def draw_calendar(self, data: list):
        weeks = self.define_weeks(data)

        for num, week in enumerate(weeks):
            img = Image.open(self.raw_img)
            draw = ImageDraw.Draw(img)
            self.exception_filter(week)
            self.draw_columns(week, draw)
            self.draw_lines_and_hours(draw)
            self.draw_items(week, draw)
            img.save(f'Results/result{num}.png')
            img.close()

    def draw_calendar_bytesio(self,data: list) -> list:

        weeks = self.define_weeks(data)
        pics = []
        for num, week in enumerate(weeks):
            img = Image.open(self.raw_img)
            draw = ImageDraw.Draw(img)
            self.exception_filter(week)
            self.draw_columns(week, draw)
            self.draw_lines_and_hours(draw)
            self.draw_items(week, draw)
            finished_image_content = BytesIO()
            finished_image_content.seek(0)
            img.save(finished_image_content, format='PNG')

            finished_image_content.name = (
                f'/home/root/your/folder/result{num}.png'
            )
            pics.append(finished_image_content)

        return pics

