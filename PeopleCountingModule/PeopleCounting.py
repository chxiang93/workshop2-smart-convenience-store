# Workshop 2 Group 3
# Group Members:
# 1) Sue Chen Xiang B032010034
# 2. Fatin Najdah binti Najmi Ismail B032010201 
# 3. Nur Afiqah binti Anuar B032010114 
# 4. Ken Prameswari Caesarella B032010461 
# 5. Mohammad Irsyad bin Mohd Shahril B032010242

from PeopleCountingModule.mylib.centroidtracker import CentroidTracker
from PeopleCountingModule.mylib.trackableobject import TrackableObject
import numpy as np
import imutils
import dlib, cv2
import queue
import threading

class PeopleCounting:
	def __init__(self):
		self.prototxt = "PeopleCountingModule/mobilenet_ssd/MobileNetSSD_deploy.prototxt"
		self.model_pth = "PeopleCountingModule/mobilenet_ssd/MobileNetSSD_deploy.caffemodel"
		self.CONFIDENCE = 0.4
		self.skip_frames = 30
		self.frames = queue.Queue()
		self.wait = True

		# initialize the list of class labels MobileNet SSD was trained to
		# detect
		self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
			"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
			"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
			"sofa", "train", "tvmonitor"]

		# load our serialized model from disk
		self.net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model_pth)

		# initialize the frame dimensions (we'll set them as soon as we read
		# the first frame from the video)
		self.W = None
		self.H = None

		# initialize the total number of frames processed thus far, along
		# with the total number of objects that have moved either up or down
		self.totalFrames = 0
		self.totalDown = 0
		self.totalUp = 0
		self.peopleCountDay = 0
		self.peopleInside = 0
		self.empty=[]
		self.empty1=[]

	def getFrames(self):
		return self.frames.get()

	def start(self, src=0):
		self.src = src
		thread = threading.Thread(target=self.startCount, args=(), daemon=True)
		thread.start()

	# need to be called upon closing, after saving to database
	def resetPeopleCounting(self):
		self.peopleCountDay = 0 
		self.peopleInside = 0

	def startCount(self):
		# vs = thread.ThreadingClass(self.input)
		vs = cv2.VideoCapture(self.src)

		# instantiate our centroid tracker, then initialize a list to store
		# each of our dlib correlation trackers, followed by a dictionary to
		# map each unique object ID to a TrackableObject
		ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
		trackers = []
		trackableObjects = {}
		x = []

		# loop over frames from the video stream
		while True:
			# grab the next frame and handle if we are reading from either
			# VideoCapture or VideoStream
			# frame = vs.read()
			ret, frame = vs.read()
			frame = frame

			# resize the frame to have a maximum width of 500 pixels (the
			# less data we have, the faster we can process it), then convert
			# the frame from BGR to RGB for dlib
			frame = imutils.resize(frame, width = 500)
			rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

			# if the frame dimensions are empty, set them
			# (height,width)=img.shape[:2] is an example of tuple unpacking, 
			# with it you extract the rows and columns values from the shape tuple.
			if self.W is None or self.H is None:
				(self.H, self.W) = frame.shape[:2]

			# initialize the current status along with our list of bounding
			# box rectangles returned by either (1) our object detector or
			# (2) the correlation trackers
			status = "Waiting"
			rects = []

			# check to see if we should run a more computationally expensive
			# object detection method to aid our tracker
			if self.totalFrames % self.skip_frames == 0:
				# set the status and initialize our new set of object trackers
				status = "Detecting"
				trackers = []

				# convert the frame to a blob and pass the blob through the
				# network and obtain the detections
				blob = cv2.dnn.blobFromImage(frame, 0.007843, (self.W, self.H), 127.5)
				self.net.setInput(blob)
				detections = self.net.forward()

				# loop over the detections
				for i in np.arange(0, detections.shape[2]):
					# extract the confidence (i.e., probability) associated
					# with the prediction
					confidence = detections[0, 0, i, 2]

					# filter out weak detections by requiring a minimum
					# confidence
					if confidence > self.CONFIDENCE:
						# extract the index of the class label from the
						# detections list
						idx = int(detections[0, 0, i, 1])

						# if the class label is not a person, ignore it
						if self.CLASSES[idx] != "person":
							continue

						# compute the (x, y)-coordinates of the bounding box
						# for the object
						box = detections[0, 0, i, 3:7] * np.array([self.W, self.H, self.W, self.H])
						(startX, startY, endX, endY) = box.astype("int")


						# construct a dlib rectangle object from the bounding
						# box coordinates and then start the dlib correlation
						# tracker
						tracker = dlib.correlation_tracker()
						rect = dlib.rectangle(startX, startY, endX, endY)
						tracker.start_track(rgb, rect)

						# add the tracker to our list of trackers so we can
						# utilize it during skip frames
						trackers.append(tracker)

			# otherwise, we should utilize our object *trackers* rather than
			# object *detectors* to obtain a higher frame processing throughput
			else:
				# loop over the trackers
				for tracker in trackers:
					# set the status of our system to be 'tracking' rather
					# than 'waiting' or 'detecting'
					status = "Tracking"

					# update the tracker and grab the updated position
					tracker.update(rgb)
					pos = tracker.get_position()

					# unpack the position object
					startX = int(pos.left())
					startY = int(pos.top())
					endX = int(pos.right())
					endY = int(pos.bottom())

					# add the bounding box coordinates to the rectangles list
					rects.append((startX, startY, endX, endY))

			# draw a horizontal line in the center of the frame -- once an
			# object crosses this line we will determine whether they were
			# moving 'up' or 'down'
			# syntax: cv2.line(image, start_point, end_point, color, thickness) 
			# 17 // 3  # floor division discards the fractional part
			cv2.line(frame, (0, self.H // 2), (self.W, self.H // 2), (0, 0, 0), 3)
			# Syntax: cv2.putText(image, text, org, font, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]]) ,, H - ((i * 20) + 200)
			cv2.putText(frame, "Entrance-", (self.W - ((i * 20)+240), 15),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

			# use the centroid tracker to associate the (1) old object
			# centroids with (2) the newly computed object centroids
			objects = ct.update(rects)

			# loop over the tracked objects
			for (objectID, centroid) in objects.items():
				# check to see if a trackable object exists for the current
				# object ID
				to = trackableObjects.get(objectID, None)

				# if there is no existing trackable object, create one
				if to is None:
					to = TrackableObject(objectID, centroid)

				# otherwise, there is a trackable object so we can utilize it
				# to determine direction
				else:
					# the difference between the y-coordinate of the *current*
					# centroid and the mean of *previous* centroids will tell
					# us in which direction the object is moving (negative for
					# 'up' and positive for 'down')
					y = [c[1] for c in to.centroids]
					direction = centroid[1] - np.mean(y)
					to.centroids.append(centroid)

					# check to see if the object has been counted or not
					if not to.counted:
						# if the direction is negative (indicating the object
						# is moving up) AND the centroid is above the center
						# line, count the object
						if direction < 0 and centroid[1] < self.H // 2:
							self.totalUp += 1
							self.empty.append(self.totalUp)
							to.counted = True

						# if the direction is positive (indicating the object
						# is moving down) AND the centroid is below the
						# center line, count the object
						elif direction > 0 and centroid[1] > self.H // 2:
							self.peopleCountDay += 1
							self.totalDown += 1
							self.empty1.append(self.totalDown)
							#print(empty1[-1])
							x = []
							# compute the sum of total people inside
							# x.append(len(self.empty1)-len(self.empty))
							x.append(self.totalDown - self.totalUp)
							print(x)
							print(self.peopleInside)
							print(self.peopleCountDay)
							self.peopleInside = x[0]
							#print("Total people inside:", x)

							to.counted = True


				# store the trackable object in our dictionary
				trackableObjects[objectID] = to

				# draw both the ID of the object and the centroid of the
				# object on the output frame
				text = "ID {}".format(objectID)
				cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
				cv2.circle(frame, (centroid[0], centroid[1]), 4, (255, 255, 255), -1)

			# construct a tuple of information we will be displaying on the
			info = [
			("Exit", self.totalUp),
			("Enter", self.totalDown),
			("Status", status),
			]

			info2 = [
			("Total people inside", x),
			]

					# Display the output
			for (i, (k, v)) in enumerate(info):
				text = "{}: {}".format(k, v)
				cv2.putText(frame, text, (10, self.H - ((i * 20) + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

			for (i, (k, v)) in enumerate(info2):
				text = "{}: {}".format(k, v)
				cv2.putText(frame, text, (265, self.H - ((i * 20) + 60)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

			# show the output frame
			# cv2.imshow("Real-Time Monitoring/Analysis Window", frame)
			key = cv2.waitKey(20) & 0xFF
			
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			self.frames.put(frame)

			if self.wait:
				self.wait = False

			# if the `q` key was pressed, break from the loop
			if key == ord("q"):
				break

			# increment the total number of frames processed thus far and
			# then update the FPS counter
			self.totalFrames += 1
		
		vs.release()
		# close any open windows
		cv2.destroyAllWindows()

if __name__ == "__main__":
	people_counter = PeopleCounting(src=1)
	people_counter.start()