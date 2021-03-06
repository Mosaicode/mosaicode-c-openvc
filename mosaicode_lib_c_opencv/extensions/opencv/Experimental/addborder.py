#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the AddBorder class.
"""
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.blockmodel import BlockModel


class AddBorder(BlockModel):
    """
    This class contains methods related the AddBorder class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        BlockModel.__init__(self)

        self.language = "c"
        self.framework = "opencv"
        self.label = "Add Border"
        self.color = "255:217:25:245"
        self.group = "Experimental"
        self.ports = [{"type":"mosaicode_lib_c_opencv.extensions.ports.image",
                    "name":"input_image",
                    "conn_type":"Input",
                    "label":"Input Image"},
                    {"type":"mosaicode_lib_c_opencv.extensions.ports.int",
                    "name":"border_size",
                    "conn_type":"Input",
                    "label":"Border Size"},
                    {"type":"mosaicode_lib_c_opencv.extensions.ports.image",
                    "name":"output_image",
                    "conn_type":"Output",
                    "label":"Output Image"}]
        self.properties = [{"label": "Color",
                            "name": "color",
                            "type": MOSAICODE_COLOR,
                            "value":"#FF0000"
                            },
                           {"name": "type",
                            "label": "Type",
                            "type": MOSAICODE_COMBO,
                            "value":"BORDER_CONSTANT",
                            "values": ["BORDER_CONSTANT",
                                       "BORDER_REPLICATE",]
                            },
                           {"label": "Border Size",
                            "name": "border_size",
                            "type": MOSAICODE_INT,
                            "value": 1,
                            "step": 1,
                            "upper": 100,
                            "lower": 1
                            }
                           ]

#-------------------------------- C/OpenCV Code -------------------------------------                           
    
        self.codes["function"] = \
"""        
    Scalar get_scalar_color_$id$(const char * rgbColor){
        if (strlen(rgbColor) < 13 || rgbColor[0] != '#')
            return Scalar(0,0,0,0);
        char r[4], g[4], b[4];
        strncpy(r, rgbColor+1, 4);
        strncpy(g, rgbColor+5, 4);
        strncpy(b, rgbColor+9, 4);

        int ri, gi, bi = 0;
        ri = (int)strtol(r, NULL, 16);
        gi = (int)strtol(g, NULL, 16);
        bi = (int)strtol(b, NULL, 16);

        ri /= 257;
        gi /= 257;
        bi /= 257;
            
        return Scalar(bi, gi, ri, 0);
    }
"""                         

        self.codes["declaration"] = \
"""        
    Mat $port[input_image]$;
    int $port[border_size]$ = $prop[border_size]$;
    Mat $port[output_image]$;
"""        

        self.codes["execution"] = \
"""        
    if(!$port[input_image]$.empty()){
        $port[output_image]$ = $port[input_image]$.clone();
        Scalar color = get_scalar_color_$id$("$prop[color]$");
        copyMakeBorder($port[input_image]$, $port[output_image]$, $port[border_size]$, $port[border_size]$, $port[border_size]$, $port[border_size]$, $prop[type]$, color);
    }
"""    

        self.codes["deallocation"] = \
"""        
    $port[input_image]$.release();
    $port[output_image]$.release();
"""

# -----------------------------------------------------------------------------