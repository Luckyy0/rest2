import cv2 
import argparse
import numpy as np

def nhap_anh():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required = True,help = "Path to the image")
    args = vars(ap.parse_args(["-i",input('Nhập đường dẫn ảnh:')]))
    image = cv2.imread(args["image"])
    return image

def hien_thi_anh(image):
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    
def luu_anh(image):
    cv2.imwrite("newimage.jpg", image)

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
    cv2.imshow("color",cv2.merge([mau, zeros, zeros]))
    cv2.waitKey(0)
def hien_thi_mau_green(canvas,mau):
    zeros = np.zeros(canvas.shape[:2], dtype = "uint8")
    cv2.imshow("color",cv2.merge([zeros, mau, zeros]))
    cv2.waitKey(0)
def hien_thi_mau_red(canvas,mau):
    zeros = np.zeros(canvas.shape[:2], dtype = "uint8")
    cv2.imshow("color",cv2.merge([zeros, zeros, mau]))
    cv2.waitKey(0)
def hop_nhat_mau(anh):
    merged = cv2.merge(anh)
    return merged
def draw(frm):
    line(frm)
    return frm

class switch_python:
    def __init__(self):
        self.case = 'case'
        self.image = nhap_anh()
    def switch(self,case):
        default = "Incorrect"
        x=self.case+case
        return getattr(self,str(x),lambda: default)()
    def case1(self):
        hien_thi_anh(self.image)
    def case2(self):
        luu_anh(self.image)
    def case3(self):
        img = thay_doi_mau(self.image)
        hien_thi_anh(img)
    def case4(self):
        frm = khung_ve()
        res = draw(frm)
        hien_thi_anh(res)
    def case5(self):
        res = draw(self.image)
        hien_thi_anh(res)
    def case6(self):
        (b,g,r) = tach_mau(self.image)
        hien_thi_mau_blue(self.image,b)
        hien_thi_mau_green(self.image,g)
        hien_thi_mau_red(self.image,r)
    def case7(self):
        mg = hop_nhat_mau(tach_mau(self.image))
        hien_thi_anh(mg)
        
    
if __name__ == '__main__':
    test = switch_python()
    print('--------------------Menu---------------')
    print('1. Hiển thị ảnh')
    print('2. Lưu ảnh')
    print('3. Thay đổi màu pixcel ảnh')
    print('4. Vẽ trên khung trống')
    print('5. Vẽ trên ảnh đã tải lên')
    print('6. Tách màu')
    print('7. Hợp nhất màu')
    print('0. thoát')
    print('---------------------------------------')
    n=10
    while(n != '0'):
        n=input('Chọn chức năng: ')
        test.switch(n)
        print('--------------------Menu---------------')
        print('1. Hiển thị ảnh')
        print('2. Lưu ảnh')
        print('3. Thay đổi màu pixcel ảnh')
        print('4. Vẽ trên khung trống')
        print('5. Vẽ trên ảnh đã tải lên')
        print('6. Tách màu')
        print('7. Hợp nhất màu')
        print('0. thoát')
        print('---------------------------------------')
        
