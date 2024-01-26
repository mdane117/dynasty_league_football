import pandas as pd
import os

# Path to the directory where the files are stored
file_path = "C:\\Users\\matth\\Desktop\\Python\\Web Scraper\\player_ranking_data\\"

# List of file names
file_names = ['qb_rankings.csv', 'rb_rankings.csv', 'wr_rankings.csv', 'te_rankings.csv']

# Function to combine CSV files
def combine_csv_files(file_list):
    combined_data = pd.concat(file_list, ignore_index=True)
    return combined_data

# Function to save combined data to a new CSV file
def save_combined_data(combined_data, output_file):
    combined_data.to_csv(output_file, index=False)
    print(f"Data from {len(file_list)} CSV files combined and saved to {output_file} successfully.")

if __name__ == "__main__":
    file_list = [pd.read_csv(os.path.join(file_path, file)) for file in file_names]
    
    try:
        combined_data = combine_csv_files(file_list)
        save_combined_data(combined_data, os.path.join(file_path, "ff_rankings.csv"))
    except pd.errors.EmptyDataError:
        print("One or more input files is empty.")