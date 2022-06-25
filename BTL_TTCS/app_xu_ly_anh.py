from copy import copy
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from tkinter.messagebox import WARNING, askokcancel, showinfo, showwarning
from process_image import *
from PIL import ImageGrab,Image,ImageDraw

class MyApp(Tk):
    def __init__(self):
        super().__init__()
        #use vista theme
        self.style = ttk.Style(self)
        self.style.theme_use('vista')
        #khởi tạo cửa sổ app
        self.title('Xử lý ảnh')
        self.size_main_frame_and_size_grip()
        self['bg'] = 'white'
        #khởi tạo menu
        self.create_menu()
        #khởi tạo hình ảnh
        self.image = None
        self.img_imageTk = None
        self.img_cv2 = None
        self.img_cv2_b = None
        self.img_cv2_b_edit = None
        self.img_cv2_g = None
        self.img_cv2_g_edit = None
        self.img_cv2_r = None
        self.img_cv2_r_edit =  None
        self.frame_split = None
        self.change = False
        self.merge = None
        #khởi tạo các frame
        self.creat_frame_menu()
        self.create_frame_image()
    def size_main_frame_and_size_grip(self):
        window_width = 1080
        window_height = 1080
        
        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        
        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        #Cho phép thay đổi kích cỡ
        self.resizable(True, True)
        #định cấu hình bố cục lưới
        self.columnconfigure(0, weight=1)
        
        self.rowconfigure(0, weight=1,minsize=100)
        self.rowconfigure(1,weight=10)
        # tạo sizegrip đê thay đổi kích cỡ
        sg = ttk.Sizegrip(self)
        sg.grid(row=2, sticky=tk.SE)
        # gans frame vaof grid
        self.style.configure('main.TFrame', background='white')
        self.main_frame_1 = ttk.Frame(self,style='main.TFrame',height=100)
        self.main_frame_1.grid(column=0,row=0, sticky="nwes")
        self.style.configure('main1.TFrame', background='white')
        self.main_frame_2 = ttk.Frame(self,style='main1.TFrame',height=980)
        self.main_frame_2.grid(column=0,row=1, sticky="nwes")
        
    def create_menu(self):
        #tạo menu chức năng
        menu_bar = Menu(self)
        self.config(menu=menu_bar)
        #File menu
        menu_file = Menu(menu_bar,tearoff=0)
        menu_file.add_command(label = 'Open Image',command=self.click_open_image)
        menu_file.add_command(label = 'Save image',command=self.click_save_image)
        menu_file.add_separator()
        menu_file.add_command(label = 'Exit',command= self.destroy)
        menu_bar.add_cascade(menu=menu_file, label="File")
        #Edit menu
        menu_edit = Menu(menu_bar,tearoff=0)
        menu_edit.add_command(label='Split and Merge Image',command=self.click_menu_split)
        # menu_edit.add_command(label='Merge Image',command=self.click_merge)
        menu_bar.add_cascade(label='Edit',menu=menu_edit)
        #About menu
        menu_about = Menu(menu_bar,tearoff=0)
        menu_about.add_command(label='About...')
        menu_bar.add_cascade(label="Help",menu=menu_about)
        
    def create_frame_image(self):
        #tạo frame chứa image
        self.main_frame_2.columnconfigure(0, weight=1)
        self.main_frame_2.rowconfigure(0, weight=1)
        self.frame_image = ttk.Frame(self.main_frame_2,height=880)
        self.frame_image.grid(column=0,row=0, sticky="nwes")
        #tạo canvas image và các thanh cuộn
        width = 600
        height = 880
        if self.img_imageTk != None:
            width = self.img_imageTk.width()
            height = self.img_imageTk.height()
            self.canvas = Canvas(self.frame_image,width=660,height=660,scrollregion=(0,0,width,height))
            self.container_image=self.canvas.create_image(0,0,anchor=NW,image=self.img_imageTk)
            self.scroll_x = ttk.Scrollbar(self.frame_image, orient="horizontal", command=self.canvas.xview)
            self.scroll_x.pack(fill='x',side='bottom')
            self.scroll_y = ttk.Scrollbar(self.frame_image, orient='vertical', command=self.canvas.yview)
            self.scroll_y.pack(side='right',fill='y')
            self.canvas.config(width=600,height=600)
            self.canvas.config(xscrollcommand=self.scroll_x.set,yscrollcommand=self.scroll_y.set)
            self.canvas.pack(fill='both',side='top')
            self.canvas.old_coords = None
    def update_canvas(self):
        if self.img_imageTk != None:
            self.create_frame_image()
            width = self.img_imageTk.width()
            height = self.img_imageTk.height()
            self.canvas.itemconfig(self.container_image,image=self.img_imageTk)
            self.canvas.configure(scrollregion=(0,0,width,height),width=self.img_imageTk.width(),height=self.img_imageTk.height())
    def creat_frame_split(self):
        self.frame_image.grid_forget()
        self.style.configure('split.TFrame', background='pink')
        self.frame_split = ttk.Frame(self.main_frame_2,style='split.TFrame',height=880)
        self.main_frame_2.columnconfigure(0, weight=1)
        self.main_frame_2.rowconfigure(0, weight=1)
        self.frame_split.grid(column=0,row=0, sticky="nwes")
        self.frame_split.columnconfigure(0, weight=1,minsize=self.main_frame_2.winfo_width()/2)
        self.frame_split.columnconfigure(1, weight=1,minsize=self.main_frame_2.winfo_width()/2)
        self.frame_split.rowconfigure(0, weight=1,minsize=self.main_frame_2.winfo_height()/2)
        self.frame_split.rowconfigure(1, weight=1,minsize=self.main_frame_2.winfo_height()/2)
        self.style.configure('split_1.TFrame', background='white')
        self.frame_split_1 = ttk.Frame(self.frame_split,style='split_1.TFrame',width=self.main_frame_2.winfo_width()/2)
        self.style.configure('split_2.TFrame', background='white')
        self.frame_split_2 = ttk.Frame(self.frame_split,style='split_2.TFrame',width=self.main_frame_2.winfo_width()/2)
        self.style.configure('split_3.TFrame', background='white')
        self.frame_split_3 = ttk.Frame(self.frame_split,style='split_3.TFrame',width=self.main_frame_2.winfo_width()/2)
        self.style.configure('split_4.TFrame', background='white')
        self.frame_split_4 = ttk.Frame(self.frame_split,style='split_4.TFrame',width=self.main_frame_2.winfo_width()/2)
        self.frame_split_1.grid(column=0,row=0, sticky="nwes")
        self.frame_split_2.grid(column=1,row=0, sticky="nwes")
        self.frame_split_3.grid(column=0,row=1, sticky="nwes")
        self.frame_split_4.grid(column=1,row=1, sticky="nwes")
        
        #+++++++++++++++++++++split_frame_1++++++++++++++++++++++#
        self.frame_split_1.columnconfigure(0, weight=5)
        self.frame_split_1.columnconfigure(1, weight=1,minsize=80)
        #---------------------frame canvas image-----------------#
        self.frame_split_1_canvas = ttk.Frame(self.frame_split_1)
        self.frame_split_1_canvas.grid(column=0,row=0,sticky="nwes")
       
        self.style.configure('TLabel', width = 200)
        lb_1 = ttk.Label(self.frame_split_1_canvas,text= "Ảnh gốc",anchor='center',style='TLabel')
        lb_1.pack(side='top')
        
        # create canvas image
        width = self.main_frame_2.winfo_width()//2-80
        height = self.main_frame_2.winfo_height()//2-50
        # if self.img_cv2_b != None:
        self.frame_split_1.columnconfigure(0,minsize=width)
        
        width_image = self.img_imageTk.width()
        height_image = self.img_imageTk.height()
        #anh hien thi
        self.canvas_split_1 = Canvas(self.frame_split_1_canvas,width=width,height=height,scrollregion=(0,0,width_image,height_image))
        self.container_image_split_1=self.canvas_split_1.create_image(0,0,anchor=NW,image= self.img_imageTk)
        self.scroll_x_split_1 = ttk.Scrollbar(self.frame_split_1_canvas, orient="horizontal", command=self.canvas_split_1.xview)
        self.scroll_x_split_1.pack(fill='x',side='bottom')
        self.scroll_y_split_1= ttk.Scrollbar(self.frame_split_1_canvas, orient='vertical', command=self.canvas_split_1.yview)
        self.scroll_y_split_1.pack(side='right',fill='y')
        self.canvas_split_1.config(width=width,height=height)
        self.canvas_split_1.config(xscrollcommand=self.scroll_x_split_1.set,yscrollcommand=self.scroll_y_split_1.set)
        self.canvas_split_1.pack(fill='both',side='top')
        #----------------frame action------------------#
        self.frame_action_1 = ttk.Frame(self.frame_split_1)
        self.frame_action_1.grid(column=1,row=0,sticky="nwes")
        #button
        self.btn_pencil = ttk.Button(self.frame_action_1,text='expand',cursor='hand2',command=self.click_expand_1)
        self.btn_pencil.pack(fill='both',side='top',expand=True)
        self.btn_pencil = ttk.Button(self.frame_action_1,text='Split image',cursor='hand2',command=self.click_split)
        self.btn_pencil.pack(fill='both',side='top',expand=True)
        self.btn_pencil = ttk.Button(self.frame_action_1,text='Change',cursor='hand2',command=self.click_change)
        self.btn_pencil.pack(fill='both',side='top',expand=True)
        self.btn_pencil = ttk.Button(self.frame_action_1,text='Merge',cursor='hand2',command=self.click_merge)
        self.btn_pencil.pack(fill='both',side='top',expand=True)
        #-----------------------------------------------#
        
    
    def creat_frame_menu(self):
        # Create style for the first frame
        self.style.configure('Frame_menu.TFrame', background='#F7F3F3')
        # Use created style in this frame
        self.frame_menu = ttk.Frame(self.main_frame_1, style='Frame_menu.TFrame')

        self.frame_menu.pack(fill='both',side='top',expand=True)
        self.paint = False
        self.delete_panit = False
        self.set_size_pen = IntVar()
        self.set_size_pen.set(1)
        self.color_draws = 'black'
        # create button draw
        ico_pen = PhotoImage(file='icon\pencil.png')
        self.btn_pencil = ttk.Button(self.frame_menu,image=ico_pen,text='hi',cursor='hand2',command=self.click_btn_draw)
        self.btn_pencil.image = ico_pen
        self.btn_pencil.pack(ipadx=5,ipady=5,side='left')
        #create button eraser
        self.btn_cut = self.creat_button_menu('icon\eraser.png',self.click_btn_delete,side='left')
        
        #đường phân cách
        separator = ttk.Separator(self.frame_menu, orient='vertical')
        separator.pack(fill='y',side='left')
        # bảng màu vẽ + sesize pen
        self.btn_color_chooser = self.creat_button_menu('icon\color_chooser.png',self.click_btn_color_chooser,side='left')
        self.btn_color_chooser = self.creat_button_menu('icon\size_pen.png',self.New_Window_pen_size,side='left')
        
        separator = ttk.Separator(self.main_frame_1, orient='horizontal')
        separator.pack(fill='x',side='bottom')
        
        
    def create_circle(self,x, y, r, canvasName,color): #center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return canvasName.create_oval(x0, y0, x1, y1,fill=color)

    def creat_button_menu(self,ico_path,click,side):
        ico_pen = PhotoImage(file=ico_path)
        btn = ttk.Button(self.frame_menu,image=ico_pen,command=click,text='hi',cursor='hand2')
        btn.image = ico_pen
        btn.pack(ipadx=5,ipady=5,side=side)
    def make_label(self,frame,img):
        label = Label(frame,image= img)
        label.image = img
        label.pack(fill = "both")
    def click_open_image(self):
        
        # win.frame_image.pack_propagate(0)
        # win.frame_image.pack()
        file_path = filedialog.askopenfilename(filetypes=(('jpg','*.jpg'),('png','*.png')))
        print(f'gia tri: {file_path} {type(file_path)}')
        if self.frame_split != None:
            self.frame_split.grid_forget()
            self.frame_image.grid(column=0,row=0,sticky="nwes")
            self.img_cv2_b=self.img_cv2_g=self.img_cv2_r=self.img_cv2_b_edit=self.img_cv2_g_edit=self.img_cv2_r_edit=None
            self.merge=None
        if(file_path!=''):
            # win.img_path = Image.open(file_path)
            image = nhap_anh(file_path)
            self.img_cv2 = image
            img = anh_hien_thi(image)
            self.img_imageTk = img
            self.image = ImageTk.getimage(self.img_imageTk)
            self.update_canvas()

            # scroll_x.grid(row=1, column=0, sticky="ew")
    def click_save_image(self):
        self.img_imageTk = ImageTk.PhotoImage(self.image)
        # self.update_canvas()

        a = ImageTk.getimage(self.img_imageTk )
        a.save('a.png')
        
        self.img_cv2 = nhap_anh('a.png')
        self.img_imageTk = anh_hien_thi(self.img_cv2)
        self.image = ImageTk.getimage(self.img_imageTk)
        self.update_canvas()
    def save_image_merge(self):
        a = ImageTk.getimage(self.merge)
        a.save('merge.png')
        b = hien_thi_mau_blue(self.img_cv2,self.img_cv2_b_edit)
        b = ImageTk.getimage(b)
        b.save('b.png')
        g = hien_thi_mau_green(self.img_cv2,self.img_cv2_g_edit)
        g = ImageTk.getimage(g)
        g.save('g.png')
        r = hien_thi_mau_red(self.img_cv2,self.img_cv2_r_edit)
        r = ImageTk.getimage(r)
        r.save('r.png')
        
    def click_menu_split(self):
        try:
            if self.img_cv2==None:
                showwarning(
                    title='Warning',
                    message='Vui lòng nhập ảnh')
        except:
            self.creat_frame_split()
    def click_split(self):
        #Tách màu
        b,g,r=tach_mau(self.img_cv2)
        self.img_cv2_b=b
        self.img_cv2_g=g
        self.img_cv2_r=r
        self.img_cv2_b_edit=self.img_cv2_b.copy()
        self.img_cv2_g_edit=self.img_cv2_g.copy()
        self.img_cv2_r_edit=self.img_cv2_r.copy()
        
        #+++++++++++++++++++++split_frame_2++++++++++++++++++++++#
        self.frame_split_2.columnconfigure(0, weight=5)
        self.frame_split_2.columnconfigure(1, weight=1,minsize=50)
        #---------------------frame canvas image-----------------#
        self.frame_split_2_canvas = ttk.Frame(self.frame_split_2)
        self.frame_split_2_canvas.grid(column=0,row=0,sticky="nwes")
       
        self.style.configure('TLabel', width = 200)
        lb_2 = ttk.Label(self.frame_split_2_canvas,text= "Ảnh tách xanh dương",anchor='center',style='TLabel')
        lb_2.pack(side='top')
        
        # create canvas image
        width = self.main_frame_2.winfo_width()//2-80
        height = self.main_frame_2.winfo_height()//2-50
        # if self.img_cv2_b != None:
        self.frame_split_2.columnconfigure(0,minsize=width)
        
        width_image = self.img_imageTk.width()
        height_image = self.img_imageTk.height()
        #anh hien thi
        self.canvas_split_2 = Canvas(self.frame_split_2_canvas,width=width,height=height,scrollregion=(0,0,width_image,height_image))
        self.b = anh_hien_thi_split(self.img_cv2_b)
        self.container_image_split_2=self.canvas_split_2.create_image(0,0,anchor=NW,image= self.b,tag = ("abc"))
        self.scroll_x_split_2 = ttk.Scrollbar(self.frame_split_2_canvas, orient="horizontal", command=self.canvas_split_2.xview)
        self.scroll_x_split_2.pack(fill='x',side='bottom')
        self.scroll_y_split_2 = ttk.Scrollbar(self.frame_split_2_canvas, orient='vertical', command=self.canvas_split_2.yview)
        self.scroll_y_split_2.pack(side='right',fill='y')
        self.canvas_split_2.config(width=width,height=height)
        self.canvas_split_2.config(xscrollcommand=self.scroll_x_split_2.set,yscrollcommand=self.scroll_y_split_2.set)
        self.canvas_split_2.pack(fill='both',side='top')
        #----------------frame action------------------#
        self.frame_action_2 = ttk.Frame(self.frame_split_2)
        self.frame_action_2.grid(column=1,row=0,sticky="nwes")
        #button expand
        self.btn_pencil_2 = ttk.Button(self.frame_action_2,text='expand',cursor='hand2',command=self.click_expand_2)
        self.btn_pencil_2.pack(fill='x',side='top')
        #button reset
        self.btn_pencil_2 = ttk.Button(self.frame_action_2,text='reset',cursor='hand2',command=self.click_reset_2)
        self.btn_pencil_2.pack(fill='x',side='top')
        #slider image
        self.current_value_2 = tk.IntVar()
        self.current_value_2.set(0)
        slider = ttk.Scale(
            self.frame_action_2,
            from_=-255,
            to=255,
            orient='vertical',  # vertical
            command=self.slider_changed_2,
            variable=self.current_value_2
        )
        print(self.current_value_2.get())
        self.value_label_2 = ttk.Label(self.frame_action_2,text=str(self.current_value_2.get()))

        slider.pack(fill='y',side='top',expand=True)
        self.value_label_2.pack(fill="x",anchor='center',side='top')
        self.btn_pencil_2 = ttk.Button(self.frame_action_2,text='Edit',cursor='hand2',command=self.click_change_pixcel_2)
        self.btn_pencil_2.pack(fill='x',side='top')
        #-----------------------------------------------#
        
        #+++++++++++++++++++++split_frame_3++++++++++++++++++++++#
        self.frame_split_3.columnconfigure(0, weight=5)
        self.frame_split_3.columnconfigure(1, weight=1,minsize=80)
        #---------------------frame canvas image-----------------#
        self.frame_split_3_canvas = ttk.Frame(self.frame_split_3)
        self.frame_split_3_canvas.grid(column=0,row=0,sticky="nwes")
       
        self.style.configure('TLabel', width = 200)
        lb_3 = ttk.Label(self.frame_split_3_canvas,text= "Ảnh tách đỏ",anchor='center',style='TLabel')
        lb_3.pack(side='top')
        
        # create canvas image
        width = self.main_frame_2.winfo_width()//2-80
        height = self.main_frame_2.winfo_height()//2-50
        # if self.img_cv2_b != None:
        self.frame_split_3.columnconfigure(0,minsize=width)
        
        width_image = self.img_imageTk.width()
        height_image = self.img_imageTk.height()
        #anh hien thi
        self.canvas_split_3 = Canvas(self.frame_split_3_canvas,width=width,height=height,scrollregion=(0,0,width_image,height_image))
        self.r = anh_hien_thi_split(self.img_cv2_r)
        self.container_image_split_3=self.canvas_split_3.create_image(0,0,anchor=NW,image= self.r)
        self.scroll_x_split_3 = ttk.Scrollbar(self.frame_split_3_canvas, orient="horizontal", command=self.canvas_split_3.xview)
        self.scroll_x_split_3.pack(fill='x',side='bottom')
        self.scroll_y_split_3 = ttk.Scrollbar(self.frame_split_3_canvas, orient='vertical', command=self.canvas_split_3.yview)
        self.scroll_y_split_3.pack(side='right',fill='y')
        self.canvas_split_3.config(width=width,height=height)
        self.canvas_split_3.config(xscrollcommand=self.scroll_x_split_3.set,yscrollcommand=self.scroll_y_split_3.set)
        self.canvas_split_3.pack(fill='both',side='top')
        #----------------frame action------------------#
        self.frame_action_3 = ttk.Frame(self.frame_split_3)
        self.frame_action_3.grid(column=1,row=0,sticky="nwes")
        #button expand
        self.btn_pencil_3 = ttk.Button(self.frame_action_3,text='expand',cursor='hand2',command=self.click_expand_3)
        self.btn_pencil_3.pack(fill='x',side='top')
        #button reset
        self.btn_pencil_3 = ttk.Button(self.frame_action_3,text='reset',cursor='hand2',command=self.click_reset_3)
        self.btn_pencil_3.pack(fill='x',side='top')
        #slider image
        self.current_value_3 = tk.IntVar()
        self.current_value_3.set(0)
        slider = ttk.Scale(
            self.frame_action_3,
            from_=-255,
            to=255,
            orient='vertical',  # vertical
            command=self.slider_changed_3,
            variable=self.current_value_3
        )
        print(self.current_value_3.get())
        self.value_label_3 = ttk.Label(self.frame_action_3,text=str(self.current_value_3.get()))

        slider.pack(fill='y',side='top',expand=True)
        self.value_label_3.pack(fill="x",anchor='center',side='top')
        self.btn_penci_3 = ttk.Button(self.frame_action_3,text='Edit',cursor='hand2',command=self.click_change_pixcel_3)
        self.btn_penci_3.pack(fill='x',side='top')
        #-----------------------------------------------#
        
        #+++++++++++++++++++++split_frame_4++++++++++++++++++++++#
        self.frame_split_4.columnconfigure(0, weight=5)
        self.frame_split_4.columnconfigure(1, weight=1,minsize=50)
        #---------------------frame canvas image-----------------#
        self.frame_split_4_canvas = ttk.Frame(self.frame_split_4)
        self.frame_split_4_canvas.grid(column=0,row=0,sticky="nwes")
       
        self.style.configure('TLabel', width = 200)
        lb_4 = ttk.Label(self.frame_split_4_canvas,text= "Ảnh tách xanh lá",anchor='center',style='TLabel')
        lb_4.pack(side='top')
        
        # create canvas image
        width = self.main_frame_2.winfo_width()//2-80
        height = self.main_frame_2.winfo_height()//2-50
        # if self.img_cv2_b != None:
        self.frame_split_4.columnconfigure(0,minsize=width)
        
        width_image = self.img_imageTk.width()
        height_image = self.img_imageTk.height()
        #anh hien thi
        self.canvas_split_4 = Canvas(self.frame_split_4_canvas,width=width,height=height,scrollregion=(0,0,width_image,height_image))
        self.g = anh_hien_thi_split(self.img_cv2_g)
        self.container_image_split_4=self.canvas_split_4.create_image(0,0,anchor=NW,image= self.g,tag = ("abc"))
        self.scroll_x_split_4 = ttk.Scrollbar(self.frame_split_4_canvas, orient="horizontal", command=self.canvas_split_4.xview)
        self.scroll_x_split_4.pack(fill='x',side='bottom')
        self.scroll_y_split_4 = ttk.Scrollbar(self.frame_split_4_canvas, orient='vertical', command=self.canvas_split_4.yview)
        self.scroll_y_split_4.pack(side='right',fill='y')
        self.canvas_split_4.config(width=width,height=height)
        self.canvas_split_4.config(xscrollcommand=self.scroll_x_split_4.set,yscrollcommand=self.scroll_y_split_4.set)
        self.canvas_split_4.pack(fill='both',side='top')
        #----------------frame action------------------#
        self.frame_action_4 = ttk.Frame(self.frame_split_4)
        self.frame_action_4.grid(column=1,row=0,sticky="nwes")
        #button expand
        self.btn_pencil_4 = ttk.Button(self.frame_action_4,text='expand',cursor='hand2',command=self.click_expand_4)
        self.btn_pencil_4.pack(fill='x',side='top')
        #button reset
        self.btn_pencil_4 = ttk.Button(self.frame_action_4,text='reset',cursor='hand2',command=self.click_reset_4)
        self.btn_pencil_4.pack(fill='x',side='top')
        #slider image
        self.current_value_4 = tk.IntVar()
        self.current_value_4.set(0)
        slider = ttk.Scale(
            self.frame_action_4,
            from_=-255,
            to=255,
            orient='vertical',  # vertical
            command=self.slider_changed_4,
            variable=self.current_value_4
        )
        print(self.current_value_4.get())
        self.value_label_4 = ttk.Label(self.frame_action_4,text=str(self.current_value_4.get()))

        slider.pack(fill='y',side='top',expand=True)
        self.value_label_4.pack(fill="x",anchor='center',side='top')
        self.btn_pencil_4 = ttk.Button(self.frame_action_4,text='Edit',cursor='hand2',command=self.click_change_pixcel_4)
        self.btn_pencil_4.pack(fill='x',side='top')
        #-----------------------------------------------#
    def click_reset_2(self):
        self.img_cv2_b_edit=self.img_cv2_b.copy()
        self.b = anh_hien_thi_split(self.img_cv2_b_edit)
        self.canvas_split_2.itemconfig(self.container_image_split_2,image= self.b)
        self.current_value_2.set(0)
    def click_reset_3(self):
        self.img_cv2_r_edit=self.img_cv2_r.copy()
        self.r = anh_hien_thi_split(self.img_cv2_r_edit)
        self.canvas_split_3.itemconfig(self.container_image_split_3,image= self.r)
        self.current_value_3.set(0)
    def click_reset_4(self):
        self.img_cv2_g_edit=self.img_cv2_g.copy()
        self.g = anh_hien_thi_split(self.img_cv2_g_edit)
        self.canvas_split_4.itemconfig(self.container_image_split_4,image= self.g)
        self.current_value_4.set(0)
    def slider_changed_2(self,event):
        self.value_label_2.configure(text=str(self.current_value_2.get()))
    def slider_changed_3(self,event):
        self.value_label_3.configure(text=str(self.current_value_3.get()))
    def slider_changed_4(self,event):
        self.value_label_4.configure(text=str(self.current_value_4.get()))
    
    def click_change_pixcel_2(self):
        self.img_cv2_b_edit=self.img_cv2_b.copy()
        self.img_cv2_b_edit = thay_doi_mau_pixcel(self.img_cv2_b_edit,self.current_value_2.get())
        if self.change:
            self.b = hien_thi_mau_blue(self.img_cv2,self.img_cv2_b_edit)
            self.canvas_split_2.itemconfig(self.container_image_split_2,image= self.b)
        else:
            self.b = anh_hien_thi_split(self.img_cv2_b_edit)
            self.canvas_split_2.itemconfig(self.container_image_split_2,image= self.b)
    def click_change_pixcel_3(self):
        self.img_cv2_r_edit=self.img_cv2_r.copy()
        self.img_cv2_r_edit = thay_doi_mau_pixcel(self.img_cv2_r_edit,self.current_value_3.get())
        if self.change:
            self.r = hien_thi_mau_red(self.img_cv2,self.img_cv2_r_edit)
            self.canvas_split_3.itemconfig(self.container_image_split_3,image= self.r)
        else:
            self.r = anh_hien_thi_split(self.img_cv2_r_edit)
            self.canvas_split_3.itemconfig(self.container_image_split_3,image= self.r)
    def click_change_pixcel_4(self):
        self.img_cv2_g_edit=self.img_cv2_g.copy()
        self.img_cv2_g_edit = thay_doi_mau_pixcel(self.img_cv2_g_edit,self.current_value_4.get())
        if self.change:
            self.g = hien_thi_mau_green(self.img_cv2,self.img_cv2_g_edit)
            self.canvas_split_4.itemconfig(self.container_image_split_4,image= self.g)
        else:
            self.g = anh_hien_thi_split(self.img_cv2_g_edit)
            self.canvas_split_4.itemconfig(self.container_image_split_4,image= self.g)
            
    def click_expand_1(self):
        self.image_display = anh_hien_thi(self.img_cv2)
        self.New_Window(self.image_display)
    def click_expand_2(self):
        if self.change:
            self.image_display = hien_thi_mau_blue(self.img_cv2,self.img_cv2_b_edit)
            self.New_Window(self.image_display)
        else:
            self.image_display = anh_hien_thi_split(self.img_cv2_b_edit)
            self.New_Window(self.image_display)
    def click_expand_3(self):
        if self.change:
            self.image_display = hien_thi_mau_red(self.img_cv2,self.img_cv2_r_edit)
            self.New_Window(self.image_display)
        else:
            self.image_display = anh_hien_thi_split(self.img_cv2_r_edit)
            self.New_Window(self.image_display)
    def click_expand_4(self):
        if self.change:
            self.image_display = hien_thi_mau_green(self.img_cv2,self.img_cv2_g_edit)
            self.New_Window(self.image_display)
        else:
            self.image_display = anh_hien_thi_split(self.img_cv2_g_edit)
            self.New_Window(self.image_display)
    def click_merge(self):
        self.check_merge = True
        self.merge = hop_nhat_mau([self.img_cv2_b_edit,self.img_cv2_g_edit,self.img_cv2_r_edit])
        print(type(self.merge),type(self.img_cv2))
        self.New_Window(self.merge)
        # hop_nhat_mau([self.img_cv2_b_edit,self.img_cv2_g_edit,self.img_cv2_r_edit])
    def New_Window(self,image):
        self.win = tk.Toplevel()
        window_width = 1080
        window_height = 1080
        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        
        # set the position of the window to the center of the screen
        self.win.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        if image == self.merge:
            self.win.button = ttk.Button(self.win,text='save',command=self.save_image_merge)
            self.win.button.pack(side='top',fill='x')
        self.win.canvas = Canvas(self.win,width=1080,height=1080)
        self.win.canvas.create_image(0,0,anchor=NW,image= image)
        self.win.canvas.pack(side='top')
    def New_Window_pen_size(self):
        self.win1 = tk.Toplevel()
        self.win1.title("Chọn kích thước")
        window_width = 300
        window_height = 90
        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        
        # set the position of the window to the center of the screen
        self.win1.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        lab = ttk.Label(self.win1,text="vui lòng nhập kích thước(pixcel):")
        lab.pack(side='top',fill='both')
        self.current_val = IntVar()
        self.current_val.set(1)
        spin_box = ttk.Spinbox(
            self.win1,
            from_= 1,
            to=20,
            textvariable=self.current_val,
            wrap=True)
        spin_box.pack(side='top',fill='both')
        self.but = ttk.Button(self.win1,text='OK',command=self.click_set_size)
        self.but.pack(side='left',fill='both')
        self.but = ttk.Button(self.win1,text='Cancel',command=self.click_close_win)
        self.but.pack(side='right',fill='both')
    def click_set_size(self):
        self.set_size_pen = self.current_val
        self.win1.destroy()
    def click_close_win(self):
        self.win1.destroy()
    def cut(self):
        pass
    def click_change(self):
        self.change = not self.change
        if self.change:
            self.r = hien_thi_mau_red(self.img_cv2,self.img_cv2_r_edit)
            self.canvas_split_3.itemconfig(self.container_image_split_3,image= self.r)
            self.b = hien_thi_mau_blue(self.img_cv2,self.img_cv2_b_edit)
            self.canvas_split_2.itemconfig(self.container_image_split_2,image= self.b)
            self.g = hien_thi_mau_green(self.img_cv2,self.img_cv2_g_edit)
            self.canvas_split_4.itemconfig(self.container_image_split_4,image= self.g)
        else:
            self.r = anh_hien_thi_split(self.img_cv2_r_edit)
            self.canvas_split_3.itemconfig(self.container_image_split_3,image= self.r)
            self.b = anh_hien_thi_split(self.img_cv2_b_edit)
            self.canvas_split_2.itemconfig(self.container_image_split_2,image= self.b)
            self.g = anh_hien_thi_split(self.img_cv2_g_edit)
            self.canvas_split_4.itemconfig(self.container_image_split_4,image= self.g)
    def click_btn_draw(self):
        
        self.draw = ImageDraw.Draw(self.image)
        self.paint = not self.paint
        if self.paint:
            self.canvas.bind("<B1-Motion>",self.draws)
            self.canvas.bind('<ButtonRelease>',self.release)
        else:
            self.canvas.unbind("<B1-Motion>")
        print(self.paint)
    def draws(self,event):
        x, y = event.x, event.y
        if self.canvas.old_coords:
            x1, y1 = self.canvas.old_coords
            self.canvas.create_line(x, y, x1, y1,fill=self.color_draws,width=self.set_size_pen.get())
            self.draw.line([x, y, x1, y1], fill=self.color_draws,width=self.set_size_pen.get())
        self.canvas.old_coords = x, y
    def release(self,event):
        self.canvas.old_coords = None
        self.paint = False
        self.delete_panit = False
    def click_btn_delete(self):
        
        self.draw = ImageDraw.Draw(self.image)
        self.delete_panit = not self.delete_panit
        if self.delete_panit:
            self.canvas.bind("<B1-Motion>",self.delete)
            self.canvas.bind('<ButtonRelease>',self.release)
        else:
            self.canvas.unbind("<B1-Motion>")
        print(self.delete_panit)
    def delete(self,event):
        x, y = event.x, event.y
        if self.canvas.old_coords:
            x1, y1 = self.canvas.old_coords
            self.canvas.create_line(x, y, x1, y1,fill="white",width=self.set_size_pen.get())
            self.draw.line([x, y, x1, y1], fill="white",width=self.set_size_pen.get())
        self.canvas.old_coords = x, y
    def click_btn_color_chooser(self):
        colors = askcolor(title="Tkinter Color Chooser")
        self.color_draws = colors[1]
    
if __name__ == "__main__":
    win = MyApp()
    win.mainloop()
