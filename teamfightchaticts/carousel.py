import cv2
import numpy as np
import time
import glob

from PIL import ImageGrab
import PIL.Image, PIL.ImageTk
import tkinter as tk
import threading


class TwitchBotGUI(tk.Frame):
    def __init__(self, parent, width=800, height=680, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.imageLabel = tk.Label(self.parent)
        self.imageLabel.pack()
        
        self.items = ItemFinder()
        self.delay = 20
        self.loopCapture()

        
        self.state = False 
        
    def loopCapture(self):

        frame = self.items.get_items()
        
        #level = self.items.get_text(True)
        #gold = self.items.get_text(False)
        
        #gold = 'Gold: ' + str(gold)
        #level = 'Level: ' + str(level)
        
        #cv2.putText(img=frame, text=gold, org=(800, 850), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255, 255, 0),thickness=2)
        #cv2.putText(img=frame, text=level, org=(350, 850), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 255),thickness=2)
        
        self.imageLabel.tkimg = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self.imageLabel.config(image=self.imageLabel.tkimg)
        
        self.parent.update_idletasks()
        self.parent.after(self.delay, self.loopCapture)
        
        
class ItemFinder:

    
    def __init__(self):
        
        self.stop_thread = threading.Event()
        self.object_detector = cv2.createBackgroundSubtractorKNN()
        

    @staticmethod
    def prepare_item_images(fn='../images/items_sheet.jpg'):
        
        image = cv2.imread(fn)

        box = (74,74)
        box_resize = (33,33)
        coord = (78, 103)
        
        for j in range(10):
            i = j
            while i <= 9:
                
                x = coord[0]+i*96
                y = coord[1]+j*96
                cropped_image = image[y:y+box[1], x:x+box[0]]
                resized = cv2.resize(cropped_image, box_resize, interpolation = cv2.INTER_AREA)
                cv2.imwrite('../images/items/item'+str(i)+str(j)+'.png', resized)
                i += 1

    def adthresholding(self, image):
        return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 61, 11)

    def findMatches(self, img, threshold=0.8) -> list:
        
        coord = (670, 250, 1250, 700)
        bg = img[coord[1]:coord[3], coord[0]:coord[2]]
        bg_gray = cv2.cvtColor(bg, cv2.COLOR_RGB2GRAY)
        
        for filename in glob.glob('../images/items/*.png'):
            item = cv2.imread(filename)
            item_gray = cv2.cvtColor(item, cv2.COLOR_RGB2GRAY)
            w, h = item_gray.shape[::-1]
            item_name = filename.split('/')
            item_name = item_name[-1].split('\\')
            item_name = item_name[-1].split('.')[0]
        
            res = cv2.matchTemplate(bg_gray,item_gray,cv2.TM_CCOEFF_NORMED)
            
            loc = np.where( res >= threshold)
            matches =  list(zip(*loc[::-1]))
            
        
            len_matches = len(matches)
            if len_matches > 0:
                loc = self.edit_list(matches, len_matches, 10)
            else:
                loc = []
            
            for pt in loc:
                x = pt[0] + coord[0]
                y = pt[1] + coord[1]
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),1)
                cv2.putText(img, item_name, (x, y-2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,255,255))
                
        return img

    def not_satisfy2(self, a,k,critical) -> bool:
        flag=False
        cx2,cy2 = k
        for i in a:
            cx1,cy1 = i
            if(abs(cx1-cx2) < critical and abs(cy1-cy2) < critical):
                flag=True
                break
        return flag
    
    def edit_list(self, a,length_of_a,critical) -> list:
        l = []
        l.append(a[0])
        i=1
        while(i < length_of_a):
            if(self.not_satisfy2(l,a[i],critical)==True):
                i+=1
            else:
                l.append(a[i])
                i+=1
        
        return l
    
    def search_items(self):
        
        global foo
        global frame
                
        while True:
            
            if frame is None:
                continue
            foo = self.findMatches(frame)
            if self.stop_thread.is_set():
                break


if __name__ == '__main__':

    screenshot = ImageGrab.grab()
    screenshot = np.array(screenshot)
    frame = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    items = ItemFinder()
    
    thread = threading.Thread(target=items.search_items)
    
    thread.start()
    
    global foo

    foo = None

    while True:
        
        screenshot = ImageGrab.grab()
        screenshot = np.array(screenshot)
        frame = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        if foo is not None:
            
            cv2.imshow("Frame", foo)

        if cv2.waitKey(1) & 0Xff == ord('q'):
            break
        
    cv2.destroyAllWindows()
    items.stop_thread.set()
    thread.join()
