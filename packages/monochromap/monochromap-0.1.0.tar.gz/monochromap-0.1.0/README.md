# MonochroMap

A compact library to paint and plot black and white map. Inspired and continued from [StaticMap](https://github.com/komoot/staticmap).


## Example
### Draw Lines
This example code will show the location of Laugh Tale from intersection of coordinates given by road poneglyph.

```python
m = MonochroMap()
line = Line(((13.4, 52.5), (2.3, 48.9)), '#ff000088', 15)
m.add_feature(line)

line = Line(((4.9041, 52.3676), (7.27, 46.57)), '#0000ff88', 15)
m.add_feature(line)
image = m.render()
```
![laugh Tale location](/samples/laugh_tale.png?raw=true)

### Draw Points


### Draw (any) Polygon


### Draw Icon (random image)


### License
StaticMap is open source and licensed under Apache License, Version 2.0

The map samples on this page are made with [OSM](http://www.osm.org) data, © [OpenStreetMap](http://www.openstreetmap.org/copyright) contributors
