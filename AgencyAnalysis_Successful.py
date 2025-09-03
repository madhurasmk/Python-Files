import pyodbc
import pandas as pd
from tabulate import tabulate
from termcolor import colored
from colored import fg
from flask import Flask, render_template, request
from datetime import datetime, timedelta
app = Flask(__name__)
server = 'tp-dev-sql.database.windows.net'  # Replace with your server name or IP
database = 'Staging_Web_Interactions'  # Replace with your database name
username = 'sqladmin'  # Replace with your username
password = 'TPDon#2024'  # Replace with your passworD
@app.route('/')
def display_data():
    try:
        # Create connection string
        connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"

        # Establish the connection
        connection = pyodbc.connect(connection_string)

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()
        print(colored("Connection to SQL Server database established successfully.", "green"))
        print("Connection to SQL Server database established successfully.")
        # timeframe = 'week'
        timeframe =  input ("Enter the timeframe (hours/week/prev_week/month) : ") #timeframe
        query = input("Enter scenario (S - Successful; U - UW Block; E - Error) : ")
        querySuccess= """
         DECLARE @timeframe NVARCHAR(50) = ?;
        DECLARE @month_start DATE;
        DECLARE @month_end DATE;
        DECLARE @prev_week_start DATE;
        DECLARE @prev_week_end DATE;
        DECLARE @week_start DATE;
        DECLARE @week_end DATE;
        
        SET @month_start = DATEADD(MONTH, -1, GETDATE());
        SET @month_end = GETDATE();
        SET @prev_week_start = DATEADD(WEEK, -2, GETDATE());
        SET @prev_week_end = DATEADD(WEEK, -1, GETDATE());
        SET @week_start = DATEADD(WEEK, -1, GETDATE());
        SET @week_end = GETDATE();
            SELECT 
                am.agencyName, quoteNumber --,
                --COUNT(DISTINCT f.QuoteNumber) AS SuccessfulQuoteCount
            FROM FlattenPageViewData f
            JOIN AgencyMapping am
                ON f.userId = am.agentName
            WHERE f.QuoteStatus IN ('Bound')
              AND (
                  (@timeframe = 'hours' AND SaveDateTime >= DATEADD(HOUR, -24, GETDATE()))
                  OR (@timeframe = 'prev_week' AND CONVERT(DATE, SaveDateTime) BETWEEN @prev_week_start AND @prev_week_end)
                  OR (@timeframe = 'week' AND CONVERT(DATE, SaveDateTime) BETWEEN @week_start AND @week_end)
                  OR (@timeframe = 'month' AND CONVERT(DATE, SaveDateTime) BETWEEN @month_start AND @month_end)
              )
            GROUP BY am.agencyName, QuoteNumber
            order by am.agencyName, QuoteNumber
        """
        queryUWB="""        
        DECLARE @timeframe NVARCHAR(50) = ?;
        DECLARE @month_start DATE;
        DECLARE @month_end DATE;
        DECLARE @prev_week_start DATE;
        DECLARE @prev_week_end DATE;
        DECLARE @week_start DATE;
        DECLARE @week_end DATE;
        
        SET @month_start = DATEADD(MONTH, -1, GETDATE());
        SET @month_end = GETDATE();
        SET @prev_week_start = DATEADD(WEEK, -2, GETDATE());
        SET @prev_week_end = DATEADD(WEEK, -1, GETDATE());
        SET @week_start = DATEADD(WEEK, -1, GETDATE());
        SET @week_end = GETDATE();
        
        
        -- UW Block Counts
        --WITH uwBlockCounts AS (
            SELECT 
                am.agencyName, 
                sq5.QuoteNumber
            FROM (
                SELECT DISTINCT userId, QuoteNumber
                FROM FlattenPageViewData
                WHERE ErrorType = 'UW Block'
                  AND QuoteNumber IS NOT NULL
                  AND (
                      (@timeframe = 'hours' AND SaveDateTime >= DATEADD(HOUR, -24, GETDATE()))
                      OR (@timeframe = 'prev_week' AND CONVERT(DATE, SaveDateTime) BETWEEN @prev_week_start AND @prev_week_end)
                      OR (@timeframe = 'week' AND CONVERT(DATE, SaveDateTime) BETWEEN @week_start AND @week_end)
                      OR (@timeframe = 'month' AND CONVERT(DATE, SaveDateTime) BETWEEN @month_start AND @month_end)
                  )
            ) sq5
            JOIN AgencyMapping am
                ON sq5.userId = am.agentName
            GROUP BY am.agencyName, sq5.QuoteNumber
            order by am.agencyName, sq5.QuoteNumber
        """
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
            # Get current date

        if query =="S":
            cursor.execute(querySuccess, (timeframe, ))
            rows = cursor.fetchall()
            # Get column names
            columns = [column[0] for column in cursor.description]

            percentage_columns = ['UWBlockPercentage', 'NonUWErrorPercentage', 'SuccessfulQuotePercentage']
            # Clean the rows to remove newline characters
            cleaned_rows = [
                tuple(str(value).replace("\n", " ").strip() if isinstance(value, str) else value for value in row)
                for row in rows
            ]

            # Create a DataFrame
            df = pd.DataFrame.from_records(cleaned_rows, columns=columns)
            df = df[df["agencyName"] != "Agency not mapped"]

            # Replace \n in the DataFrame for clean display
            df.replace(r'\n', ' ', regex=True, inplace=True)
        elif query == "U":
            cursor.execute(queryUWB, (timeframe,))
            rows = cursor.fetchall()
            # Get column names
            columns = [column[0] for column in cursor.description]

            percentage_columns = ['UWBlockPercentage', 'NonUWErrorPercentage', 'SuccessfulQuotePercentage']
            # Clean the rows to remove newline characters
            cleaned_rows = [
                tuple(str(value).replace("\n", " ").strip() if isinstance(value, str) else value for value in row)
                for row in rows
            ]

            # Create a DataFrame
            df = pd.DataFrame.from_records(cleaned_rows, columns=columns)
            df = df[df["agencyName"] != "Agency not mapped"]

            # Replace \n in the DataFrame for clean display
            df.replace(r'\n', ' ', regex=True, inplace=True)
        else:
            print("Invalid choice")
        connection.close()
        print("Connection closed.")
        return render_template('AgencyAnalysisTable.html', tables=[df.to_html(classes='data', header="False")], timeframe=timeframe,     start_date=start_date,     end_date=end_date)

    except pyodbc.Error as e:
        print(colored(f"Error while connecting to SQL Server: {e}", "red"))

    # finally:
    #     # Clean up and close the connection
    #     if 'connection' in locals() and connection:
    #         connection.close()
    #         print(colored("Connection closed.", "blue"))
if __name__ == '__main__':
    app.run(debug=True)