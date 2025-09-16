import time

class LoopTick:
    """ 循环计时器，用于测量每次循环及总耗时"""
    NS2MS  = 1 / 1_000_000
    NS2SEC = 1 / 1_000_000_000

    def __init__(self, first_tick=0.01, auto_report=True):
        """ 
        :param auto_report: True 时，在退出上下文时自动打印总耗时和平均耗时
        """ 
        self._last_time = None
        self._total_time_ns = 0
        self._count = 0
        self._diff_ns = 0
        self._first_tick = first_tick
        self.auto_report = auto_report

    def __call__(self):
        """  添加 call 方法精简调用语法 """
        return self.tick()

    def tick(self):
        """ 记录一次循环，返回本次循环耗时（ns）"""
        now = time.time_ns()
        if self._last_time is None:
            self._last_time = now
            return self._first_tick   # 避免除零
        self._diff_ns = now - self._last_time
        self._last_time = now
        self._total_time_ns += self._diff_ns 
        self._count += 1
        return self._diff_ns 
    
    @property
    def tick_ms(self):
        """ 记录一次循环，返回本次循环耗时（ms）"""
        return self.tick() * self.NS2MS
    
    @property
    def tick_sec(self):
        """ 记录一次循环，返回本次循环耗时（s）"""
        return self.tick() * self.NS2SEC
    
    @property
    def get_hz(self):
        """ 查询当前帧率（hz） , 不更新 tick"""
        return 1 / (self._diff_ns * self.NS2SEC)

    @property
    def get_avg_hz(self):
        """ 获取平均帧率（hz）, 不更新 tick """
        return 1 / self.average_sec

    def reset(self):
        """ 重置计时器 """
        self._last_time = None
        self._total_time_ns = 0
        self._count = 0

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

    def __enter__(self):
        self.reset()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.auto_report:
            print(f"总耗时: {self.total_sec:.6f} 秒")
            print(f"平均耗时: {self.average_ms:.6f} ms")
            print(f"平均Hz: {self.get_avg_hz:.6f} Hz")
            print(f"总次数: {self._count}")




if __name__ == "__main__":
    # 普通方式
    looptick = LoopTick()

    for i in range(10):
        diff = looptick.tick()
        print(f"第 {i} 次循环耗时: {diff * looptick.NS2MS:.6f} ms")
        time.sleep(0.001)
    
    print(f"总耗时: {looptick.total_sec:.6f} 秒")
    print(f"平均耗时: {looptick.average_ms:.6f} ms")
    print(f"平均Hz: {looptick.get_avg_hz:.6f} Hz")
    

    # 用上下文管理器方式
    with LoopTick() as looptick:
        for i in range(10):
            diff = looptick.tick()
            print(f"第 {i} 次循环耗时: {diff * looptick.NS2MS:.6f} ms")
            time.sleep(0.001)

    while True:
        time.sleep(0.1)
        pass

