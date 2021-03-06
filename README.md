 # What is StaySafe?
 
 
 * StaySafe  is an application that will predict in real time whether a person is wearing a mask or not, using transfer learning. The pre-trained model used is <b>MobileNet</b> ( https://www.tensorflow.org/api_docs/python/tf/keras/applications/MobileNet ) and has been trained on a dataset that contains pictures of people wearing and not wearing face masks (https://github.com/cabani/MaskedFace-Net).
 


![Test Image 1](/IMGreadme/safe.png)


![Test Image 2](/IMGreadme/notsafe.png)



-----------------------------------------------



# What options do I have?
 
 * You can play a sound that says "please wear a mask", when someone without mask is in front of the WebCam, and can be turned <b>ON/OFF</b> by pressing the <i>sound button</i>. 
 

 * You can activate/deactivate the grid (the rectangle around the face) using the <i>grid button</i>.
 





# Where can I download it?

* You can download StaySafe, including the trained model (<b>not included on this repository</b>) , from here: <b> https://drive.google.com/drive/folders/1mnBbVKH7_LoG_zE6lx6zTf3ENlVzbalF?usp=sharing </b>





# How can I run it?
* To open the app execute the following command: <b> python StaySafe.py</b>



