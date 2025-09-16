import time

class LoopTick:
    """循环计时器，用于测量每次循环及总耗时"""
    NS2MS  = 1 / 1_000_000
    NS2SEC = 1 / 1_000_000_000

    def __init__(self, auto_report=True, init_sec=None, unit="ns"):
        """
        :param auto_report: True 时，在退出上下文时自动打印总耗时和平均耗时
        :param init_sec: 初始化秒数，用于第一次调用tick时返回的默认值
        :param unit: 默认单位，可选值: "ns", "ms", "sec"
        """
        self._last_time = None
        self._total_time_ns = 0
        self._count = 0
        self.auto_report = auto_report
        self._init_ns = init_sec * 1_000_000_000 if init_sec is not None else None
        self._default_unit = unit
        self._timestamps = {}  # 存储标签时间戳

    def __call__(self, **kwargs):
        """ 添加 call 方法精简调用语法"""
        return self.tick(**kwargs)

    def tick(self, first=False, last=False, tag=None):
        """
        记录一次循环，返回本次循环耗时
        
        :param first: 标记为第一次调用，用于精确计算开始时间
        :param last: 标记为最后一次调用，用于精确计算结束时间
        :param tag: 时间戳标签，可用于后续计算时间差
        :return: 本次循环耗时（默认纳秒）
        """
        now = time.time_ns()
        
        # 如果提供了标签，保存时间戳
        if tag is not None:
            self._timestamps[tag] = now
            
        # 处理 first 标记
        if first:
            self._last_time = now
            # 如果设置了初始值，返回初始纳秒数，否则返回极小值
            result = self._init_ns if self._init_ns is not None else 0.000_001
            return result
            
        if self._last_time is None:
            self._last_time = now
            # 如果设置了初始值，返回初始纳秒数，否则返回极小值
            result = self._init_ns if self._init_ns is not None else 0.000_001
            return result
            
        diff = now - self._last_time
        
        # 处理 last 标记
        if last:
            self._last_time = None  # 重置以便下次重新开始
        else:
            self._last_time = now
            
        self._total_time_ns += diff
        self._count += 1
        return diff

    def reset(self):
        """重置计时器"""
        self._last_time = None
        self._total_time_ns = 0
        self._count = 0
        self._timestamps.clear()

    @property
    def total_ns(self):
        return self._total_time_ns

    @property
    def total_ms(self):
        return self.total_ns * self.NS2MS
    
    @property
    def total_sec(self):
        return self._total_time_ns * self.NS2SEC
    
    @property
    def average_ns(self):
        return self._total_time_ns / self._count if self._count else 0

    @property
    def average_ms(self):
        return self.average_ns * self.NS2MS
    
    @property
    def average_sec(self):
        return self.average_ns * self.NS2SEC

    def spend_time(self, start, end, unit="ns"):
        """
        计算两个标签之间的时间差
        
        :param start: 起始标签
        :param end: 结束标签
        :param unit: 返回单位，可选值: "ns", "ms", "sec"
        :return: 时间差
        """
        if start not in self._timestamps:
            raise ValueError(f"起始标签 '{start}' 不存在")
        if end not in self._timestamps:
            raise ValueError(f"结束标签 '{end}' 不存在")
            
        diff_ns = self._timestamps[end] - self._timestamps[start]
        
        if unit == "ns":
            return diff_ns
        elif unit == "ms":
            return diff_ns * self.NS2MS
        elif unit == "sec":
            return diff_ns * self.NS2SEC
        else:
            raise ValueError("单位必须是 'ns', 'ms', 或 'sec' 之一")

    def loop_time(self, unit="ns"):
        """
        返回 first -> last 的时间（基于_total_time_ns）
        
        :param unit: 返回单位，可选值: "ns", "ms", "sec"
        :return: 循环总时间
        """
        if unit == "ns":
            return self._total_time_ns
        elif unit == "ms":
            return self.total_ms
        elif unit == "sec":
            return self.total_sec
        else:
            raise ValueError("单位必须是 'ns', 'ms', 或 'sec' 之一")

    # 单位转换方法
    def tick_ns(self, **kwargs):
        """返回纳秒单位的时间差"""
        return self.tick(**kwargs)
        
    def tick_ms(self, **kwargs):
        """返回毫秒单位的时间差"""
        return self.tick(**kwargs) * self.NS2MS
        
    def tick_sec(self, **kwargs):
        """返回秒单位的时间差"""
        return self.tick(**kwargs) * self.NS2SEC

    def __enter__(self):
        self.reset()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.auto_report:
            print(f"总耗时: {self.total_sec:.6f} 秒")
            print(f"平均耗时: {self.average_ms:.6f} ms")



if __name__ == "__main__":
    # 普通方式
    looptick = LoopTick()

    for i in range(10):
        diff = looptick.tick()
        print(f"第 {i} 次循环耗时: {diff * looptick.NS2MS:.6f} ms")
        time.sleep(0.001)
    
    print(f"总耗时: {looptick.total_sec:.6f} 秒")
    print(f"平均耗时: {looptick.average_ms:.6f} ms")
    

    # 用上下文管理器方式
    with LoopTick() as looptick:
        for i in range(10):
            diff = looptick.tick()
            print(f"第 {i} 次循环耗时: {diff * looptick.NS2MS:.6f} ms")
            time.sleep(0.001)

    # 测试新功能
    print("\n=== 测试 first/last 标记 ===")
    loop_tick = LoopTick()
    start = loop_tick.tick(first=True)
    time.sleep(0.001)  # 模拟中间处理用时
    tick_1 = loop_tick.tick()
    time.sleep(0.001)  # 模拟中间处理用时
    end = loop_tick.tick(last=True)
    loop_time = loop_tick.loop_time("ms")  # 返回 first -> last 的时间
    print(f"循环时间: {loop_time:.6f} ms")

    print("\n=== 测试标签功能 ===")
    loop_tick = LoopTick()
    start = loop_tick.tick(tag="task_start")
    time.sleep(0.001)  # 模拟中间处理用时
    tick_1 = loop_tick.tick(tag="task_1_finish")
    time.sleep(0.001)  # 模拟中间处理用时
    tick_2 = loop_tick.tick(tag="task_2_finish")
    time.sleep(0.001)  # 模拟中间处理用时
    end = loop_tick.tick(tag="all_task_finish")
    # 返回 task_start -> task_2_finish 的时间
    start_to_tick_2 = loop_tick.spend_time(start="task_start", end="task_2_finish", unit="ms")
    print(f"task_start 到 task_2_finish 时间: {start_to_tick_2:.6f} ms")

    print("\n=== 测试初始化秒数 ===")
    loop_tick = LoopTick(init_sec=0.01)
    loop_time = loop_tick.tick()  # 当前第一次调用时, 返回 0.01 秒(10ms)
    hz = 1 / (loop_time * loop_tick.NS2SEC)  # 未设置 init_sec 时返回 0.01
    print(f"当前循环用时 {loop_time} ns, 帧率: {hz:.2f} Hz")

    print("\n=== 测试单位转换 ===")
    loop_tick = LoopTick(unit="sec")
    start = loop_tick.tick()  # 默认返回设置的单位: sec
    time.sleep(0.001)  # 模拟中间处理用时
    tick_1 = loop_tick.tick_sec()  # 也能直接用指定单位的函数:
    time.sleep(0.001)  # 模拟中间处理用时
    tick_2 = loop_tick.tick_ns()  # 返回 ns
    time.sleep(0.001)  # 模拟中间处理用时
    end = loop_tick.tick_ms()  # 返回 ms
    print(f"tick()返回: {start} sec")
    print(f"tick_sec()返回: {tick_1} sec")
    print(f"tick_ns()返回: {tick_2} ns")
    print(f"tick_ms()返回: {end} ms")