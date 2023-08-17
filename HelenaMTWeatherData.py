import pandas as pd
import calendar


class WeatherAnalysis():
    '''
    a weather analysis class that takes .csv files of weather data and analyzes the results of the location
    '''

    def __init__(self, params):
        '''
        Constructor
        Loads a csv file using the loadFile method and stores it as a pandas variable
        '''
        self.data = self.loadFile(params)

    def loadFile(self, file_path):
        '''
        loads a csv file and stores its columns STATION    NAME    DATE    ACMH    AWND    PRCP    PSUN    SNOW    SNWD    TAVG    TMAX    TMIN    WDFM    WSFM
        as a pandas dataframe
        '''
        data = pd.read_csv(file_path)
        data['MONTH'] = pd.to_datetime(data['DATE']).dt.month
        data['YEAR'] = pd.to_datetime(data['DATE']).dt.year
        return data

    def precipitation(self):
        '''
        uses the class' csv file PRCP column
        prints the sum of the PRCP column
        prints the PRCP by 5 wettest years using the YEAR column
        prints the PRCP by 5 driest years using the YEAR column
        '''
        print("PRECIPITATION STATISTICS")
        prcp_sum = self.data['PRCP'].sum()
        print("Total precipitation: ", round(prcp_sum,2), "in")
    
        wettest_years = self.data.groupby('YEAR')['PRCP'].sum().nlargest(5)
        print("Top 5 wettest years:")
        for year, prcp in wettest_years.items():
            print(year, prcp)
    
        driest_years = self.data.groupby('YEAR')['PRCP'].sum().nsmallest(5)
        print("Top 5 driest years:")
        for year, prcp in driest_years.items():
            print(year, prcp)


    def temperature(self):
        '''
        uses the dataframe columns TAVG (temperature average) TMIN (temperature min) and TMAX (temperature max)
        prints the coldest months on average (sort by month and take the average TAVG temperature)
        prints the average TMAX and TMIN again sorted by month
        '''
        print("TEMPERATURE STATISTICS")
        avg_temp_by_month = self.data.groupby('MONTH')['TAVG'].mean().sort_values()
        print("Coldest months on average:")
        for month, avg_temp in avg_temp_by_month.items():
            month_name = calendar.month_name[month]
            avg_temp_rounded = round(avg_temp, 2)
            print(f"{month_name}: {avg_temp_rounded}")
    
        avg_tmax_by_month = self.data.groupby('MONTH')['TMAX'].mean().sort_values()
        print("Average TMAX by month:")
        for month, avg_tmax in avg_tmax_by_month.items():
            month_name = calendar.month_name[month]
            avg_tmax_rounded = round(avg_tmax, 2)
            print(f"{month_name}: {avg_tmax_rounded}")
    
        avg_tmin_by_month = self.data.groupby('MONTH')['TMIN'].mean().sort_values()
        print("Average TMIN by month:")
        for month, avg_tmin in avg_tmin_by_month.items():
            month_name = calendar.month_name[month]
            avg_tmin_rounded = round(avg_tmin, 2)
            print(f"{month_name}: {avg_tmin_rounded}")

    def livability(self):
        '''
        prints the average number of sunny days (defined as having a PSUN value over 50) in a year
        prints the average number of days where the high is between 50 and 75 degrees in a year
        takes TMIN and prints the average of the lowest 10% of lows in a year
        takes TMAX and prints the average of the highest 10% of highs in a year
        prints the average WSFM per day (average of the WSFM columns)
        prints the number of windy days (count WSFM column > 5)
        prints the average SNOW column total per year
        '''
        degree_sign = u'\N{DEGREE SIGN}'
        print("----Location Summary----")
        avg_sunny_days = self.data[self.data['PSUN'] > 50].groupby('YEAR').size().mean()
        print("Average number of sunny days per year:", round(avg_sunny_days,1))

        avg_moderate_temp_days = self.data[(self.data['TMAX'] >= 50) & (self.data['TMAX'] <= 75)].groupby('YEAR').size().mean()
        print("Average number of days with moderate high temperature (50-75 degrees) per year:", round(avg_moderate_temp_days,1))

        lowest_10pct_tmin_avg = self.data.groupby('YEAR')['TMIN'].quantile(0.05).mean()
        print("Temperature Rarely Below", round(lowest_10pct_tmin_avg,1),degree_sign, "F")

        highest_10pct_tmax_avg = self.data.groupby('YEAR')['TMAX'].quantile(0.95).mean()
        print("Temperature Rarely Above", round(highest_10pct_tmax_avg,1),degree_sign, "F")

        avg_wsfm_per_day = self.data['WSFM'].mean()
        print("Average Wind Speed:", round(avg_wsfm_per_day,1))

        windy_days_count = self.data[self.data['WSFM'] > 10].groupby('YEAR').size().mean()
        print("Number of windy days (above 10mph):", round(windy_days_count,1))

        avg_snow_per_year = self.data.groupby('YEAR')['SNOW'].sum().mean()
        print("Average Snow per year:", round(avg_snow_per_year,1))
        
        
        
        
if __name__ == '__main__':
    helena = WeatherAnalysis("HelenaMTWeatherData.csv")
    #helena.precipitation()
    helena.livability()

        