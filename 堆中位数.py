import heapq

class MedianFinder:
    def __init__(self):
        self.max_heap = []  # 存较小的一半（取负实现大顶堆）
        self.min_heap = []  # 存较大的一半

    def addNum(self, num: int) -> None:
        # 1. 插入
        if not self.max_heap or num <= -self.max_heap[0]:
            heapq.heappush(self.max_heap, -num)
        else:
            heapq.heappush(self.min_heap, num)

        # 2. 平衡大小
        if len(self.max_heap) > len(self.min_heap) + 1:
            move = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, move)
        elif len(self.min_heap) > len(self.max_heap):
            move = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -move)

    def findMedian(self) -> float:
        if len(self.max_heap) > len(self.min_heap):
            return -self.max_heap[0]
        return (-self.max_heap[0] + self.min_heap[0]) / 2.0
    
