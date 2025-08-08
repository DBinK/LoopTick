from looptick import LoopTick
import time

def main():
    timer = LoopTick(auto_report=False)
    for i in range(5):
        diff = timer.tick()
        print(f"第 {i} 次循环耗时: {diff * timer.NS2MS:.6f} ms")
        time.sleep(0.01)
    print(f"总耗时: {timer.total_sec:.6f} 秒")
    print(f"平均耗时: {timer.average_ms:.6f} ms")

if __name__ == "__main__":
    main()
