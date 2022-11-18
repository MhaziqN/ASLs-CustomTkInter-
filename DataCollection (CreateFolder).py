import time

import customtkinter
import os

class App(customtkinter.CTk):
        def __init__(self):
            super().__init__()

            self.title('ASLDs')
            self.minsize(250, 150)
#            self.iconbitmap('AS (1).ico')

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

                                                         text_font=("Roboto Medium", -12))

            self.buttonEx.grid(row=4, column=0, pady=10, padx=10)

            self.Label2 = customtkinter.CTkLabel(master=self.frame_left,
                                                      text='Appearance Mode',
                                                      text_font=("Roboto Medium", -12))

            self.Label2.grid(row=7, column=0, pady=10, padx=10)

            self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                                 values=['Light', 'Dark', 'System'],
                                                                 #command=self.Change_Apearance_Mode
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

            self.ButtonOk.grid(row=7, column=2, pady=10, padx=10)

        def Ok_Button(self):
            I_Folder = self.EntryNDE.get()
            #=====Masukkan variable for image capture============#
            #=====================Create new folder =====================

            path_D = "C:/Users/user/PycharmProjects/New/"
            path = os.path.join(path_D, I_Folder)

            os.mkdir(path)
            print(("Directory '%s' created " % I_Folder))
            print(path)


            #===========Masukkan prosess for image capturing===============
            #========== Button snap image as shown Below ===================
            key == cv2.waitkey (1)
            if key == ord ("s"):
                counter += 1
                cv2.imwrite(f'{path}/Image_{time.time()}.jpg', imgWhite)
                print(counter)

            if key == ord ('w'):
                #================== Masukkan script asal for key "w"








if __name__ == "__main__":
    app = App()
    app.mainloop()
