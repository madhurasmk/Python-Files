import pyodbc
import pandas as pd
from tabulate import tabulate
from termcolor import colored
from colored import fg
from flask import Flask, render_template, request
from datetime import datetime, timedelta
from datetime import datetime, timedelta
app = Flask(__name__)
server = r'localhost\SQLEXPRESS'  # Change to your SQL Server instance name
database = 'Staging_Web_Interactions_22Jan25_Bkp'  # Your database name
# stored_procedure = 'EXEC AgencySummaryPerformance'
timeframe =  input ("Enter the timeframe (hours/week/prev_week/month) : ") #timeframe
SumAnalysis = int(input ("Enter 1 for Agency Analysis Report and 2 for Agency Summary Report : "))
# print("Hello ", SumAnalysis)
@app.route('/')
def display_data():
    try:

        # Establish database connection
        conn_str = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()

        current_date = datetime.now()
        if timeframe == 'hours':
            start_date = (current_date - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
        elif timeframe == 'week':
            start_date = (current_date - timedelta(days=7)).strftime('%Y-%m-%d')
        elif timeframe == 'prev_week':
            start_date = (current_date - timedelta(days=14)).strftime('%Y-%m-%d')
            end_date = (current_date - timedelta(days=7)).strftime('%Y-%m-%d')
        elif timeframe == 'month':
            start_date = (current_date - timedelta(days=30)).strftime('%Y-%m-%d')
        else:
            return "Invalid timeframe", 400  # Return a bad request response

        end_date = current_date.strftime('%Y-%m-%d')

        # Call the appropriate stored procedure
        stored_procedure = "AgencyAnalysisPerformance" if SumAnalysis == 1 else "AgencySummaryPerformance"
        cursor.execute(f"EXEC {stored_procedure} ?", (timeframe,))
        rows = cursor.fetchall()

        # Get column names
        columns = [column[0] for column in cursor.description]

        # Convert data to DataFrame
        df = pd.DataFrame.from_records(rows, columns=columns)

        # Format columns
        if SumAnalysis == 1:
            percentage_columns = ['UWBlockPercentage', 'NonUWErrorPercentage', 'SuccessfulQuotePercentage',
                                  'DeclinedQuotePercentage']
            for col in percentage_columns:
                if col in df.columns:
                    df[col] = df[col].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else x)
        else:
            if 'TotalPremium' in df.columns:
                df['TotalPremium'] = df['TotalPremium'].apply(lambda x: f"$ {x:.2f}" if pd.notna(x) else x)

        # Close connection
        connection.close()

        def colorize_text(df, text_column):
            """
            Applies color to text based on color names in a dataframe column.
            """
            def apply_color(row):
                color = row[text_column]
                return [f"color: {color}" if pd.notna(color) else "" for _ in row]

                # Apply styling
            styled_df = df.style.apply(apply_color, axis=1)

            # Hide the column by setting display properties
            if (SumAnalysis == 1):
                styled_df = styled_df.hide(axis="columns", subset=[text_column])  # 'AgencyId'
            else:
                styled_df = styled_df.hide(axis="columns", subset=[text_column, 'AgencyId'])  #

            return styled_df

        styled_df = colorize_text(df, 'PerformanceStatus')  if SumAnalysis ==1 else colorize_text(df, 'AgencySummaryPerformance')

            # Render appropriate template
        template_name = 'AgencyAnalysisTable.html' if SumAnalysis == 1 else 'AgencySummaryTable.html'
        return render_template(template_name, tables=[styled_df.to_html(classes='data', index=False, escape=False)],
                               timeframe=timeframe, start_date=start_date, end_date=end_date)

    except pyodbc.Error as e:
        return f"Database connection error: {e}", 500  # Return server error response

if __name__ == '__main__':
    app.run(debug=True)