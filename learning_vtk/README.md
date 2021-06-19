# How to use viz3d ?
#### step 1
```python
from viz3d import *
```

#### step 2
```python
if __name__ == '__main__':
    scene = Scene()
    thread_test = threading.Thread(target=thread_func_test)
    thread_test.start()
    scene.start()
```

#### step 3
```python
def thread_func_test():
    print("thread 1")
    for i in range(360):
        sleep(0.1)
        mat = np.array([[np.cos(np.radians(i)), np.sin(np.radians(i)), 0, 0],
                        [-np.sin(np.radians(i)), np.cos(np.radians(i)), 0, 0],
                        [0, 0, 1, i],
                        [0, 0, 0, 1]])
        scene.camera_callback.setMat(mat)
```
You can change the matrix here while visualizing.