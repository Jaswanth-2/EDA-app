Data Dashboard and Visualization App
This repository contains a multi-page Streamlit application for uploading, analyzing, and visualizing datasets. The app offers a user-friendly interface to perform exploratory data analysis (EDA), generate automated dashboards, and create custom visualizations.

Features

File Uploads: Supports CSV, Excel (.xlsx, .xls), and JSON file formats.
Automated EDA: Generates a detailed data summary report using ydata-profiling, which can be downloaded in both HTML and PDF formats.
Smart Dashboard: Automatically generates key performance indicators (KPIs) and a variety of interactive charts (e.g., bar, line, scatter, correlation heatmaps) based on the uploaded data's column types (numerical, categorical, date).
Multi-library Visualizations: Offers a choice of visualization libraries, including Plotly, Matplotlib, Seaborn, and Altair, for generating different chart types.
Dynamic Filtering: Users can filter data by date range and categorical values directly from the sidebar.
Customizable Dashboard Builder: An advanced feature that allows users to create a custom dashboard by adding and arranging different chart tiles.
Data Cleaning and Download: Provides options to view and download cleaned versions of the dataset, either with duplicates removed or with missing values filled.
Multilingual Support: The dashboard interface supports multiple languages, including English and Hindi.


 Project Structure
 
upload page.py: Handles file uploads and data session management.
dashboard.py: Contains the core logic for the automated dashboard, including data type detection, KPI generation, and chart creation.
preview.py: Manages the data preview and automated EDA report generation.
advanced visualization.py: Implements the custom, drag-and-drop dashboard builder.



Installation
To run this application, you will need to have Python and the required libraries installed.

Clone the repository:

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

pip install -r requirements.txt



How to Run

Start the Streamlit application from your terminal:

streamlit run "upload page.py"
The application will open in your web browser. You can then navigate between the different pages (upload page.py, dashboard.py, preview.py) to access the various features.

Upload Data: Go to the "Upload Your Dataset" page (upload page.py) and upload a supported file.

View Preview & Summary: Navigate to the preview.py page to see a data preview, download cleaned versions, and view the automated EDA report.

Explore Dashboard: Head to the "Smart Auto-Generated Dashboard" (dashboard.py) to see automated visualizations and KPIs. Use the sidebar to apply filters or change visualization settings.

Build Custom Dashboard: Visit the advanced visualization.py page to create your own dashboard by adding different charts.

