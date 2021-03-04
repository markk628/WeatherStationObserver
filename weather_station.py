class Subject:

    def registerObserver(observer):
        pass
    def removeObserver(observer):
        pass
    def notifyObservers():
        pass
    

class Observer:

    def update(self, temp, humidity, pressure):
        pass


class WeatherData(Subject):
    
    def __init__(self):        
        self.observers = []
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0
    
    def registerObserver(self, observer):
        self.observers.append(observer)
        
    def removeObserver(self, observer):
        self.observers.remove(observer)
    
    def notifyObservers(self):
        for ob in self.observers:
            ob.update(self.temperature, self.humidity, self.pressure)
    
    def measurementsChanged(self):
        self.notifyObservers()
    
    def setMeasurements(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.measurementsChanged()
    

class CurrentConditionsDisplay(Observer):
    
    def __init__(self, weatherData):        
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0
        self.weatherData = weatherData
        weatherData.registerObserver(self)

    def update(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.display()
        
    def display(self):
        print("Current conditions: Temp: %s°F  Humidity: %s%% Pressure: %sinHg" % (self.temperature,
                                                                                    self.humidity,
                                                                                    self.pressure))
        

class StatisticsDisplay(Observer):
   
    def __init__(self, weatherData):        
        self.temperatures = []
        self.humidities = []
        self.pressures = []
        self.weatherData = weatherData
        weatherData.registerObserver(self)
    
    def update(self, temperature, humidity, pressure):
        self.temperatures.append(temperature)
        self.humidities.append(humidity)
        self.pressures.append(pressure)
        self.display()
        
    def get_stats(self, units):
        if units == "°F":
            values = self.temperatures
            measurement = "Temp"
        elif units == "%":
            values = self.humidities
            measurement = "Humidity"
        else:
            values = self.pressures
            measurement = "Pressure"
        
        result = (
            f"Min {measurement}: {min(values)}{units}, " + 
            f"Avg {measurement}: {sum(values) / len(values)}{units}, " + 
            f"Max {measurement}: {max(values)}{units}"
        )
        return result

    def display(self):
        if self.temperatures:
            print(self.get_stats("°F"))
        else:
            print("No temperature stats")
        if self.humidities:
            print(self.get_stats("%"))
        else:
            print("No humidity stats")
        if self.pressures:
            print(self.get_stats("inHg"), "\n")
        else:
            print("No pressure stats", "\n")


class ForecastDisplay(Observer):
    
    def __init__(self, weather_data):
        self.weather_data = weather_data 
        weather_data.registerObserver(self)
        
        self.forecast_temp = 0
        self.forecast_humidity = 0
        self.forecast_pressure = 0
        
    def update(self, temperature, humidity, pressure):
        self.forecast_temp = temperature + 0.11 * humidity + 0.2 * pressure
        self.forecast_humidity = humidity - 0.9 * humidity
        self.forecast_pressure = pressure + 0.1 * temperature - 0.21 * pressure
        self.display()

    def display(self):
        print("Forecast conditions: Temp: %s°F  Humidity: %s%% Pressure: %sinHg" % (self.forecast_temp,
                                                                                    self.forecast_humidity,
                                                                                    self.forecast_pressure))
    

class WeatherStation:
    def main(self):
        weather_data = WeatherData()
        current_display = CurrentConditionsDisplay(weather_data)
        forecast_display = ForecastDisplay(weather_data)
        stats_display = StatisticsDisplay(weather_data)
        
        weather_data.setMeasurements(80, 65,30.4)
        weather_data.setMeasurements(82, 70,29.2)
        weather_data.setMeasurements(78, 90,29.2)
        
        weather_data.removeObserver(current_display)
        weather_data.removeObserver(forecast_display)
        weather_data.removeObserver(stats_display)
        weather_data.setMeasurements(120, 100,1000)
    
        

if __name__ == "__main__":
    ya_local_weatherman = WeatherStation()
    ya_local_weatherman.main()