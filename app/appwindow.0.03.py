# The main window for the application

# Additional abilities needed from pointer
    # ability to trigger an activity.  For example a TimeoutError
    # Maybe the objects that are created and are children can have different reactions to the double click Event
    # Send the double click event to the group if pointer is in group mode.  Then the invividual objects react based upon if they have a doubel clicked function to call or not
    # Send the double click event to the individual item if pointer is in id mode. still will only react if it has the double clicked function

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


class AppWindow():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("simple Object Display and Editor")

        # for testing using a global variable to increment each time object is created
        self.i = 0

        # for tracking the current pointer mode.  
        # values: group (default), id
        self._pointer_mode = 'group'

        # configure layout of window
        self.window.rowconfigure(0,minsize=800, weight=1)
        self.window.columnconfigure(1, minsize=800, weight=1)

        #setting up window controls
        #canvas object to draw on
        self.myCanvas = tk.Canvas(self.window, bg="white")
        coord = 10, 10, 300, 300
        # container for buttons
        self.fr_buttons = tk.Frame(self.window)

        # define buttons
        self.btns={}
        self.btns['create_obj']=tk.Button(self.fr_buttons, text="Create Object", command=lambda: self.create_object(canvas=self.myCanvas))
        self.btns['save'] = tk.Button(self.fr_buttons, text="Save As...", command=self.save_file)
        # This button will have it's text changed based upon the value of _pointer_mode
        self.btns['Change Pointer Mode'] = tk.Button(self.fr_buttons, text="Pointer " + self._pointer_mode.upper(), command=self.change_pointer_mode)

        self.btns['create_obj'].grid(row=0, column=0, sticky="ew", padx=5, pady=2.5)
        self.btns['save'].grid(row=1, column=0, sticky="ew", padx=5, pady=2.5)
        self.btns['Change Pointer Mode'].grid(row=2, column=0, sticky="ew", padx=5, pady=2.5)

        self.fr_buttons.grid(row=0, column=0, sticky="ns")
        self.myCanvas.grid(row=0, column=1, sticky="nsew")

        # this data is used to keep track of an
        # item being dragged
        # if "item" is a tag it will drag all the items with the matching tag
        self._drag_data = {"x": 0, "y": 0, "item": None}


        self.window.mainloop()

    def setBindings(self):
            #set bindings to objects created in canvas
            #called each time a new object is created or not.
            self.myCanvas.tag_bind("object", "<ButtonPress-1>", self.drag_start)
            self.myCanvas.tag_bind("object", "<ButtonRelease-1>", self.drag_stop)
            self.myCanvas.tag_bind("object", "<B1-Motion>", self.drag)

    def setBindings_move(self):
            #set bindings to objects created in canvas for the pointer_mode == move
            #called each time a new object is created or not.
            self.myCanvas.tag_bind("object", "<ButtonPress-1>", self.drag_start_move)
            self.myCanvas.tag_bind("object", "<ButtonRelease-1>", self.drag_stop_move)
            self.myCanvas.tag_bind("object", "<B1-Motion>", self.drag)


    def drag_start(self, event):
        """Begining drag of an object"""
        # record the item and its location
        # get the item
        item = self.myCanvas.find_closest(event.x, event.y)[0]

        # check self._pointer_mode 
        # if group return the name tag
        # if id return the selected item id
        # get tags for the item
        if self._pointer_mode == 'group':
            tagName = self.getObjectNameTag(item)
            # add the Name tag that was found to the drag_data
            self._drag_data["item"] = tagName
        elif self._pointer_mode == 'id':
            self._drag_data["item"] = item
        elif self._pointer_mode == 'move':
            self._drag_data["item"] = item

        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def drag_start_move(self, event):
        """Begining drag of an object"""
        # record the item and its location
        # get the item
        item = self.myCanvas.find_closest(event.x, event.y)[0]

        #raise it to the topmost in the canvas
        self.myCanvas.tag_raise(item, 'all')
        
        # check self._pointer_mode 
        # if group return the name tag
        # if id return the selected item id
        # get tags for the item
        if self._pointer_mode == 'group':
            tagName = self.getObjectNameTag(item)
            # add the Name tag that was found to the drag_data
            self._drag_data["item"] = tagName
        elif self._pointer_mode == 'id':
            self._drag_data["item"] = item
        elif self._pointer_mode == 'move':
            self._drag_data["item"] = item

        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y


    def drag_stop(self, event):
        """End drag of an object"""
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def drag_stop_move(self, event):
        """End drag of an object"""
        print('Ending move and dropping')
        source = self._drag_data['item']
        # find object at location of the drop
        #target = self.myCanvas.find_closest(event.x, event.y)[1]
        
        # find object below the moved item
        # returns the item below in the order, not in relation to where it is on the canvas
        #target = self.myCanvas.find_below(self._drag_data['item'])

        # get the item that intersects with the bounding box of the dragged item
        bboxSource = self.myCanvas.bbox(source)
        print (bboxSource)
        x1,y1,x2,y2 = bboxSource
        # The dragging object, source has been moved to the front on drag stop
        # that means the target will always be below it. [0] will be the bottom of the overlapping objects returned
        target = self.myCanvas.find_overlapping(x1,y1,x2,y2)[0]

        print ('Drop x,y: {},{}'.format(event.x, event.y))
        print ('Target item: {}'.format(target,))

        # get it's tag name
        tagTarget = self.getObjectNameTag(target)
        print ('Target tag: {}'.format(tagTarget,))

        # change the tag name that's in the _drag_data item 
        # assuming that pointer mode is id
        # delete the original Name tag for the source object, the one dragged
        self.myCanvas.dtag(source,self.getObjectNameTag(source))
        # add the new Name tag to the source object to group it with the object dropped on
        self.myCanvas.addtag_withtag( tagTarget, self._drag_data["item"])
        print(self.myCanvas.gettags(self._drag_data["item"]))
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0



    def drag(self, event):
        """Handle dragging of an object"""
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        self.myCanvas.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def change_pointer_mode(self):
        if self._pointer_mode == 'group':
            self._pointer_mode = 'id'
            self.setBindings()
        elif self._pointer_mode == 'id':
            self._pointer_mode = 'move'
            self.setBindings_move()
        elif self._pointer_mode == 'move':
            self._pointer_mode = 'group'
            self.setBindings()

        self.btns['Change Pointer Mode']['text'] = "Pointer " + self._pointer_mode.upper()
        

    def getObjectNameTag(self, id):
            tags = self.myCanvas.gettags(id)
            # find the Name tag.  This will identify the group of items to move.
            tagName = [tg for tg in tags if tg.find('Name')>-1]
            print ('The id and name tag are: {},{}'.format(id, tagName[0],))
            return tagName[0]


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
        canvas.create_rectangle(
                x,
                y,
                x + width,
                y + height,
                outline=color,
                fill=color,
                tags=("object",tagName),
            )
        self.setBindings()

        # create text with the same tag
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
                tags=("object",tagName),
                anchor = anchor,
        )


    def save_file(self):
        msg = 'Stub save_file'
        tk.messagebox.showinfo(title=msg, message=msg)



if __name__ == '__main__':
    #print('Starting in __main__')
    app = AppWindow()