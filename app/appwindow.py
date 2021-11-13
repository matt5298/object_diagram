# The main window for the application

# idea
    # have the ability to visually build a command
    # A data object list
        # has list of data
        # displays the data
        # can scroll the data if it's off the screen
        # can search the data by typing in text (regex support?). requires a data entry area
        # can select one or more items by clicking on them.
        # drop the object on another and the selected items are copied or moved to it.
        
    # have an data object that can display, search, select tags
    # have an data object that can display, search, select tags

# Additional abilities needed from pointer
    # ability to trigger an activity.  For example a TimeoutError
    # Maybe the objects that are created and are children can have different reactions to the double click Event
    # Send the double click event to the group if pointer is in group mode.  Then the invividual objects react based upon if they have a doubel clicked function to call or not
    # Send the double click event to the individual item if pointer is in id mode. still will only react if it has the double clicked function

# To do
    # display all tags from all objects on the canvas in a compound object

# to do
    # to create a compound object
    # have _id_background: the is also the lowest member because all other objects will be .tag_raise(<this group tag>, <background id>)
    # have the count of member objects
    # _add_object(): to add an object and put it in the correct display number
    # tag_object(): to add a tag to all objects in the object
    # remove_object(): to remove the object tag from the object.
    # to readjust all elements position in the display list use .tag_raise(<this group tag>, <background id>)
    # add new text item to the object
    # have object able to be hidden and shown.  Use tags to designate hidden and shown items.
    # have app tags that are prefixed with _
    # have a right click function display a context sensitive menu


    # detection of collisions happens with the background object
    # detection of overlaps can happen with the background object, and/or with the component objects
    

# v0.05
    # currently I have the dragging and dropping working in the following manner
        # the mode is id or sourceNameTag
        # added to _drag_data, sourceNameTag, sourceIndex (the location in the display list)
        # in pointer.select() get the sourceIndex for the lowest item in the id or sourceNameTag
        # in pointer._drop_def() return the item to it's location which is below the item currently in sourceIndex of display list
        # have not implemented in pointer._drop_move()
            # bugs in the pointer._drop_move for pointer id move mode.  haven't tested pointer group move mode.

    #Todo
        # new attribute tags to identify object attributes
        # _background: for the background of the object.  This can only be dragged in group mode with the Name tag
        # _item: for an item that is a member of the object.  This is dragged by it's Item tag


    # modify pointer code
        # in object mode get the Name tag and move the object
        ## in item move mode get the Item tag and then drop on the Name tag if there is one
        # for _background drag in tag mode using the Name tag
        # for _item drag in tag mode using the Item tag
        # adding a tag to the selected object _source
        # adding a tag to the target _target
        # then delete the sources Name tag and add to it the target's Name tag
        # then remove the source and target tags

# v0.04 pointer_mode object implemented
    # this encapsulated all the drag and drop functionality for the different pointer modes.
    # have implemented group, id, group move, id move modes.


# v0.03 drag and drop functionality
#   additional pointer mode: dnd move
    # this will switch the pointer to id mode
    # will then when the item is dropped on another object will change the tag "Name" of the item dragged to the item it was dropped on
    # this is works as a rough proof of concept.  
    # works as long as the dragged item, source, is put at the top of the canvas when the drag is started.
    # when the source is dropped onto the target, currently it's location in the display list is not recalculated so it remains at the top.

#v0.02 2021_10_13 implemented some formatting
    # justify of the text objects
    # changing the selection mode of the pointer from group(tag) to individual(id)

#v0.01 2021_10_12 implemented dragging a group of canvas objects
    # did this by assigning a tag prefixed with "Name" to each object created in the group
    # then on the click event it finds the nearest object and gets the tag prefixed with "Name"
    # it stores the "Name" tag in the _drag_data as the item.  Then the other events
    # will accept the tag or id.  If they get a tag that matches multiple objects all those
    # objects are updated at the same time and so are dragged together and treated as a group.

#v0.00 2021_10_11 Have main window
# Have buttons for menu
# Create object creates a rectangle that can be dragged

import tkinter as tk
from tkinter import Event, messagebox
#from tkinter.filedialog import askopenfilename, asksaveasfilename
from objects import ZObject

# to bring together the code to implement pointer modes
# inherit and extend functions as needed
# the app is expecting the Select, Drag, Drop functions and will bind to them when the pointer object is set in the app
# basic pointer can operate in id or tagName modes.  The inherited classes implement one or the other and set their name and modes appropriately

class Pointer_Mode:
    def __init__(self, myCanvas):
        self.name = "Pointer"
        self.myCanvas = myCanvas
        # which identifier out of _drag_data will be used
        # id or tagName. used as keyname to retrieve correct value from _drag_data dictionary
        self._mode = "id"
        # tag that will be used to mark the item(s) being dragged
        self._drag_source = '_Source'
        # marks the item that is the target in a drag and drop
        self._drag_target = '_Target'

        self.reset_drag_data()

        # need to setup the public methods
        # always present the functions: select, move, drop
        # if they need to be modified then overwrite in an inherited
        # class or there may be an intern function that can be set 
        # to one of these functions.
        self.drop = self._drop_def
    
    def reset_drag_data(self):
        # sourceNameTag is the name tag that is for the object clicked on
        # targetNameTag is the name tag of the drop target
        # displayListStart is the 
        self._drag_data = {"x": 0, "y": 0, "id":None, "sourceNameTag":None, "targetNameTag":None, "sourceIndex":None}


    def select(self, event):
        """Begining drag of a group"""
        # record its location and tag it
        # get the object id and tagName
        id = self.myCanvas.find_closest(event.x, event.y)[0]
        self._drag_data['id'] = id 
        self._drag_data['sourceNameTag'] = self._getObjectNameTag(self._drag_data['id'])
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        #get the location in the display list of the current item based on _mode
        # this is the index of the item in the list of all items.
        print("Current select mode: " + self._mode + ", tag/id: " + str(self._drag_data[self._mode]) )
        # get array of items in canvas with the tag or id
        items = self.myCanvas.find_all()
        # the first item in the find_withtag(tag or id) returned array is the lowest one in the display list.  
        sourceLowItem = self.myCanvas.find_withtag(self._drag_data[self._mode])[0]
        # get it's index in the items list
        self._drag_data['sourceIndex'] = items.index(sourceLowItem)
        #print('{}, {}'.format(self._drag_data["sourceIndex"],items))
        
        #raise selected item to the topmost in the canvas
        self.myCanvas.tag_raise(self._drag_data[self._mode], 'all')

        #print('Pointer mode: {}'.format(self._mode))
        print('Selected item tags: ' + str(self.myCanvas.gettags(self._drag_data[self._mode])))

    def move(self, event):
        """Handle dragging of a group"""
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        self.myCanvas.move(self._drag_data[self._mode], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def _drop_def(self, event):
        """End drag of an object"""
        # return the item to it's place in the display
        # acts on the tags of the selected item.
        # print('Before replacing: {}'.format(self.myCanvas.find_all()))
        
        # get all the items from which we can get the item at the index of sourceIndex
        items = self.myCanvas.find_all()
        #lower the current item to below the item in the location of sourceIndex
        #this will place the item to where it was befor.  If _mode = id then only the one item moves
        #if _mode=sourceNameTag then all items with that tag will be moved and maintain their relative locations.
        self.myCanvas.tag_lower(self._drag_data[self._mode],items[self._drag_data['sourceIndex']])
        #print('After replacing: {}'.format(self.myCanvas.find_all()))

        self.reset_drag_data()

    def drop(self, event):
        pass

    def _drop_move(self, event):
        """End drag of an object"""
        print('!!!!!Ending move and dropping!!!!!')
        # get the source tag/id according to the _mode
        source = self._drag_data[self._mode]

        # add the tag source1 to mark the group
        # later the name tag is removed so need something to mark it
        self.myCanvas.addtag_withtag( 'source1', source)
        print ('Source object tags: {}'.format(self.myCanvas.gettags('source')))

        # find object below the moved item
        # returns the item below in the order, not in relation to where it is on the canvas
        #target = self.myCanvas.find_below(self._drag_data['item'])

        # get the item that intersects with the bounding box of the dragged item
        bboxSource = self.myCanvas.bbox(source)
        print (bboxSource)
        x1,y1,x2,y2 = bboxSource
        # The dragging object, source has been moved to the front on drag start
        # that means the target will always be below it. [0] will be the bottom of the overlapping objects returned
        # this returns the id of the target no matter what the _mode is set to
        target = self.myCanvas.find_overlapping(x1,y1,x2,y2)[0]

        print ('Drop x,y: {},{}'.format(event.x, event.y))
        print ('Target item: {}'.format(target,))

        # get it's tag name

        tagTarget = self._getObjectNameTag(target)
        print ('Target tag: {}'.format(tagTarget,))

        # change the tag name that's in the _drag_data item 
        
        
        # delete the original Name tag for the source object, the one dragged
        print ('Deleting from {}, tag {}'.format(source,self._getObjectNameTag(source)))
        self.myCanvas.dtag(source,self._getObjectNameTag(source))
        # add the new Name tag to the source object to group it with the object dropped on
        # need to use the 'source' tag because the Name tag that's in the source variable no longer exists.
        self.myCanvas.addtag_withtag( tagTarget, 'source1')
        print ('Adding to source {}, target tag {}'.format( 'source1', tagTarget))
        # remove the source1 tag from all objects that contain source1
        self.myCanvas.dtag('source1','source1')
        print(self.myCanvas.gettags(self._drag_data[self._mode]))
        # reset the drag information
        self.reset_drag_data()

    def _getObjectTagStartWith(self, id, startWith):
            # this is to return the tag that startWith
            # assuming looking for a tag that only one value exists
            # so returning the first string in the returned aray
            #print ('the id: {}'.format(id))
            tags = self.myCanvas.gettags(id)
            # find the tag that startsWith by find()==0
            tagName = [tg for tg in tags if tg.find(startWith)==0]
            #print ('The id and name tag are: {},{}'.format(id, tagName[0],))
            return tagName[0]

    def _setObjectTag(self, targetTag, newTag):
        # on the targetTag add the newTag
        self.myCanvas.addtag_withtag(targetTag, newTag)      
    
    def _deleteObjectTag(self, targetTag, deleteTag):
        # on the targetTag delete the deleteTag
        self.myCanvas.dtag(targetTag, deleteTag)

    def _getObjectNameTag(self, id):
            #print ('the id: {}'.format(id))
            tags = self.myCanvas.gettags(id)
            # find the Name tag.  This will identify the group of items to move.
            tagName = [tg for tg in tags if tg.find('Name')>-1]
            #print ('The id and name tag are: {},{}'.format(id, tagName[0],))
            return tagName[0]

    def get_Object(self):
        # Return either id or tagName based on mode
        return self._drag_data[self._mode]

class Pointer_mode_group(Pointer_Mode):
    def __init__(self, myCanvas):
        # call the parent
        super().__init__(myCanvas=myCanvas)
        # override properties
        self._mode = 'sourceNameTag'
        self.name = "Pointer Group"
        #point drop method to needed internal method
        self.drop = self._drop_def

class Pointer_mode_group_move(Pointer_Mode):
    def __init__(self, myCanvas):
        # call the parent
        super().__init__(myCanvas=myCanvas)
        # override properties
        self._mode = 'sourceNameTag'
        self.name = "Pointer Group Move"
        #point drop method to needed internal method
        self.drop = self._drop_move

class Pointer_mode_id(Pointer_Mode):
    def __init__(self, myCanvas):
        # call the parent
        super().__init__(myCanvas=myCanvas)
        # override properties
        self._mode = 'id'
        self.name = "Pointer Id"
        #point drop method to needed internal method
        self.drop = self._drop_def

class Pointer_mode_id_move(Pointer_Mode):
    def __init__(self, myCanvas):
        # call the parent
        super().__init__(myCanvas=myCanvas)
        # override properties
        self._mode = 'id'
        self.name = "Pointer Id Move"
        #point drop method to needed internal method
        self.drop = self._drop_move

class AppWindow():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("simple Object Display and Editor")

        # for testing using a global variable to increment each time object is created
        self.i = 0
        # using a global variable to increment each time an object element is created
        self.j = 0

        # configure layout of window
        self.window.rowconfigure(0,minsize=800, weight=1)
        self.window.columnconfigure(1, minsize=800, weight=1)

        #setting up window controls
        #canvas object to draw on
        self.myCanvas = tk.Canvas(self.window, bg="light grey")
        coord = 10, 10, 300, 300
        # container for buttons
        self.fr_buttons = tk.Frame(self.window)

        # object for setting the pointer mode
        self._pointer = Pointer_mode_group(self.myCanvas)

        # define buttons
        self.btns={}
        self.btns['create_obj']=tk.Button(self.fr_buttons, text="Create Object", command=lambda: self.create_object(canvas=self.myCanvas))
        # This button will have it's text changed based upon the value of _pointer_mode
        self.btns['Change Pointer Mode'] = tk.Button(self.fr_buttons, text= self._pointer.name.upper(), command=self.change_pointer_mode)

        self.btns['create_obj'].grid(row=0, column=0, sticky="ew", padx=5, pady=2.5)
        self.btns['Change Pointer Mode'].grid(row=1, column=0, sticky="ew", padx=5, pady=2.5)

        self.fr_buttons.grid(row=0, column=0, sticky="ns")
        self.myCanvas.grid(row=0, column=1, sticky="nsew")

        self.window.mainloop()

    def setBindings(self):
            #set bindings to objects created in canvas
            #called each time a new object is created or not.
            self.myCanvas.tag_bind("object", "<ButtonPress-1>", self._pointer.select)
            self.myCanvas.tag_bind("object", "<ButtonRelease-1>", self._pointer.drop)
            self.myCanvas.tag_bind("object", "<B1-Motion>", self._pointer.move)

    
    def drag_stop_move(self, event):
            pass

    def change_pointer_mode(self):
        if self._pointer.name == 'Pointer Group':
            self._pointer = Pointer_mode_id(self.myCanvas)
        elif self._pointer.name == 'Pointer Id':
            self._pointer = Pointer_mode_id_move(self.myCanvas)
        elif self._pointer.name == 'Pointer Id Move':
            self._pointer = Pointer_mode_group_move(self.myCanvas)
        elif self._pointer.name == 'Pointer Group Move':
            self._pointer = Pointer_mode_group(self.myCanvas)

        self.setBindings()
        self.btns['Change Pointer Mode']['text'] = self._pointer.name
        

    def create_object(self, canvas=None ):
        # create an object
        # this is for early testing
        # this will be replaced by the actual class object
        # need to draw the object

        # Grouping items by giving them the same tag
        tagName = 'Name:' + str(self.i)
        # incrementing tag for the next object to be created
        self.i = self.i + 1

        # to test first want to draw a rectangle on the canvas
        # and then draw text next to it and give them the same tag
        # default sizes
        height=200
        width=100
        x=10
        y=10
        color = "grey"
        # this is the background of the object.  It's synonymous with the object.
        canvas.create_rectangle(
                x,
                y,
                x + width,
                y + height,
                outline=color,
                fill=color,
                tags=("object",'_background',tagName),
            )
        self.setBindings()

        # create text with the same tag
        # these are items of the object so they have the Name tag and the Item tag with unique
        textValues = [tagName, 'one','two','what ever','Hello World!!']
        # is text going to be left justified or center justified
        justify = 'left'
        if justify == 'center':
            anchor = tk.N
            #get the center of the rectangle
            txtX = x + (width/2)
        elif justify == 'left':
            anchor = tk.NW
            #get the left of the rectangle with some padding
            txtX = x + 5
        for row in range (0,5,1):
            rowHeight = 15
            txtY = (rowHeight * row) + y
            #create unique item tag for this item
            tagItem = 'Item' + str(self.j)
            # increment the j counter for the next item
            self.j += 1

            # format the font of the entries 
            if row == 0:
                fnt = ('Helvetica 15 bold')
            else:
                fnt = ('Helvetica 12')
            canvas.create_text(
                txtX,
                txtY, 
                text = textValues[row],
                fill = "white",
                font = fnt,
                tags=("object",'_item',tagName, tagItem),
                anchor = anchor,
        )



if __name__ == '__main__':
    #print('Starting in __main__')
    app = AppWindow()