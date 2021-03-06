#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the HarrisCorner class.
"""

from mosaicode.GUI.fieldtypes import *
from mosaicode.model.blockmodel import BlockModel

class HarrisCorner(BlockModel):
	"""
	This class contains methods related the HarrisCorner class.
	"""

	def __init__(self):
		BlockModel.__init__(self)

		self.language = "c"
		self.framework = "opencv"
		self.label = "Harris Corner Detector"
		self.color = "0:138:64:245"
		self.group = "Gradients, Edges and Corners"
		self.ports = [{"type": "mosaicode_lib_c_opencv.extensions.ports.image",
						"name": "input_image",
						"label": "Input Image",
						"conn_type": "Input"},
						{"type": "mosaicode_lib_c_opencv.extensions.ports.image",
						"name": "output_image",
						"label": "Output Image",
						"conn_type":"Output"}
		]
		self.properties = [{"label": "Harris parameter",
							"name": "parameter",
							"type": MOSAICODE_INT,
							"value": 150,
							"step": 1,
							"lower": 50,
							"upper": 255
							}
		]

# --------------------------- C/OpenCV Code --------------------------- #

		self.codes["declaration"] = \
"""
	Mat $port[input_image]$;
	Mat $port[output_image]$;
	Mat tmp_$id$;
"""

		self.codes["execution"] = \
"""		
	if(!$port[input_image]$.empty()){
		cvtColor($port[input_image]$, $port[input_image]$, COLOR_BGR2GRAY);
		$port[output_image]$ = Mat::zeros($port[input_image]$.size(), CV_32FC1);
		cornerHarris($port[input_image]$, tmp_$id$, 2, 3, 0.04, BORDER_DEFAULT);
		normalize(tmp_$id$, tmp_$id$, 0, 255, NORM_MINMAX, CV_32FC1, Mat());
		convertScaleAbs(tmp_$id$, $port[output_image]$);
		for(int j = 0; j < tmp_$id$.rows ; j++){ 
			for(int i = 0; i < tmp_$id$.cols; i++){
            	if((int) tmp_$id$.at<float>(j,i) > $prop[parameter]$){
            		circle( $port[output_image]$, Point(i, j), 5, Scalar(0), 2, 8, 0);
              	}
          	}
		}
	}
"""

		self.codes["deallocation"] = \
"""
	$port[input_image]$.release();
	$port[output_image]$.release();
"""			

# --------------------------------------------------------------------- #