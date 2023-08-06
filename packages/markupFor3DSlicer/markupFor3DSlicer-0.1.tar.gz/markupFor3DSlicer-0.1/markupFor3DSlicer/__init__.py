def line(x,y,z,vectX,vectY,vectZ,norme,name):
    dLine={
            "type": "Line",
            "coordinateSystem": "LPS",
            "locked": False,
            "labelFormat": "%N-%d",
            "controlPoints": [
                {
                    "id": "1",
                    "label": name,
                    "description": "",
                    "associatedNodeID": "vtkMRMLScalarVolumeNode1",
                    "position": [y, x, z],
                    "orientation": [-1.0, -0.0, -0.0, -0.0, -1.0, -0.0, 0.0, 0.0, 1.0],
                    "selected": True,
                    "locked": True,
                    "visibility": True,
                    "positionStatus": "defined"
                },
                {
                    "id": "2",
                    "label": "MarkupsLine-2",
                    "description": "",
                    "associatedNodeID": "vtkMRMLScalarVolumeNode1",
                    "position": [vectY, vectX, vectZ],
                    "orientation": [-1.0, -0.0, -0.0, -0.0, -1.0, -0.0, 0.0, 0.0, 1.0],
                    "selected": True,
                    "locked": True,
                    "visibility": True,
                    "positionStatus": "defined"
                }
            ],
            "measurements": [
                {
                    "name": "length",
                    "enabled": True,
                    "value": norme,
                    "printFormat": "%-#4.4gmm"
                }
            ],
            "display": {
                "visibility": True,
                "opacity": 1.0,
                "color": [0.4, 1.0, 0.0],
                "selectedColor": [1.0, 0.5000076295109484, 0.5000076295109484],
                "activeColor": [0.4, 1.0, 0.0],
                "propertiesLabelVisibility": True,
                "pointLabelsVisibility": False,
                "textScale": 3.0,
                "glyphType": "Sphere3D",
                "glyphScale": 1.0,
                "glyphSize": 5.0,
                "useGlyphScale": True,
                "sliceProjection": False,
                "sliceProjectionUseFiducialColor": True,
                "sliceProjectionOutlinedBehindSlicePlane": False,
                "sliceProjectionColor": [1.0, 1.0, 1.0],
                "sliceProjectionOpacity": 0.6,
                "lineThickness": 0.3,
                "lineColorFadingStart": 1.0,
                "lineColorFadingEnd": 10.0,
                "lineColorFadingSaturation": 1.0,
                "lineColorFadingHueOffset": 0.0,
                "handlesInteractive": False,
                "snapMode": "toVisibleSurface"
            }
        }
    return dLine