=========================================
 OMERO ROI Exporter to CSV
=========================================

Description:
------------
This Python script connects to an OMERO server and exports all ROIs (Regions of Interest) 
created by the user across all accessible groups, datasets, and images. It retrieves detailed 
information about each shape (type, coordinates, dimensions, name, etc.) and saves the data 
into a structured CSV file.

Features:
---------
- Connects securely to an OMERO server using user-provided credentials.
- Retrieves all user-accessible groups and iterates through all datasets and images.
- Extracts all ROI shapes: Rectangle, Ellipse, Polygon, Polyline, Point, Line.
- Captures ROI metadata such as shape type, position, dimensions, and labels.
- Exports the collected information into a CSV file.

CSV Output Format:
------------------
The resulting CSV file contains the following columns:

| Column                 | Description                                   |
|------------------------|-----------------------------------------------|
| Group ID               | ID of the OMERO group.                        |
| Group Name             | Name of the OMERO group.                      |
| Dataset ID             | ID of the dataset containing the image.       |
| Dataset Name           | Name of the dataset.                          |
| Image ID               | ID of the image containing the ROI.           |
| Image Name             | Name of the image.                            |
| ROI ID                 | ID of the ROI object.                         |
| Shape ID               | ID of the shape inside the ROI.              |
| Shape Type             | Type of the shape (e.g., Rectangle, Ellipse).|
| Shape Name             | Text label associated with the shape.         |
| Coordinates & Dimensions | Detailed geometry of the shape.             |

Requirements:
-------------
The script requires the following Python libraries:
- pandas
- omero-gateway
- tkinter (included with most Python distributions)

Installation:
-------------
Install the required dependencies using:

pip install pandas pip install omero-py

If `tkinter` is missing (mostly on Linux), install it using:

sudo apt-get install python3-tk

Usage:
------
1. Run the script:
python exportall.py
2. Enter your OMERO server, username, and password.
3. The script will iterate through all accessible groups and datasets, extracting shape data.
4. Choose the location and name for the CSV output file when prompted.
5. The resulting CSV file will be saved with all shape data included.

Author:
-------
This script was developed by **Daurys De Alba**.

For inquiries, contact:
- Email: daurysdealbaherra@gmail.com
- Email: DeAlbaD@si.edu
