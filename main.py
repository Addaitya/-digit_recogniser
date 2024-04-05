import tkinter as tk
from PIL import Image
from datetime import datetime

# Here i inherited the buildin tk.Canvas and created my new canvas class
class DrawingBoard(tk.Canvas):
    def __init__(self, window, x_pos, y_pos, height, width):
        super().__init__(window, heigh=height, width=width, bg='white', borderwidth=0)
        
        # setting postion of the board on the window
        self.place(x=x_pos, y=y_pos)

        # This is height and width of the drawing board
        self.height = height
        self.width = width

        # make canvas background black 
        # This is done like this because,  earlier i was try drawingBoard(canvas) own attribute bg = 'black'
        # to make canvas black but black background was not captured by when we save drawing board image
        self.create_rectangle(0, 0, self.width+2, self.height+2, fill="black")

        # Stores the cursor postion on the drawing board
        self.pen_pos_x = None
        self.pen_pos_y = None

        self.bind("<B1-Motion>", self.draw)
        self.bind('<Motion>', self.change_pen_coordinates)
        

    def change_pen_coordinates(self, event):
        self.pen_pos_x = event.x
        self.pen_pos_y = event.y

    def draw(self, event):
        if self.pen_pos_x is not None and self.pen_pos_y is not None:
            self.create_line(self.pen_pos_x, self.pen_pos_y, event.x, event.y, width=15, fill='white', capstyle='round', smooth=True, splinesteps=12)
        self.pen_pos_x = event.x
        self.pen_pos_y = event.y
    
    def clear_board(self):
        self.pen_pos_x = None
        self.pen_pos_y = None
        self.delete('all')
        self.create_rectangle(0, 0, self.width+2, self.height+2, fill="black")



def save_image(board):
    board.postscript(file="canvas.ps", colormode="gray") 
    img = Image.open("canvas.ps")
    img = img.resize((28,28))
    name = str(datetime.now())
    img.save(f'images/{name}.png', "PNG")


if __name__ == '__main__':

    window = tk.Tk()

    window.title("Digits")
    window.geometry('800x600')
    
    # This is our drawing canvas
    board = DrawingBoard(window, 100, 100, 280, 280)


    clear_button = tk.Button(window, text='Clear', command=board.clear_board, font=("Arial", 16))
    clear_button.place(x=100, y = 400)

    # You can find saved images in folder "images/"
    save_image_button = tk.Button(window, text='Save', command=(lambda: save_image(board)), font=("Arial", 16))
    save_image_button.place(x=200, y = 400)

    window.mainloop()