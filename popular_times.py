import populartimes as popular
import pandas as pd
import googlemaps

# import the location data set

df = pd.read_csv('location.csv')
df.head() # check the results

df['LAT'] = None
df['LON'] = None
df['PLACEID'] = None

gmaps_key = googlemaps.Client(key = 'AIzaSyAw2TK6g2AvrxiFPV7ObAepk6FUPA837xY')

# Get the Lat, Lon and place_id
for i in range(0, len(df), 1):
    geocode_result = gmaps_key.geocode(df.iat[i,0])
    try:
        lat = geocode_result[0]['geometry']['location']['lat']
        lon = geocode_result[0]['geometry']['location']['lng']
        placeid = geocode_result[0]['place_id']
        df.iloc[i, df.columns.get_loc("LAT")] = lat
        df.iloc[i, df.columns.get_loc("LON")] = lon
        df.iloc[i, df.columns.get_loc("PLACEID")] = placeid
        
    except:
        lat = None
        lon = None


df_mon = df.copy()

for i in range(0,24,1):
    hr = str(i).zfill(2) + '00'
    df_mon[hr] = 0

df_tue = df_mon.copy()
df_wed = df_mon.copy()
df_thu = df_mon.copy()
df_fri = df_mon.copy()
df_sat = df_mon.copy()
df_sun = df_mon.copy()

for i in range(0,len(df),1):
    locname = df.iloc[i, df.columns.get_loc("Location Name")]
    placeid = df.iloc[i, df.columns.get_loc("PLACEID")]
    pop = popular.get_id("AIzaSyAw2TK6g2AvrxiFPV7ObAepk6FUPA837xY", placeid)
    for j in range(0,7,1):
        try:
            lst = pop['populartimes'][j]
            dow = lst['name']
            for k in range(0,24,1):
                hr = str(k).zfill(2) + '00'
                val = lst['data'][k]
                if (dow == 'Monday'):
                    df_mon.iloc[i, df_mon.columns.get_loc(hr)] = val
                elif (dow == 'Tuesday'):
                    df_tue.iloc[i, df_tue.columns.get_loc(hr)] = val
                elif (dow == 'Wednesday'):
                    df_wed.iloc[i, df_wed.columns.get_loc(hr)] = val
                elif (dow == 'Thursday'):
                    df_thu.iloc[i, df_thu.columns.get_loc(hr)] = val
                elif (dow == 'Friday'):
                    df_fri.iloc[i, df_fri.columns.get_loc(hr)] = val
                elif (dow == 'Saturday'):
                    df_sat.iloc[i, df_sat.columns.get_loc(hr)] = val
                else:
                    df_sun.iloc[i, df_sun.columns.get_loc(hr)] = val
        except:
            print ('except \n')
            print (pop)

# write output
df_mon.to_csv('mon.csv')
df_tue.to_csv('tue.csv')
df_wed.to_csv('wed.csv')
df_thu.to_csv('thu.csv')
df_fri.to_csv('fri.csv')
df_sat.to_csv('sat.csv')
df_sun.to_csv('sun.csv')