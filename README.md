# Smart Convenience Store
A smart convenience store system is a retail system that combines traditional convenience store operations with advanced technology such as Machine Learning and computer vision to create a more efficient, secure, and personalized shopping experience for customers. Machine learning algorithms can be used to predict consumer demand, optimize product placement, and provide personalized product recommendations. Computer vision can be used for tasks such as people counting, object detection, and item recognition, which can be used for security and marketing purposes. The system can also include features such as self-checkout and mobile payments, making the shopping experience more convenient for customers. In addition, the system can also provide valuable insights to store managers, helping them make data-driven decisions, such as which products to stock, and when to restock them. Overall, a smart convenience store system aims to improve the efficiency and convenience of retail operations, while providing customers with a personalized and secure shopping experience, using advanced technologies.

# System Architecture 
The system is built with implementation of a convolutional neural network (CNN) transfer learning technique to train a model to recognise the type of product from the input image from the camera using PyTorch library and YOLOv5 model. The system also uses another deep neural network (DNN) model which can count the number of people going inside or going outside of the convenience store using MobileNet Single Shot Detector (SSD) model. Both the pre-trained object detection network model is loaded using OpenCV’s dnn module. This will enable us to pass input images through the network and obtain the output bounding box (x,y) coordinates of each recognized object in the image.

# Full Poster

[Click for full poster](assets/poster.pdf)

# Full Report

[Click for full report](assets/report.pdf)

# Module Developed

![poster module](assets/poster1.jpg)

# Artificial Intelligence Technique

![poster ai](assets/poster2.jpg)

# Accuracy of Artificial Intelligence Technique

![poster result ai](assets/poster3.jpg)

# Group Members

![members](assets/members.jpg)
