This is simple package for your easy AI projects.

[ImageClassification]

Classification is as simple as...

from X_AI.Vision.ImageClassification import Classify
classify = Classify.ImageClassification(path)  #path to imagefolder
classify._Train()

That's it your model is trained

To plot your results:-

classify.plot_results()

To predict on New images:

classify._predict()

To save your model/weights:

classify.save_model(path) 	#path to store the model
classify.save_weights(path) 	# path to store weights




