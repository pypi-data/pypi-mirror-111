# vinset
Video inset function

This toolbox provides a commandline function that will insert a graph (defined in a CSV file) into a video 



# configuration file 

Example configuration file 

```
{ 
  "title" : "title of graph",
  
  // define the appearance of the graph 
  "position" :  { "x" : 100, 
                  "y" : 100,
                  "width" : 500,
                  "height" : 250 },                  
    
  "background" : { "fill":"black", "opacity" : 0.1 },
  "y-limit" : { "type" : "fixed", "limits" : { "lower" : -1, "upper" : +1 } },
  "t-limit" : { "type" : "time",  "width" : 100 },   // 100 seconds all the time 
      
   // This is the pointer to the actual data 
   "series" : [ { "name"  : "displacement", 
                "type"  : "file",
                "input" : "data.csv",
                "t"     : "CurrentTime",
                "y"     : "y" } ]

    
}
``
