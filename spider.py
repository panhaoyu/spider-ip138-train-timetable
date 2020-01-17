import ruia.exceptions
from database import Province, Station, Train, TimeTable


class ProvinceItem(ruia.Item):
    target_item = ruia.TextField(css_select='body > table:nth-of-type(4) td')
    url = ruia.AttrField(attr='href', css_select='a', default='无')
    name = ruia.TextField(css_select='a', default='无')

    @staticmethod
    async def clean_name(value):
        if value == '无':
            raise ruia.exceptions.IgnoreThisItem
        return value


class StationItem(ruia.Item):
    target_item = ruia.TextField(css_select='table[width="420"] td')
    url = ruia.AttrField(attr='href', css_select='a', default='无')
    name = ruia.TextField(css_select='a', default='无')

    @staticmethod
    async def clean_name(value):
        if value == '无':
            raise ruia.exceptions.IgnoreThisItem
        return value


class TrainItem(ruia.Item):
    target_item = ruia.TextField(css_select='#checilist table tr')
    url = ruia.AttrField(attr='href', css_select='td:nth-of-type(1) a', default='无')
    name = ruia.TextField(css_select='td:nth-of-type(1) a', default='无')

    @staticmethod
    async def clean_name(value):
        if value == '无':
            raise ruia.exceptions.IgnoreThisItem
        return value


class TimetableItem(ruia.Item):
    target_item = ruia.TextField(css_select='#stationInfo table tr[onmouseover]')
    station = ruia.TextField('td:nth-of-type(2)')
    arrive = ruia.TextField('td:nth-of-type(3)')
    leave = ruia.TextField('td:nth-of-type(4)')


class Spider(ruia.Spider):
    start_urls = ['http://qq.ip138.com/train/']
    request_config = {
        'encoding': 'gbk',
    }
    concurrency = 100

    async def parse(self, response):
        async for item in ProvinceItem.get_items(html=response.html):
            item: ProvinceItem
            yield self.process_province_item(item)

    async def process_province_item(self, item: ProvinceItem):
        db_item = Province.create(name=item.name, url=item.url)
        async for response in self.multiple_request([f'http://qq.ip138.com{item.url}'], encoding='gbk'):
            yield self.parse_province(response, province_item=db_item)

    async def parse_province(self, response, province_item: Province):
        async for item in StationItem.get_items(html=response.html):
            item: StationItem
            yield self.process_station_item(item, province_item)

    async def process_station_item(self, station_item: StationItem, province_item: Province):
        Station.create(name=station_item.name, url=station_item.url, province=province_item)
        async for response in self.multiple_request([f'http://qq.ip138.com{station_item.url}'], encoding='gbk'):
            yield self.parse_train(response)

    async def parse_train(self, response):
        async for item in TrainItem.get_items(html=response.html):
            item: TrainItem
            yield self.process_train_item(item)

    async def process_train_item(self, train_item: TrainItem):
        if Train.filter(name=train_item.name):
            return
        train_db_item = Train.create(name=train_item.name, url=train_item.url)
        async for response in self.multiple_request([f'http://qq.ip138.com{train_db_item.url}'], encoding='gbk'):
            yield self.parse_timetable(response, train_db_item)

    async def parse_timetable(self, response, train_db_item: Train):
        async for item in TimetableItem.get_items(html=response.html):
            item: TimetableItem
            yield self.process_timetable_item(item, train_db_item)

    async def process_timetable_item(self, timetable_item: TimetableItem, train_db_item: Train):
        TimeTable.create(train=train_db_item, arrive=timetable_item.arrive, leave=timetable_item.leave,
                         station=timetable_item.station)


if __name__ == '__main__':
    Province.drop_table()
    Province.create_table()
    Station.drop_table()
    Station.create_table()
    Train.drop_table()
    Train.create_table()
    TimeTable.drop_table()
    TimeTable.create_table()
    Spider.start()
