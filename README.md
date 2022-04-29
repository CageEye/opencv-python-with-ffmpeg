### How to build linux 64b custom version of opencv with ffmpeg? 


go to `find_version.py` and edit line 65 
```python
    f.write('opencv_version = "{}"\n'.format("4.6.0"))
```
(bump version you want to publish) 

then 

```shell
docker build --build-arg REPO_PWD=***** . -t opencv-build 
```


```shell
docker run -it opencv-build  bash
```

Inside the container run 

```shell
pip wheel . --verbose 
```

This will produce `whl` file that you need to copy to your host machine via `docker cp` 
and publish with `twine` 

