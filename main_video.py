import cv2
from simple_facerec import SimpleFacerec
import tkinter
import database_operations as myData


#Gui initialisation
start = tkinter.Tk()
start.title("Start menu")
start.geometry("400x400+450+200")

#Labels
tkinter.Label(start, text="Admin: ").place(x=20, y=20)
tkinter.Label(start, text="Name: ").place(x=20, y=70)
tkinter.Label(start, text="Code: ").place(x=20, y=120)

#Admin fields
global name_field, code_field
name_field = tkinter.Entry(start, bd=5)
name_field.place(x=120, y=70)
code_field = tkinter.Entry(start, show='*', bd=5)
code_field.place(x=120, y=120)


def insertData():
    data_dict = myData.d
    for e in data_dict:
        myData.InsertBlob(e, data_dict[e])
    myData.RetriveAll()
    print("Data has been inserted")
    myData.refreshInsert()


def deleteEntry():
    nameDel = nameDel_field.get()
    print(f'Name: {nameDel} is to be deleted')
    myData.DeleteBlob(nameDel)
    myData.RetriveAll()


def verify():
    name = name_field.get()
    code = code_field.get()
    message = tkinter.Label(start, text="Access denied!", fg='red')
    message.place(x=70, y=20)
    message.place_forget()
    if (name != "lau") or (code != "lau"):
        #print("incoreect")
        message = tkinter.Label(start, text="Access denied!", fg='red')
        message.place(x=70, y=20)
    else:#ADMIN Menu
        top = tkinter.Toplevel()
        top.title("Admin menu")
        top.geometry("400x400+450+200")

        insert = tkinter.Button(top, text="Insert", command=insertData, bd=5)
        insert.place(x=40, y=100)
        tkinter.Label(top, text="Insert data from buffer folder").place(x=130, y=100)
        #start.destroy()

        global nameDel_field
        nameDel_field = tkinter.Entry(top, bd=5)
        nameDel_field.place(x=130, y=210)
        #nameDel = nameDel_field.get()

        deletebtn = tkinter.Button(top, text="Delete", command=deleteEntry, bd=5)
        deletebtn.place(x=40, y=210)
        tkinter.Label(top, text="Input the name of the entry you want to delete").place(x=40, y=240)

        bt_rec = tkinter.Button(top, text="Start face recognition", command=recognise, bd=5)
        bt_rec.place(x=250, y=330)

verify = tkinter.Button(start, text="Verify", command=verify, bd=5)
verify.place(x=320, y=90)


def recognise():
    sfr = SimpleFacerec()
    sfr.load_encoding_images("RetrievedImages/")

    # Load Camera
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        # Detect Faces
        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (180, 240, 20), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (170, 170, 0), 4)

        cv2.imshow("Frame   Exit with key Q", frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


tkinter.Label(start, text="Regular user: ").place(x=20, y=300)
btn = tkinter.Button(start, text="Start face recognition", command=recognise, bd=5)
btn.place(x=250, y=300)
tkinter.Label(start, text="Exit face recognition\n with key Q", fg='red').place(x=250, y=340)

start.mainloop()
