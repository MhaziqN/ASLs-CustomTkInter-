from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import customtkinter
from PIL import ImageTk, Image
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import time
import pyttsx3
import os

customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('green')

        #============================ MAIN PAGE =========================#
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title('ASLDs')
        self.minsize(780, 520)
        self.iconbitmap('AS (1).ico')

        #========================= Setup Image Logo ======================
       # fileIlocation = "D:/Cisco/Phyton/"
       # image_path = os.path.join (os.path.dirname(os.path.realpath(__file__)), "pythonProject")
       # self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, 'AS.png')), size=(500, 150))


        # ===============Create Two Frame===============================

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)


        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="OPTION",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Scan Gesture",
                                                command=self.ScanButton
                                                )
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                command=self.AddGesture,
                                                text="New Gesture",
                                                )
        self.button_2.grid(row=3, column=0, pady=10, padx=20)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Exit",
                                                command=self.Exit,
                                                )
        self.button_3.grid(row=4, column=0, pady=10, padx=20)

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.Change_Appearance_M
                                                        )
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ====================== frame_right =================================

        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        #self.frame_right_image_logo = customtkinter.CTkLabel(self.frame_right, text="", image=self.logo_image)
        #self.frame_right_image_logo.grid(row=0, column=0,padx=20,pady=10 )

        #       self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        #       self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        #        self.frame_info.rowconfigure(0,weight=1)


        #        self.frame_info.columnconfigure(0,weight=1)

        self.imageLogo = customtkinter.CTkButton(master=self.frame_right,
                                                fg_color=None, hover=False,
                                                text="",
                                                image=ImageTk.PhotoImage(Image.open("AS.png"))
                                                )

        self.imageLogo.grid(row=0, column=2, columnspan=2, rowspan=2, pady=10, padx=10)


    def Exit(self):
        app = customtkinter.CTk()
        app.geometry("400x200")
        app.iconbitmap('AS (1).ico')
        app.title('Exit Application')

        def OkB_function():
            self.destroy()
            app.destroy()

        #       Guna "relx" and 'rely' untuk placement gantikan grid.
        Label = customtkinter.CTkLabel(master=app, text="Are you sure you want to exit the application ?")
        Label.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

        button = customtkinter.CTkButton(master=app, text='OK', command=OkB_function)
        button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

        app.mainloop()

    def Change_Appearance_M(Self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def ScanButton(self):

        def talk(labels):
            engine.say(labels)
            engine.runAndWait()

        customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

        cap = cv2.VideoCapture(0)
        detector = HandDetector(maxHands=1)
        classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")
        engine = pyttsx3.init()
        voice = engine.getProperty('voice')
        engine.setProperty('voice', voice[0])

        offset = 20
        imgsize = 300

        folder = " D:\Cisco\Phyton\pythonProject\A"
        counter = 0

        labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                  "U", "V", "W",
                  "X", "Y", "Z"]

        while True:
            success, img = cap.read()
            imgOutput = img.copy()
            hands, img = detector.findHands(img)
            if hands:
                hand = hands[0]
                x, y, w, h = hand['bbox']

                imgWhite = np.ones((imgsize, imgsize, 3), np.uint8) * 255
                imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

                imgCropShape = imgCrop.shape

                # Image collector Resolution Capture

                aspectRatio = h / w

                if aspectRatio > 1:
                    k = imgsize / h  # Video capture Hight+Size Resolution
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgsize))
                    imgResizeShape = imgResize.shape
                    wGap = math.ceil((imgsize - wCal) / 2)  # Vide capture Centre postion
                    imgWhite[:, wGap:wCal + wGap] = imgResize  # Declare Resolution
                    prediction, index = classifier.getPrediction(imgWhite, draw=False)
                    print(prediction, index)


                else:
                    k = imgsize / w  # Video capture data more than rectangle size that being set
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgsize, hCal))
                    imgResizeShape = imgResize.shape
                    hGap = math.ceil((imgsize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize  # Declare Resolution
                    prediction, index = classifier.getPrediction(imgWhite, draw=False)
                    # HIGHT                              #LENGHT                          #cOLOUR CODE    #cOLOUR FILLED BOXES
                cv2.rectangle(imgOutput, (x - offset, y - offset - 50), (x + w + offset - 50, y - offset - 50 + 50),
                              (255, 64, 64), cv2.FILLED)
                cv2.putText(imgOutput, labels[index], (x, y - 25), cv2.FONT_HERSHEY_COMPLEX, 2, (240, 248, 255), 2)
                cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (255, 64, 64), 4)
                # talk(labels[index])

                cv2.imshow("ImageCrop", imgCrop)
                cv2.imshow("ImageWhite", imgWhite)

            # for image collector jangan terlalu dekat nnti error
            # jauh kit

            cv2.imshow("Image", imgOutput)
            Key = cv2.waitKey(1)
            #           "S" key function for captured input function from live input
            if Key == ord('s'):
                talk('successfully captured !')
                with open('Word.txt', "a") as f:
                    f.write(labels[index])
            #           "a" Key function for clear data in 'Word.txt' file
            elif Key == ord('a'):
                file = open("Word.txt", "r+")
                file.truncate(0)
                file.close()
            #           "d' KEy function fro read 'r' line phrases in 'Word.txt' file
            elif Key == ord('d'):

                with open('Word.txt', "r") as f:
                    for line in f.readlines():
                        print(line)

                        class App(customtkinter.CTk):

                            def __init__(self):
                                super().__init__()

                                self.title('ASLDs')
                                self.minsize(250, 150)
                                self.iconbitmap('AS (1).ico')

                                self.grid_columnconfigure(1, weight=1)
                                self.grid_rowconfigure(0, weight=1)

                                # ===================== Devide 2 partition ==============================

                                self.frame_left = customtkinter.CTkFrame(master=self,
                                                                         width=180,
                                                                         corner_radius=0)
                                self.frame_left.grid(row=0, column=0, sticky="nswe")

                                self.frame_right = customtkinter.CTkFrame(master=self)
                                self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

                                # ===================== cfarme left grid conf ==============================
                                # configure grid layout (1x11)
                                self.frame_left.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
                                self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
                                self.frame_left.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
                                self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

                                self.label = customtkinter.CTkLabel(master=self.frame_left,
                                                                    text="Scan Gesture",
                                                                    text_font=('Roboto Medium', -16))

                                self.label.grid(row=0, column=0, pady=10, padx=10)

                                self.buttonEx = customtkinter.CTkButton(master=self.frame_left,
                                                                        text="Exit",
                                                                        command=self.Exit_,
                                                                        text_font=("Roboto Medium", -12))

                                self.buttonEx.grid(row=4, column=0, pady=10, padx=10)

                                self.Label2 = customtkinter.CTkLabel(master=self.frame_left,
                                                                     text='Appearance Mode',
                                                                     text_font=("Roboto Medium", -12))

                                self.Label2.grid(row=7, column=0, pady=10, padx=10)

                                self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                                                values=['Light', 'Dark', 'System'],
                                                                                command=self.Change_Apearance_Mode
                                                                                )
                                self.optionmenu_1.grid(row=8, column=0, pady=10, padx=10)

                                # ================================== frame Right Grid ============================================

                                self.frame_right.rowconfigure((0, 1, 2, 3, 4), weight=0)  # row spacing configure
                                self.frame_right.columnconfigure((0, 1, 2, 3, 4), weight=1)  # column spacing configure

                                self.labelR1 = customtkinter.CTkLabel(master=self.frame_right,
                                                                      text="Data Translate",
                                                                      text_font=("Roboto Medium", -16))

                                self.labelR1.grid(row=0, column=2, pady=10, padx=10)

                                self.labelR2 = customtkinter.CTkLabel(master=self.frame_right,
                                                                      text='Word Translated :\n' + line,
                                                                      text_font=('Roboto Medium', -12))

                                self.labelR2.grid(row=1, column=2, pady=10, padx=10)

                                self.ButtonVoice = customtkinter.CTkButton(master=self.frame_right,
                                                                           text='Translated',
                                                                           command=self.Voivetrans_,
                                                                           text_font=('Roboto Medium', -12))
                                self.ButtonVoice.grid(row=3, column=2, pady=10, padx=10)

                            def Change_Apearance_Mode(self, new_appearance_mode):
                                customtkinter.set_appearance_mode(new_appearance_mode)

                            def Exit_(self):
                                app = customtkinter.CTk()
                                app.geometry("400x200")
                                app.iconbitmap('AS (1).ico')
                                app.title('Exit Application')

                                def OkB_function():
                                    self.destroy()
                                    app.destroy()

                                #       Guna "relx" and 'rely' untuk placement gantikan grid.
                                Label = customtkinter.CTkLabel(master=app,
                                                               text="Are you sure you want to exit the application ?")
                                Label.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

                                button = customtkinter.CTkButton(master=app, text='OK', command=OkB_function)
                                button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

                                app.mainloop()

                            def Ok_(self):
                                self.destroy()

                            def Voivetrans_(self):
                                talk(line)

                        if __name__ == "__main__":
                            app = App()
                            app.mainloop()

            if Key == ord('w'):
                cap.close()

    def AddGesture(self):
        # ======================== Main Interface ==================================
        class App(customtkinter.CTk):
            def __init__(self):
                super().__init__()

                self.title('ASLDs')
                self.minsize(250, 150)
                self.iconbitmap('AS (1).ico')

                self.grid_columnconfigure(1, weight=1)
                self.grid_rowconfigure(0, weight=1)

                # ===================== Devide 2 partition ==============================

                self.frame_left = customtkinter.CTkFrame(master=self,
                                                         width=180,
                                                         corner_radius=0)
                self.frame_left.grid(row=0, column=0, sticky="nswe")

                self.frame_right = customtkinter.CTkFrame(master=self)
                self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

                # ===================== cfarme left grid conf ==============================
                # configure grid layout (1x11)
                self.frame_left.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
                self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
                self.frame_left.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
                self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

                self.label = customtkinter.CTkLabel(master=self.frame_left,
                                                    text="New Gesture",
                                                    text_font=('Roboto Medium', -16))

                self.label.grid(row=0, column=0, pady=10, padx=10)

                self.buttonEx = customtkinter.CTkButton(master=self.frame_left,
                                                        text="Exit",
                                                        command=self.Exit_,
                                                        text_font=("Roboto Medium", -12))

                self.buttonEx.grid(row=4, column=0, pady=10, padx=10)

                self.Label2 = customtkinter.CTkLabel(master=self.frame_left,
                                                     text='Appearance Mode',
                                                     text_font=("Roboto Medium", -12))

                self.Label2.grid(row=7, column=0, pady=10, padx=10)

                self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                                values=['Light', 'Dark', 'System'],
                                                                command=self.Change_Apearance_Mode
                                                                )
                self.optionmenu_1.grid(row=8, column=0, pady=10, padx=10)

                # ================================== frame Right Grid ============================================

                self.frame_right.rowconfigure((0, 1, 2, 3, 4), weight=0)  # row spacing configure
                self.frame_right.columnconfigure((0, 1, 2, 3, 4), weight=1)  # column spacing configure

                self.labelR1 = customtkinter.CTkLabel(master=self.frame_right,
                                                      text="New Data Collection",
                                                      text_font=("Roboto Medium", -16))

                self.labelR1.grid(row=0, column=2, pady=10, padx=10)

                self.labelR2 = customtkinter.CTkLabel(master=self.frame_right,
                                                      text='Please choose your Alphabet option for Data collection A-Z',
                                                      text_font=('Roboto Medium', -12))

                self.labelR2.grid(row=1, column=2, pady=10, padx=10)

                self.EntryNDE = customtkinter.CTkEntry(master=self.frame_right,
                                                       width=140,
                                                       placeholder_text=" Enter New Value",
                                                       )

                self.EntryNDE.grid(row=2, column=2, pady=10, padx=10)

                self.ButtonOk = customtkinter.CTkButton(master=self.frame_right,
                                                        text="Ok",
                                                        command=self.Ok_Button,
                                                        text_font=('Roboto Medium', -12))

                self.ButtonOk.grid(row=8, column=2, pady=10, padx=10)

                self.ButtonBr = customtkinter.CTkButton(master=self.frame_right,
                                                        text="Browse",
                                                        command=self.Openfile,
                                                        text_font=('Roboto Medium', -12))

                self.ButtonBr.grid(row=7, column=2, pady=10, padx=10)

                # ============ frame_info ============
                self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
                self.frame_info.grid(row=9, column=1, columnspan=9, rowspan=6, pady=10, padx=10, sticky="nsew")

                # configure grid layout (1x1)
                self.frame_info.rowconfigure(0, weight=1)
                self.frame_info.columnconfigure(0, weight=1)

                self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                           text="*************************  Note   ********************\n\n" +
                                                                "Please refer from File list (Browse) for document existent\n\n" +
                                                                "(S) = Snap Picture  (W) = Open file capture ",
                                                           height=100,
                                                           corner_radius=6,  # <- custom corner radius
                                                           fg_color=("white", "gray38"),  # <- custom tuple-color
                                                           justify=customtkinter.LEFT)
                self.label_info_1.grid(row=9, column=0, padx=15, pady=15,sticky="nwe")

            def Openfile (self):
                root = Tk()
                root.withdraw()
                file_path = filedialog.askopenfilename()

            def Change_Apearance_Mode(self, new_appearance_mode):
                customtkinter.set_appearance_mode(new_appearance_mode)

            def Exit_(self):
                app = customtkinter.CTk()
                app.geometry("400x200")
                app.iconbitmap('AS (1).ico')
                app.title('Exit Application')

                def OkB_function():
                    self.destroy()
                    app.destroy()

                #       Guna "relx" and 'rely' untuk placement gantikan grid.
                Label = customtkinter.CTkLabel(master=app, text="Are you sure you want to exit the application ?")
                Label.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

                button = customtkinter.CTkButton(master=app, text='OK', command=OkB_function)
                button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

                app.mainloop()

            def Ok_Button(self):
                I_Folder = self.EntryNDE.get()
                # =====================Create new folder =====================
                path_D = "D:/Cisco/Phyton/pythonProject/AddGesture Test/"
                path = os.path.join(path_D, I_Folder)
                os.mkdir(path)
                print("Process complete...")

                cap = cv2.VideoCapture(0)
                detector = HandDetector(maxHands=1)

                offset = 20
                imgsize = 300

                counter = 0

                while True:

                    success, img = cap.read()
                    hands, img = detector.findHands(img)
                    if hands:
                        hand = hands[0]
                        x, y, w, h = hand['bbox']

                        imgWhite = np.ones((imgsize, imgsize, 3), np.uint8) * 255
                        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

                        imgCropShape = imgCrop.shape

                        # Image collectore Resolution Capture

                        aspectRatio = h / w

                        if aspectRatio > 1:
                            k = imgsize / h  # Video capture Hight+Size Resolution
                            wCal = math.ceil(k * w)
                            imgResize = cv2.resize(imgCrop, (wCal, imgsize))
                            imgResizeShape = imgResize.shape
                            wGap = math.ceil((imgsize - wCal) / 2)  # Vide capture Centre postion
                            imgWhite[:, wGap:wCal + wGap] = imgResize  # Declare Resolution

                        else:
                            k = imgsize / w  # Video capture data more than rectangle size that being set
                            hCal = math.ceil(k * h)
                            imgResize = cv2.resize(imgCrop, (imgsize, hCal))
                            imgResizeShape = imgResize.shape
                            hGap = math.ceil((imgsize - hCal) / 2)
                            imgWhite[hGap:hCal + hGap, :] = imgResize  # Declare Resolution

                        cv2.imshow("ImageCrop", imgCrop)
                        cv2.imshow("ImageWhite", imgWhite)

                    # for image collector jangan terlalu dekat nnti error
                    # jauh kit

                    cv2.imshow("Image", img)
                    # ========== Button snap image as shown Below ===================
                    key = cv2.waitKey(1)
                    if key == ord("s"):
                        counter += 1
                        cv2.imwrite(f'{path}/Image_{time.time()}.jpg',imgWhite)
                        print(counter)

                    if key == ord('w'):

                        class App(customtkinter.CTk):

                            def Change_Apearance_Mode(self, new_appearance_mode):
                                customtkinter.set_appearance_mode(new_appearance_mode)

                            def Exit_(self):
                                app = customtkinter.CTk()
                                app.geometry("400x200")
                                app.iconbitmap('AS (1).ico')
                                app.title('Exit Application')

                                def OkB_function():
                                    self.destroy()
                                    app.destroy()

                                #       Guna "relx" and 'rely' untuk placement gantikan grid.
                                Label = customtkinter.CTkLabel(master=app,
                                                               text="Are you sure you want to exit the application ?")
                                Label.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

                                button = customtkinter.CTkButton(master=app, text='OK', command=OkB_function)
                                button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

                                app.mainloop()

                            def Openfile(self):
                                root = Tk()
                                root.withdraw()
                                file_path = filedialog.askopenfilename()

                            def __init__(self):
                                super().__init__()

                                self.title('ASLDs')
                                self.minsize(250, 150)
                                self.iconbitmap('AS (1).ico')

                                self.grid_columnconfigure(1, weight=1)
                                self.grid_rowconfigure(0, weight=1)

                                # ===================== Devide 2 partition ==============================

                                self.frame_left = customtkinter.CTkFrame(master=self,
                                                                         width=180,
                                                                         corner_radius=0)
                                self.frame_left.grid(row=0, column=0, sticky="nswe")

                                self.frame_right = customtkinter.CTkFrame(master=self)
                                self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

                                # ===================== cfarme left grid conf ==============================
                                # configure grid layout (1x11)
                                self.frame_left.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
                                self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
                                self.frame_left.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
                                self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

                                self.label = customtkinter.CTkLabel(master=self.frame_left,
                                                                    text="New Gesture",
                                                                    text_font=('Roboto Medium', -16))

                                self.label.grid(row=0, column=0, pady=10, padx=10)

                                self.buttonEx = customtkinter.CTkButton(master=self.frame_left,
                                                                        text="Exit",
                                                                        command=self.Exit_,
                                                                        text_font=("Roboto Medium", -12))

                                self.buttonEx.grid(row=4, column=0, pady=10, padx=10)

                                self.Label2 = customtkinter.CTkLabel(master=self.frame_left,
                                                                     text='Appearance Mode',
                                                                     text_font=("Roboto Medium", -12))

                                self.Label2.grid(row=7, column=0, pady=10, padx=10)

                                self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                                                values=['Light', 'Dark', 'System'],
                                                                                command=self.Change_Apearance_Mode
                                                                                )
                                self.optionmenu_1.grid(row=8, column=0, pady=10, padx=10)

                                # ================================== frame Right Grid ============================================

                                self.frame_right.rowconfigure((0, 1, 2, 3, 4), weight=0)  # row spacing configure
                                self.frame_right.columnconfigure((0, 1, 2, 3, 4), weight=1)  # column spacing configure

                                self.labelR1 = customtkinter.CTkLabel(master=self.frame_right,
                                                                      text="New Data Collection",
                                                                      text_font=("Roboto Medium", -16))

                                self.labelR1.grid(row=0, column=2, pady=10, padx=10)

                                self.labelR2 = customtkinter.CTkLabel(master=self.frame_right,
                                                                      text="You have captured " + str(
                                                                          counter) + " image captured.",
                                                                      text_font=('Roboto Medium', -12))

                                self.labelR2.grid(row=1, column=2, pady=10, padx=10)

                                self.ButtonBr = customtkinter.CTkButton(master=self.frame_right,
                                                                        text="Open File",
                                                                        command=self.Openfile,
                                                                        text_font=('Roboto Medium', -12))

                                self.ButtonBr.grid(row=7, column=2, pady=10, padx=10)

                        if __name__ == "__main__":
                            app = App()
                            app.mainloop()

        if __name__ == "__main__":
            app = App()
            app.mainloop()
if __name__ == "__main__":
    app = App()
    app.mainloop()
