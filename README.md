# MeshPipeline

# Individual Tools

## Cloud Combiner

This tool combines multiple point clouds into a single cloud for further processing. Ideally, the clouds should be organized as follows: 

The **object folder** contains multiple **group folders**. A group is the result of one scanning pass (usually one rotation of the turntable). Each group folder contains individual **scan cloud files** (in the .ply format) captured during one "illumination".
e.g.:
```object_folder
├── 00
│   ├── 01.ply
│   ├── 02.ply   
├── 01
│   ├── 11.ply
│   ├── 12.ply
```
The Cloud Combiner will read all the .ply files, combine them into a single \*.ply file, and save the result.