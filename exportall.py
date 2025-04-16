import pandas as pd
import sys
from omero.gateway import BlitzGateway
from omero.rtypes import unwrap
import tkinter as tk
from tkinter import filedialog, simpledialog

# Script to export all ROIs created in OMERO
def connect_to_omero():
    """
    Connect to the OMERO server using user-provided credentials.
    """
    root = tk.Tk()
    root.withdraw()

    host = simpledialog.askstring("OMERO Login", "Enter OMERO Host:", initialvalue="xxx")#put you inicial host
    username = simpledialog.askstring("OMERO Login", "Enter your OMERO Username:")
    password = simpledialog.askstring("OMERO Login", "Enter your OMERO Password:", show="*")

    conn = BlitzGateway(username, password, host=host, port=4064, secure=True)
    if not conn.connect():
        raise ConnectionError("Failed to connect to OMERO. Please check your credentials.")

    print("Successfully connected to OMERO.")
    return conn


def get_all_shapes(conn):
    """
    Retrieve all shapes from all images in all user-accessible groups.
    """
    all_data = []

    # Get all groups the user is a member of
    groups = conn.getGroupsMemberOf()

    for group in groups:
        group_id = group.getId()
        group_name = group.getName()

        # Switch to current group
        conn.setGroupForSession(group_id)
        print(f"\nCollecting data from group '{group_name}' (ID: {group_id})...")

        # Get all datasets in this group
        datasets = list(conn.getObjects("Dataset"))

        for dataset in datasets:
            dataset_id = dataset.getId()
            dataset_name = dataset.getName()

            print(f"Processing Dataset: {dataset_name} (ID: {dataset_id})")

            # Get all images in the dataset
            images = list(dataset.listChildren())

            for image in images:
                image_id = image.getId()
                image_name = image.getName()

                # Get ROIs from the image
                roi_service = conn.getRoiService()
                rois = roi_service.findByImage(image_id, None)

                for roi in rois.rois:
                    roi_id = roi.getId().getValue()

                    for shape in roi.copyShapes():
                        shape_id = shape.getId().getValue()
                        shape_type = shape.__class__.__name__.removesuffix("I")


                        # Get shape name (if any)
                        shape_name = unwrap(shape.getTextValue()) if shape.getTextValue() else ""

                        # Extract coordinates based on shape type
                        if shape_type == "Rectangle":
                            x, y = unwrap(shape.getX()), unwrap(shape.getY())
                            width, height = unwrap(shape.getWidth()), unwrap(shape.getHeight())
                            shape_data = f"X:{x}, Y:{y}, W:{width}, H:{height}"
                        elif shape_type == "Ellipse":
                            x, y = unwrap(shape.getX()), unwrap(shape.getY())
                            radiusX, radiusY = unwrap(shape.getRadiusX()), unwrap(shape.getRadiusY())
                            shape_data = f"X:{x}, Y:{y}, RX:{radiusX}, RY:{radiusY}"
                        elif shape_type == "Polygon":
                            points = unwrap(shape.getPoints())
                            shape_data = f"Points: {points}"
                        elif shape_type == "Polyline":
                            points = unwrap(shape.getPoints())
                            shape_data = f"Points: {points}"
                        elif shape_type == "Point":
                            x, y = unwrap(shape.getX()), unwrap(shape.getY())
                            shape_data = f"X:{x}, Y:{y}"
                        elif shape_type == "Line":
                            x1, y1 = unwrap(shape.getX1()), unwrap(shape.getY1())
                            x2, y2 = unwrap(shape.getX2()), unwrap(shape.getY2())
                            shape_data = f"X1:{x1}, Y1:{y1}, X2:{x2}, Y2:{y2}"
                        else:
                            shape_data = "Unknown Shape"

                        # Save the data
                        all_data.append([
                            group_id, group_name,
                            dataset_id, dataset_name,
                            image_id, image_name,
                            roi_id, shape_id, shape_type, shape_name, shape_data
                        ])

    return all_data


def save_to_csv(data):
    """
    Save shape data to a CSV file.
    """
    if not data:
        print("No shapes found to export.")
        return

    # Create DataFrame
    df = pd.DataFrame(data, columns=[
        "Group ID", "Group Name",
        "Dataset ID", "Dataset Name",
        "Image ID", "Image Name",
        "ROI ID", "Shape ID", "Shape Type", "Shape Name", "Coordinates & Dimensions"
    ])

    # Ask where to save the file
    root = tk.Tk()
    root.withdraw()
    csv_file = filedialog.asksaveasfilename(
        title="Save CSV file",
        defaultextension=".csv",
        filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
    )

    if csv_file:
        df.to_csv(csv_file, index=False, encoding="utf-8")
        print(f"File saved at: {csv_file}")
    else:
        print("No file was saved.")


if __name__ == "__main__":
    # Prevent double execution
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        sys.exit()

    try:
        # Connect to OMERO
        conn = connect_to_omero()

        # Retrieve all shape data
        shape_data = get_all_shapes(conn)

        # Save to CSV
        save_to_csv(shape_data)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if conn:
            conn.close()
        sys.exit()  # Prevent double execution in some environments
