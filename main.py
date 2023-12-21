# from fastapi import FastAPI, HTTPException, Depends
# import pandas as pd 
# import redis
# import json

# app = FastAPI()

# def get_redis():
#     redis_host = "redis"  # This should match the service name in the docker-compose.yml file
#     redis_port = 6379
#     return redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)


# # Define endpoint to get FIFA data from Redis
# @app.get("/fifa_data")
# async def get_fifa_data(r: redis.Redis = Depends(get_redis)):
#     try:
#         # Retrieve data from Redis
#         fifa_data_json = r.get('fifa_eda_stats_data')

#         # Check if data exists
#         if not fifa_data_json:
#             raise HTTPException(status_code=200, detail="FIFA data not found in Redis")

#         # Convert JSON data from Redis to a Python object
#         fifa_data = json.loads(fifa_data_json)

#         # Return the data as JSON response
#         return fifa_data
#     except (redis.exceptions.ConnectionError, redis.exceptions.AuthenticationError) as e:
#         raise HTTPException(status_code=200, detail=f"Error connecting to Redis: {str(e)}")

# # Read the CSV file into a DataFrame named 'df'
# df = pd.read_csv('fifa_eda_stats.csv')
# print(df)

# # Transformation Section
# # Calculate and print the number of unique IDs in the 'ID' column
# unique_ids_count = df['ID'].nunique()
# print(f"Number of unique IDs: {unique_ids_count}")

# # Extract unique player information (Name, Age, Nationality) and remove duplicate rows
# unique_player_info = df[['Name', 'Age', 'Nationality']].drop_duplicates()
# # Display the resulting DataFrame containing unique player information
# print(unique_player_info)

# # Group the DataFrame by player name, summing up the numerical columns, and reset the index
# unique_player_stats = df.groupby('Name').sum().reset_index()
# # Display the resulting DataFrame showing unique player statistics (summed values for each player)
# print(unique_player_stats)

# # Group the DataFrame by 'Nationality' and sum up all numerical columns for each country
# matches_won_by_country = df.groupby('Nationality').sum().reset_index()
# # Display the resulting DataFrame showing the total matches won by each country
# print(matches_won_by_country)

# # Store in Redis
# # Convert into a DataFrame
# df_json = df.to_json(orient='records')

# # Connect to Redis
# r = get_redis()

# # Save data to Redis
# try:
#     r.set('fifa_eda_stats_data', df_json)
#     print("Data successfully saved to Redis.")
# except (redis.exceptions.ConnectionError, redis.exceptions.AuthenticationError) as e:
#     print(f"Error connecting to Redis: {str(e)}")


from fastapi import FastAPI, HTTPException, Depends
import pandas as pd
import redis
import json

# Create a FastAPI instance
app = FastAPI()

# Function to get a Redis connection
def get_redis():#to get a connection to Redis.
    redis_host = "redis"  # This should match the service name in the docker-compose.yml file
    redis_port = 6379
    return redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

# Define an endpoint to get FIFA data from Redis
@app.get("/fifa_data")#Defines a FastAPI endpoint to retrieve FIFA data from Redis.
async def get_fifa_data(r: redis.Redis = Depends(get_redis)):
    try:
        # Retrieve data from Redis
        fifa_data_json = r.get('fifa_eda_stats_data')

        # Check if data exists
        if not fifa_data_json:
            raise HTTPException(status_code=200, detail="FIFA data not found in Redis")

        # Convert JSON data from Redis to a Python object
        fifa_data = json.loads(fifa_data_json)

        # Return the data as a JSON response
        return fifa_data
    except (redis.exceptions.ConnectionError, redis.exceptions.AuthenticationError) as e:
        raise HTTPException(status_code=200, detail=f"Error connecting to Redis: {str(e)}")

# Read the CSV file into a DataFrame named 'df'
df = pd.read_csv('fifa_eda_stats.csv')

# Print the DataFrame
print(df)

# Transformation Section

# Calculate and print the number of unique IDs in the 'ID' column
unique_ids_count = df['ID'].nunique()
print(f"Number of unique IDs: {unique_ids_count}")

# Extract unique player information (Name, Age, Nationality) and remove duplicate rows
unique_player_info = df[['Name', 'Age', 'Nationality']].drop_duplicates()

# Display the resulting DataFrame containing unique player information
print(unique_player_info)

# Group the DataFrame by player name, summing up the numerical columns, and reset the index
unique_player_stats = df.groupby('Name').sum().reset_index()

# Display the resulting DataFrame showing unique player statistics (summed values for each player)
print(unique_player_stats)

# Group the DataFrame by 'Nationality' and sum up all numerical columns for each country
matches_won_by_country = df.groupby('Nationality').sum().reset_index()

# Display the resulting DataFrame showing the total matches won by each country
print(matches_won_by_country)

# Store in Redis

# Convert the DataFrame into JSON
df_json = df.to_json(orient='records')

# Connect to Redis
r = get_redis()

# Save data to Redis
try:
    r.set('fifa_eda_stats_data', df_json)
    print("Data successfully saved to Redis.")
except (redis.exceptions.ConnectionError, redis.exceptions.AuthenticationError) as e:
    print(f"Error connecting to Redis: {str(e)}")
