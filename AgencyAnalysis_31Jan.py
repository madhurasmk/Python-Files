import pyodbc
import pandas as pd
from tabulate import tabulate
from termcolor import colored
from colored import fg
from flask import Flask, render_template, request

app = Flask(__name__)
server = r'localhost\SQLEXPRESS'  # Change to your SQL Server instance name
database = 'Staging_Web_Interactions_22Jan25_Bkp'  # Your database name
stored_procedure = 'GetAgencyPerformanceCounts'
timeframe='month'
# Windows Authentication (Trusted Connection)

@app.route('/')
def display_data():
    try:
        # Create connection string
        connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
        # connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"

        # Establish the connection
        connection = pyodbc.connect(connection_string)

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()
        print(colored("Connection to SQL Server database established successfully.", "green"))
        print("Connection to SQL Server database established successfully.")
        # timeframe = 'week'
        # timeframe =  input ("Enter the timeframe (hours/week/prev_week/month) : ") #timeframe
        query = """select * from FlattenPageViewData"""
        cursor.execute(query, (timeframe, ))
        rows = cursor.fetchall()
        from datetime import datetime, timedelta

        # Get current date
        current_date = datetime.now()

        # Calculate date ranges based on timeframe
        if timeframe == 'hours':
            start_date = (current_date - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
            end_date = current_date.strftime('%Y-%m-%d %H:%M:%S')
        elif timeframe == 'week':
            start_date = (current_date - timedelta(days=7)).strftime('%Y-%m-%d')
            end_date = current_date.strftime('%Y-%m-%d')
        elif timeframe == 'prev_week':
            start_date = (current_date - timedelta(days=14)).strftime('%Y-%m-%d')
            end_date = (current_date - timedelta(days=7)).strftime('%Y-%m-%d')
        elif timeframe == 'month':
            start_date = (current_date - timedelta(days=30)).strftime('%Y-%m-%d')
            end_date = current_date.strftime('%Y-%m-%d')
        else:
            start_date = "N/A"
            end_date = "N/A"
        # Process the results
        # for row in rows:
        #     print(row)
        # Get column names
        columns = [column[0] for column in cursor.description]

        # percentage_columns = ['UWBlockPercentage', 'NonUWErrorPercentage', 'SuccessfulQuotePercentage']
        # Clean the rows to remove newline characters
        cleaned_rows = [
            tuple(str(value).replace("\n", " ").strip() if isinstance(value, str) else value for value in row)
            for row in rows
        ]

        # Create a DataFrame
        df = pd.DataFrame.from_records(cleaned_rows, columns=columns)
        # df = df[df["AgencyName"] != "Agency not mapped"]
        print(df)

        # Replace \n in the DataFrame for clean display
        # df.replace(r'\n', ' ', regex=True, inplace=True)
        # # percentage_columns = ['UWBlockPercentage', 'NonUWErrorPercentage', 'SuccessfulQuotePercentage', 'DeclinedQuotePercentage']
        #
        # if not df.empty:
        #     for col in percentage_columns:
        #         df[col] = df[col].apply(lambda x: f"{x:.2f}%")

        # Function to color the text based on PerformanceStatus
        # def colorize_text(df, text_column):
        #     """
        #     Applies color to text based on color names in a dataframe column.
        #     """
        #
        #     def apply_color(row):
        #         color = row[text_column]
        #         return [f"color: {color}" if pd.notna(color) else "" for _ in row]
        #
        #         # Apply styling
        #
        #     styled_df = df.style.apply(apply_color, axis=1)
        #
        #     # Hide the column by setting display properties
        #     styled_df = styled_df.hide(axis="columns", subset=[text_column])
        #
        #     return styled_df
        #
        # # styled_df = df.style.apply(
        #     #     lambda row: [f"color: {row[text_column]}" if pd.notna(row[text_column]) else "" for _ in row], axis=1).hide_columns([text_column])
        #
        #
        # styled_df = colorize_text(df, 'PerformanceStatus')
        #styled_df1 = styled_df.drop('PerfomanceStatus', axis=1)
           # except pyodbc.Error as e:
    #     print("Error while connecting to SQL Server:", e)
    #
    # finally:
    #     # Clean up and close the connection
    #     if 'connection' in locals() and connection:
        connection.close()
        print("Connection closed.")
        return render_template('AgencyAnalysisTable.html', tables=[df.to_html(classes='data', header="False")],
                               timeframe=timeframe, start_date=start_date, end_date=end_date)

    except pyodbc.Error as e:
        print(colored(f"Error while connecting to SQL Server: {e}", "red"))

    # finally:
    #     # Clean up and close the connection
    #     if 'connection' in locals() and connection:
    #         connection.close()
    #         print(colored("Connection closed.", "blue"))
if __name__ == '__main__':
    app.run(debug=True)