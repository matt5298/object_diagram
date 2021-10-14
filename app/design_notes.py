# Notes on how application works currently are in __init__.py
# creating a window application
# take data and turn it into object diagrams

# have a main window with menu and drawing canvas
# have events

# each object created has a unique GUID, Name
# each object is displayed in a shape
# each object has dictionary of attributes
# each object has array of attributes that are displayed


# Import Data
# have a parsing module that is able to parse external data into structure for an object

# Draw Objects
# take list of objects and draw them to the canvas
# connect events to the objects so they can be manipulated

# Data Store
# have a data store abstraction layer that will allow for different possible data stores
# read object
# write object
# delete object
# query objects

# store objects in json format