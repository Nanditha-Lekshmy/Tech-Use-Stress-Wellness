import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
from math import sqrt

# Processes the input file and returns the dataframe
def input_file_parse(input_file_name):
  df = pd.read_csv(input_file_name)
# Drops any null rows
  df = df.dropna(how='any',axis=0)
  return df

# Calculates the correlation
def correlation_screen_time_vs_sleep_duration(df):
  sum_of_screen_time = 0
  sum_of_sleep_duration = 0
  diff_of_screen_time = 0
  diff_of_sleep_duration = 0
  numerator_sum = 0
  diff_of_screen_time_squared = 0
  diff_of_sleep_time_squared = 0

# Iterates through the daily_screen_time_hours column and calculates the mean
  for value in df['daily_screen_time_hours']:
    sum_of_screen_time += value
  mean_of_screen_time = sum_of_screen_time / len(df['daily_screen_time_hours'])

# Iterates through the sleep_duration_hours column and calculates the mean
  for value in df['sleep_duration_hours']:
    sum_of_sleep_duration += value
  mean_of_sleep_duration = sum_of_sleep_duration / len(df['sleep_duration_hours'])

# Iterates through the two dataframes simulataneously
# Finds the difference of each values from their corresponding mean values
  for x,y in zip(df['daily_screen_time_hours'],df['sleep_duration_hours']):
    diff_of_screen_time = (x - mean_of_screen_time)
    diff_of_screen_time_squared += diff_of_screen_time * diff_of_screen_time

    diff_of_sleep_duration = (y - mean_of_sleep_duration)
    diff_of_sleep_time_squared += diff_of_sleep_duration * diff_of_sleep_duration

    numerator_sum = numerator_sum + (diff_of_screen_time * diff_of_sleep_duration)
    denominator_sum = diff_of_screen_time_squared * diff_of_sleep_time_squared

# Calculates the correlation coefficient
  output = Decimal((numerator_sum / sqrt(denominator_sum))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
  print("CORRELATION ANALYSIS")
  print(f"Correlation between screen time in hours and sleep duration in hours: {output}")
  print("\n")
  return output

# Calculates the standard deviation
def standard_deviation_mental_health_score(df,column_name):
  sum_of_mental_health_score = 0
  numerator_of_standard_deviation = 0

# Calculates mean to apply in the standard deviation calculation
  for value in df[column_name]:
    sum_of_mental_health_score += value
  mean_of_mental_health_score = sum_of_mental_health_score / len(df[column_name])

  for value in df[column_name]:
    numerator_of_standard_deviation = numerator_of_standard_deviation + (value - mean_of_mental_health_score) ** 2

# Variance and standard deviation calculation
  variance = numerator_of_standard_deviation / len(df[column_name])
  standard_deviation = sqrt(variance)
  return (variance, standard_deviation)

# Calculates the range of the data values
def ranges_for_sleep_duration(df):
  max = 0
  min = 100

# Finds the maximum and minimum values
  for value in df['sleep_duration_hours']:
    if max < value:
      max = value
    if min > value:
      min = value

  data_range = Decimal(max - min).quantize(Decimal("0.01"), rounding = ROUND_HALF_UP)
  print("\n")
  print("SLEEP DURATION STATISTICS")
  print("Least amount of sleep (hrs): ",min)
  print("Most amount of sleep (hrs): ", max)
  print("Range of sleep duration (hrs)", data_range)
  print("\n")
  return(min,max,data_range)

# Quick sort algorithm is implemented to be used whenever sorting is required
def sorting(df,column_name):
  lower_numbers = []
  greater_numbers = []
  sorted_list = []

# Converts dataframe to list to apply quick sort algorithm
# If it is already a list, no conversion
  if isinstance(df, pd.DataFrame):
    data = df[column_name].tolist()
  else:

    data = df

# Pivot element is the first element in the list
  if len(data) <= 1:
    return df
  else:
    pivot = data[0]

    for x in data[1:]:
# values lower than pivot value is added to lower_numbers list
      if x < pivot:
        lower_numbers.append(x)
# values same as pivot value is added to lower_numbers list
      elif x == pivot:
        lower_numbers.append(x)
# values higher than pivot value is added to greater_numbers list
      else:
        greater_numbers.append(x)
# recursive calling to sort the sub lists
    return sorting(lower_numbers,column_name) + [pivot] + sorting(greater_numbers,column_name)

# Calculates the median
def median(df,column_name):
  first_element = 0
  second_element = 0
# Calls the sorting function
  sorted_list = sorting(df,column_name)
  n = int(len(sorted_list))

# Median is calculated differently for even length and odd length lists
  if n % 2 == 0:

    first_element = sorted_list[int(n // 2)]
    second_element = sorted_list[(int(n // 2) -1)]
    median = (first_element + second_element) /2

  else:
    median = sorted_list[n//2] /2
  return median

# Calculates the mode
def mode_sleep_quality(df):
  sleep_quality_count = {}
  max_value = 0

# Iterates throught the dataframe to find the sleep_quality
  for index,row in df.iterrows():
    sleep_quality = row["sleep_quality"]

# Adds the sleep_quality in the dictionary else aggregate the count to find the frequency of each sleep_quality
    if sleep_quality not in sleep_quality_count:
      sleep_quality_count[sleep_quality] = 1
    else:
      sleep_quality_count[sleep_quality] += 1

  for key,value in sleep_quality_count.items():

# Identifies the sleep_quality that has the highest mode
    if max_value < value:
      max_value = value
      sleep_quality_mode = key

  print("MODE")
  print(f"Mode for the sleep quality: {sleep_quality_mode}")
  print("\n")
  return sleep_quality_mode

# Calculates the average screen time by each gender
def mean_daily_screen_time(df):
  male_count = 0
  female_count = 0
  other_count = 0
  sum_of_male_screen_time = 0
  sum_of_female_screen_time = 0
  sum_of_other_screen_time = 0

# Summing the values of screen time and count of each gender
  for index,row in df.iterrows():
    gender = row["gender"]

    if gender.lower() == "male":
      male_count += 1
      sum_of_male_screen_time += row["daily_screen_time_hours"]
    elif gender.lower() == "female":
      female_count += 1
      sum_of_female_screen_time += row["daily_screen_time_hours"]
    else:
      other_count += 1
      sum_of_other_screen_time += row["daily_screen_time_hours"]

  avg_female_screen_time = sum_of_female_screen_time / female_count
  avg_male_screen_time = sum_of_male_screen_time / male_count
  avg_other_screen_time = sum_of_other_screen_time / other_count
  print("AVERAGE SCREEN TIME BY GENDER")
  print(f"Average screen time of female: {avg_female_screen_time:.2f}")
  print(f"Average screen time of male: {avg_male_screen_time:.2f}")
  print(f"Average screen time of other: {avg_other_screen_time:.2f}")
  print("\n")
  return (avg_female_screen_time,avg_male_screen_time,avg_other_screen_time)

# Finds the oldest oarticipant
def oldest_participant(df):
  max_age = 0
# Iterates through the 'age' column
  for index, row in df.iterrows():
    age = row['age']
    if max_age < age:
      max_age = age
  print(f"Oldest participant's age: {max_age}")
  print("\n")
  return max_age

# Calculates the outliers using IQR, lower bound and upper bound values
def outliers_caffeine_intake_mg_per_day(df):
  outliers = []

# Calls sorting and median functions
  sorted_data = sorting(df,'caffeine_intake_mg_per_day')
  Q2 = median(df,'caffeine_intake_mg_per_day')
  n = len(df['caffeine_intake_mg_per_day'])

# Divides the sorted list into two halves based on the number of observations
  if n%2 ==0:
    lower_half = sorted_data[:n // 2]
    upper_half = sorted_data[n // 2:]
  else:
    lower_half = sorted_data[:n // 2]
    upper_half = sorted_data[n // 2 + 1:]
# Recursive calling of the function to calculate the median of two lists which is Q1 and Q3
  Q1 = median(lower_half,'caffeine_intake_mg_per_day')
  Q3 = median(upper_half,'caffeine_intake_mg_per_day')
  IQR = Q3 - Q1
# calculates the boundary values based on which outliers are identified
  lower_bound = Q1 - 1.5 * IQR
  upper_bound = Q3 + 1.5 * IQR

# Iterates the caffeine_intake_mg_per_day column and checks whether it is beyond the boundary values
# Appends the outliers to outliers list
  for index, row in df.iterrows():
    if row['caffeine_intake_mg_per_day'] not in outliers and (row['caffeine_intake_mg_per_day'] < lower_bound or
        row['caffeine_intake_mg_per_day'] > upper_bound):
          outliers.append(row['caffeine_intake_mg_per_day'])
  print("OUTLIERS DETECTION")
  print(f"IQR: {IQR:.2f}")
  print(f"lower_bound: {lower_bound:.2f}")
  print(f"upper_bound: {upper_bound:.2f}")
  print("List of values that are outliers in caffeine intake: ",outliers)
  return outliers,lower_bound,upper_bound,IQR

# Function to write the output to file
def output_file_parse(output_file_name,values):
  with open(output_file_name, "a") as f:
    f.write(values)
    f.write("\n")

# All the main functions are called from here
def main():
  flag = 'yes'
  while flag.lower() == 'yes':

    input_file_name = input("Enter the input file name to be read (CSV): ")
    output_file_name = input("Enter the output file name to be written (TXT): ")
    df = input_file_parse(input_file_name)
    print("\nTECH USE AND STRESS WELLNESS ANALYSIS\n")

    corr = correlation_screen_time_vs_sleep_duration(df)
    output_file_parse(output_file_name, "TECH USE AND STRESS WELLNESS ANALYSIS\nCORRELATION ANALYSIS")
    output_file_parse(output_file_name, f"Correlation between screen time and sleep duration: {corr}\n")


    var,stdev =standard_deviation_mental_health_score(df,'mental_health_score')
    var = Decimal(var).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    stdev = Decimal(stdev).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    print("MENTAL HEALTH STATISTICS")
    print("Variance of mental_health_score: ",Decimal(var).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    print("Standard Deviation of mental_health_score: ",Decimal(stdev).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    output_file_parse(output_file_name, f"MENTAL HEALTH STATISTICS\nVariance of mental_health_score: {var}")
    output_file_parse(output_file_name, f"Standard Deviation of mental_health_score: {stdev}\n")


    min,max,data_range = ranges_for_sleep_duration(df)
    output_file_parse(output_file_name, f"SLEEP DURATION STATISTICS\nLeast amount of sleep (hrs): {min}")
    output_file_parse(output_file_name, f"Maximum amount of sleep (hrs): {min}")
    output_file_parse(output_file_name, f"Range of sleep duration (hrs): {data_range}\n")


    med = median(df,'physical_activity_hours_per_week')
    print("MEDIAN")
    print("Median for the physical activity hours per week: ",med)
    print("\n")
    output_file_parse(output_file_name, f"MEDIAN\nMedian for the physical activity hours per week: {med}\n")


    mod = mode_sleep_quality(df)
    output_file_parse(output_file_name, f"MODE\nMode for the sleep quality: {mod}\n")


    female_screen_time, male_screen_time, other_screen_time = mean_daily_screen_time(df)
    output_file_parse(output_file_name, f"AVERAGE SCREEN TIME BY GENDER\nAverage screen time for female: {female_screen_time:.2f}")
    output_file_parse(output_file_name, f"Average screen time for male: {male_screen_time:.2f}")
    output_file_parse(output_file_name, f"Average screen time for other: {other_screen_time:.2f}\n")

    max_age = oldest_participant(df)
    output_file_parse(output_file_name, f"Oldest participant's age: {max_age}\n")


    out_list,lower_bound,upper_bound,IQR = outliers_caffeine_intake_mg_per_day(df)
    output_file_parse(output_file_name, f"OUTLIERS DETECTION \nIQR: {IQR:.2f}\nlower_bound: {lower_bound:.2f}\nupper_bound: {upper_bound:.2f}\n")
    output_file_parse(output_file_name, f"List of outliers in caffeine intake: {out_list}\n")
    print("File saved")


    flag = input("Do you want to run the program again: Yes or No: ")

main()