# DALLAS - Dlc seperAte muLti animaL AnalysiS

## Divide and conquer to analyse the trajectory file

1. read in data frame wise
1.1. read in text file row wise
1.2. get frame frameNumber
1.3. read in object data
        - object:
            - name
            - qualität
            - bounding box
            - center of mass
2. identify arena 
2.1 which arena-object is where on the image (marker?)
    - sorting after x and y coordinates
    - finding marker position 
    - identifying which arena is where
2.2 mean of arenas over time to stabilize arena positions
3. fly analysis
    - fly assignment to arena
    - fly trajectory
4. food choice preference
    - if the mean x coordinate of the fly is larger than the mean x coordinate of the assigned arena, the fly is on the right position
    - preference IDX
    - choice frequency
    - activity from trajectory




# Trajectory file of the food choice assay

## frame anatomy

frameNumber: >object< >object<


## object anatomy


\> name, quality, x0,y0,x1,y1< 

x0: X-coordinate of the upper left corner of the bounding box normalised to image width
y0: Y-coordinate of the upper left corner of the bounding box normalised to image height
x0: X-coordinate of the lower right corner of the bounding box
y0: Y-coordinate of the lower right of the bounding box

# Examples:

## example entry of the trajectory file

0 : >fly,1.0,0.0314725823700428,0.7674427628517151,0.07034310698509216,0.7858083248138428< >fly,1.0,0.08977020531892776,0.040684815496206284,0.11528601497411728,0.07760496437549591< >arena,0.9999550580978394,0.4522370398044586,0.8178274631500244,0.5609667897224426,0.9818180203437805< >arena,0.9999526739120483,0.775743842124939,0.8145774006843567,0.8738982081413269,0.9783108234405518<

## example animal tracing

\>fly,1.0,0.0314725823700428,0.7674427628517151,0.07034310698509216,0.7858083248138428< 

        x0,y0------
        |         |
        | ._q0p_. |
        | '=(_)=' |
        |  / V \  |
        | (_/^\_) |
        |         |
        |-----x1,y1
