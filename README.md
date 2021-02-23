 # What is StaySafe?
 
 
 * StaySafe  is an application that in real time will predict whether a person is wearing a mask or not, using transfer learning. The pre-trained model used is <b>MobileNet</b> ( https://www.tensorflow.org/api_docs/python/tf/keras/applications/MobileNet ) and has been trained on a dataset that contains pictures of people wearing or not wearing face masks (https://github.com/cabani/MaskedFace-Net).
 


![Test Image 1](/IMGreadme/safe.png)


![Test Image 2](/IMGreadme/notsafe.png)



-----------------------------------------------



# What options do i have?
 
 * It can play a sound in the background, that says "please wear a mask", and can be turned <b>ON/OFF</b> by accessing the <i>sound button</i>. 
 

 * You can <b>activate/deactivate</b> the grid (the rectangle around the face) using the <i>grid button</i>.



# Where can I download it?

* You can download StaySafe, including the trained model, from here: <b> https://drive.google.com/drive/folders/1mnBbVKH7_LoG_zE6lx6zTf3ENlVzbalF?usp=sharing </b>

* To run it execute the following command: <b> python StaySafe.py</b>
