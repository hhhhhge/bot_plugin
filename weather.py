import httpx
import datetime

class HeFengWeather:
    def __init__(self):
        self.key = "6d9c541eb3714a3d94ad6876fa79e82a"
        self.location = "101020600"
        self.client = httpx.Client()

    def convert_time(time_str):
        dt = datetime.datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")
        if dt.year != datetime.datetime.now().year:
            return dt.strftime("%Y年%m月%d日 %H:%M时")
        else:
            return dt.strftime("%m月%d日 %H:%M时")

    def geoapi(self, location, adm=None):
        data = self.client.get(f"https://geoapi.qweather.com/v2/city/lookup?key={self.key}&location={location}&adm={adm}").json()
        return data["location"][0]["id"]

    def weather(self, day, location=None):
        if location == None:
            location = self.location
        data = self.client.get(f"https://api.qweather.com/v7/weather/7d?key={self.key}&location={location}").json()
        
        fxDate = data["daily"][day-1]["fxDate"]
        sunrise = data["daily"][day-1]["sunrise"]
        sunset = data["daily"][day-1]["sunset"]
        moonrise = data["daily"][day-1]["moonrise"]
        moonset = data["daily"][day-1]["moonset"]
        moonPhase = data["daily"][day-1]["moonPhase"]
        tempMax = data["daily"][day-1]["tempMax"]
        tempMin = data["daily"][day-1]["tempMin"]
        textDay = data["daily"][day-1]["textDay"]
        textNight = data["daily"][day-1]["textNight"]
        windDirDay = data["daily"][day-1]["windDirDay"]
        windScaleDay = data["daily"][day-1]["windScaleDay"]
        windDirNight = data["daily"][day-1]["windDirNight"]
        windScaleNight = data["daily"][day-1]["windScaleNight"]
        humidity = data["daily"][day-1]["humidity"]
        precip = data["daily"][day-1]["precip"]
        pressure = data["daily"][day-1]["pressure"]
        vis = data["daily"][day-1]["vis"]
        cloud = data["daily"][day-1]["cloud"]
        uvIndex = data["daily"][day-1]["uvIndex"]

        res = f'''{fxDate} 天气预报
天气  {textDay} -> {textNight}
最高温度  {tempMax}℃ 最低温度 {tempMin}℃

日间  {windDirDay}{windScaleDay}级
夜间  {windDirNight}{windScaleNight}级

预计降水量  {precip}mm
相对湿度  {humidity}
大气压强  {pressure}hPa
紫外线强度等级  {uvIndex}级
能见度  {vis}km
云量  {cloud}

日升日落  {sunrise} -> {sunset}
月升月落  {moonrise} -> {moonset}
月相  {moonPhase}
        '''

        return res

    def warning(self, location=None):
        if location == None:
            location = self.location
        data = self.client.get(f"https://devapi.qweather.com/v7/warning/now?location={location}&key={self.key}").json()

        if data["warning"] != None:
            sender = data["warning"]["sender"]
            pubTime = data["warning"]["pubTime"]
            title = data["warning"]["title"]
            startTime = data["warning"]["startTime"]
            endTime = data["warning"]["endTime"]
            status = data["warning"]["status"]
            severityColor = data["warning"]["severityColor"]
            typeName = data["warning"]["typeName"]
            text = data["warning"]["text"]

            pubtime = self.convert_time(pubTime)
            starttime = self.convert_time(startTime)
            endtime = self.convert_time(endTime)

            colour_dict = {
                "Blue": "蓝色",
                "Yellow": "黄色",
                "Orange": "橙色",
                "Red": "红色"
            }
            for i, j in colour_dict.items():
                severityColor = severityColor.replace(i, j)

            res = f'''天气灾害预警
{typeName}{severityColor}预警

{sender}
{pubTime}
{title}
{text}

预警状态
持续时间  {startTime} -> {endTime}
            '''

            return res

    def airaqi(self, day, location=None):
        if location is None:
            location = self.location
        data