import mysql.connector
import os
import glob


data_folder = os.path.join(os.getcwd(), 'images')
data = []  # list that hold the path for each image
names = []  # list for the names of the images

for root, folders, files in os.walk(data_folder):
    for f in files:
        path = os.path.join(root, f)
        data.append(path)
        names.append(os.path.splitext(f)[0]) # os.path.splitext()

#print(f'Images in folder: {len(data)}')
#print(f'Names in folder: {len(names)}')
d = dict(zip(data, names))

#for i in d:
#    print(f'Path: {i}     Name: {d[i]}')

MyDB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="minecraft",
    database="proiect_face_rec"
)

MyCursor = MyDB.cursor()
# Statement for Table creation:
# MyCursor.execute("CREATE TABLE IF NOT EXISTS Images (id INTEGER(45) NOT NULL AUTO_INCREMENT PRIMARY KEY, Photo LONGBLOB NOT NULL, Name CHAR(30) NOT NULL)")
##MyCursor.execute("CREATE TABLE IF NOT EXISTS ImagesCV2 (id INTEGER(45) NOT NULL AUTO_INCREMENT PRIMARY KEY, Photo LONGBLOB NOT NULL, Name CHAR(30) NOT NULL)")


def InsertBlob(FilePath, name):
    with open(FilePath, "rb") as file:
        BinaryData = file.read()
    SQLStatement = "INSERT INTO Images (Photo, Name) VALUES (%s, %s)"
    MyCursor.execute(SQLStatement, (BinaryData, name))
    MyDB.commit()

def DeleteBlob(givenName):
    SQLStatement = "DELETE FROM Images WHERE Name = " + "'" + givenName + "'"
    MyCursor.execute(SQLStatement)
    MyDB.commit()

'''##def InsertBlobCV2(FilePath, name):
    #with open(FilePath, "rb") as file:
    ImageData = cv2.imread(FilePath)
    SQLStatement = "INSERT INTO ImagesCV2 (Photo, Name) VALUES (%s, %s)"
    MyCursor.execute(SQLStatement, (ImageData, name))
    MyDB.commit()
    MyCursor.fetchall()'''

#for e in d:
 #   InsertBlob(e, d[e])


def RetriveAll():
    dest = glob.glob('RetrievedImages/*')
    for item in dest:
        os.remove(item)
    SQLStatement2 = "SELECT * FROM Images"
    MyCursor.execute(SQLStatement2)
    result = MyCursor.fetchall()
    #print(result[0][2])
    for index in result:
        storeFilePath = f'RetrievedImages/{index[2]}.jpg'
        with open(storeFilePath, "wb") as file:
            file.write(index[1])
            file.close()


def refreshInsert():
    dest = glob.glob('images/*')
    for item in dest:
        os.remove(item)


#RetriveAll()# nu le dubleaza
