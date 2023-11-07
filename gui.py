from re import L
from flask import Flask, request, jsonify, render_template #Flask web-server backend
import numpy as np #images are in numpy format: therefore, np array is required to process 
import cv2 #to read n process any image
from tensorflow.keras.models import load_model   #to load the AI model
#all necessary imports 

# img = 'img.png'
# img = cv2.imread(img)

model = load_model('model.h5') #loading the AI model

app = Flask(__name__) #initialization of the object

@app.route('/',methods = ['POST','GET']) #to get the data in GET and POST format

#creating a main function
def main():
    if request.method == 'POST': #checking if the request contains any image in POST method
        imagefile = request.files.get('imagefile', '') #reading the image 
        
        if imagefile.filename == '':
        	return render_template('upload.html',
        	data = {"output":"Please Upload Image"},
        	color_data = {'color':"red"})
        imagefile.save("static/output.jpg") #saving the image
        img = cv2.imread('static/output.jpg') #loading the saved image
        img = np.array([cv2.resize(img,(300,300))]) #converting the image to 100x100 size (hieght and width)
        
        #creating color combination of the output
        r = {"0":'Covid', 
        "1":'Healthy',
        "2":"Others"}
        rc = {"0":'red','1':"green",'2':"Orange"}
        
        #getting the required output from model (prediction
        output = np.argmax(model.predict(img), axis=1)
        
        #identfying the color wrt to output label
        color_data = {'color':rc[str(output[0])]}
        
        #creating the output in JSON format
        data = {"output":r[str(output[0])]} 
        
        #returning the output in the form of Json 
        return render_template('upload.html', data = data, color_data = color_data)
        
    #if the requested method is get, will load only the option to load image 
    elif request.method == 'GET':
        return render_template('upload.html')


#creating main function 
if __name__ == '__main__':
    app.run(debug=True)
