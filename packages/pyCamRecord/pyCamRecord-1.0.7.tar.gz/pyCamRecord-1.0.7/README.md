__Calculate differential power of each frame in webcam stream and record while it is bigger than the presetting threshold.__ 

```python
import pyCamRecord
#filename format: "%Y%m%d%H%M%S.mp4"  ex:20210630115959.mp4 
#==>2021 06/30 11:59:59 
pyCamRecord.record(maxDuration=0.1)
#==>Auto record to file every 0.1 minute
```

```python
import pyCamRecord
#Record while the differential power is bigger than threshold (TH = 15000)
pyCamRecord.recordMove(showPower=True)
# print differential power frame by frame

```