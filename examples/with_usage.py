from looptick import LoopTick
import time

def main():
    with LoopTick() as timer:
        for i in range(5):
            diff = timer.tick()
            print(f"第 {i} 次循环耗时: {diff * timer.NS2MS:.6f} ms")
            time.sleep(0.01)

if __name__ == "__main__":
    main()
