import cv2 
import argparse
import os
import numpy as np
from PIL import ImageTk,Image
from tkinter import filedialog
import math
def nhap_anh(c):
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required = True,help = "Path to the image")
    args = vars(ap.parse_args(["-i",c]))
    image = cv2.imread(args["image"])
    return image

def anh_hien_thi(image):
    # sắp xếp lại thứ tự màu
    (b,g,r) = cv2.split(image)
    img = cv2.merge((r,g,b))
    img_array = Image.fromarray(img)
    img_display = ImageTk.PhotoImage(image=img_array)
    return img_display
def anh_hien_thi_split(image):
    img_array= Image.fromarray(image)
    img_display = ImageTk.PhotoImage(image=img_array)
    return img_display

def resize_image_height(image_need_resize,heigt):
        height = int(heigt)
        scale = image_need_resize.shape[0] / heigt 
        width = int(image_need_resize.shape[1] /scale )
        dim = (width, height)
        imgCv2 = cv2.resize(image_need_resize, dim, interpolation = cv2.INTER_AREA)
        imageTK = anh_hien_thi(imgCv2)
        return imageTK
def resize_image_width(image_need_resize,widt):
        width = int(widt)
        scale = image_need_resize.shape[1] / widt
        height = int(image_need_resize.shape[0] /scale )
        dim = (width, height)
        imgCv2 = cv2.resize(image_need_resize, dim, interpolation = cv2.INTER_AREA)
        imageTK = anh_hien_thi(imgCv2)
        return imageTK
def luu_anh(image):
    # file = filedialog.asksaveasfile(mode='w', defaultextension=".png", filetypes=(("PNG file", "*.png"),("All Files", "*.*") ))
    # if file:
    #     abs_path = os.path.abspath(file.name)
    #     win.img_path.save(abs_path)
    files = [('png','*.png'),('jpg','*.jpg')]
    file = filedialog.asksaveasfile(filetypes=files,mode='w',defaultextension = files)
    if file:
        abs_path = os.path.split(file.name)
        cv2.imwrite(os.path.join(abs_path[0],abs_path[1]),image)

def thay_doi_mau(image):
    print('Thay đổi màu pixcel')
    vi_tri_dau = tuple(map(int,input('nhập vị trí điểm đầu: ').split()))
    vi_tri_cuoi = tuple(map(int,input('nhập vị trí diểm cuối: ').split()))
    mau_thay_doi = tuple(map(int,input('nhập màu sắc: ').split()))
    # corner = image[vi_tri_dau[0]:vi_tri_cuoi[0], vi_tri_dau[1]:vi_tri_cuoi[1]]
    # cv2.imshow("Corner", corner)
    image[vi_tri_dau[0]:vi_tri_cuoi[0], vi_tri_dau[1]:vi_tri_cuoi[1]] = mau_thay_doi
    return image

def khung_ve():
    kich_thuoc_khung = list(map(int,input('Nhập kích thước khung: ').split()))
    canvas = np.zeros((kich_thuoc_khung[0], kich_thuoc_khung[1], 3), dtype = "uint8")
    return canvas
def line(canvas):
    print('Vẽ đường thẳng: ')
    vi_tri_bat_dau = tuple(map(int,input('nhập vị trí điểm đầu: ').split()))
    vi_tri_ket_thuc = tuple(map(int,input('nhập vị trí diểm cuối: ').split()))
    color = tuple(map(int,input('nhập màu sắc: ').split()))
    do_day = int(input('độ dày pixcel: '))
    cv2.line(canvas, vi_tri_bat_dau, vi_tri_ket_thuc, color,do_day)
def rec(canvas):
    print('Vẽ hình chữ nhật: ')
    vi_tri_bat_dau = tuple(map(int,input('nhập vị trí điểm đầu: ').split()))
    vi_tri_ket_thuc = tuple(map(int,input('nhập vị trí diểm cuối: ').split()))
    color = tuple(map(int,input('nhập màu sắc: ').split()))
    do_day = int(input('độ dày pixcel: '))
    cv2.rectangle(canvas, vi_tri_bat_dau, vi_tri_ket_thuc, color,do_day)
def circle(canvas):
    print('Vẽ đường tròn: ')
    vi_tri_tam = tuple(map(int,input('Tọa độ tâm đường tròn: ').split()))
    ban_kinh = int(input('Bán kính đường tròn: '))
    color = tuple(map(int,input('nhập màu sắc: ').split()))
    do_day = int(input('độ dày pixcel: '))
    cv2.circle(canvas, vi_tri_tam, ban_kinh, color, do_day)
    
def tach_mau(canvas):
    (B, G, R) = cv2.split(canvas)
    return B,G,R
def hien_thi_mau_blue(canvas,mau):
    zeros = np.zeros(canvas.shape[:2], dtype = "uint8")
    img_display = anh_hien_thi(cv2.merge([mau,zeros, zeros]))
    return img_display
def hien_thi_mau_green(canvas,mau):
    zeros = np.zeros(canvas.shape[:2], dtype = "uint8")
    img_display = anh_hien_thi(cv2.merge([zeros, mau, zeros]))
    return img_display
def hien_thi_mau_red(canvas,mau):
    zeros = np.zeros(canvas.shape[:2], dtype = "uint8")
    img_display = anh_hien_thi(cv2.merge([zeros, zeros, mau]))
    return img_display
def hop_nhat_mau(anh):
    merged = cv2.merge(anh)
    img_display = anh_hien_thi(merged)
    return img_display
def thay_doi_mau_pixcel(anh,d):
    for x in range(anh.shape[0]):
        for y in range(anh.shape[1]):
            anh[x][y]+=d
    return anh
def draw(image):
    drawing = False
    params=[]
    params.append(image)
    params.append(drawing)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image',draw_circle,param=params)
    
    

def draw_circle(event,x,y,flags,param):
    global ix,iy
    drawing = param[1]
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        # we take note of where that mouse was located
        ix,iy = x,y
        
    elif event == cv2.EVENT_MOUSEMOVE:
        drawing == True
        
    elif event == cv2.EVENT_LBUTTONUP:
        radius = int(math.sqrt( ((ix-x)**2)+((iy-y)**2)))
        cv2.circle(param[0],(ix,iy),radius,(255,255,255), thickness=1)
        drawing = False