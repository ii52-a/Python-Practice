import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import matplotlib.dates as mdates


class InvestmentPoolVisualizer:
    def __init__(self):
        # 初始化模拟数据
        self.dates = self.generate_dates(30)  # 30天的数据
        self.usdt_pool = self.generate_usdt_data()
        self.btc_pool = self.generate_btc_data()
        self.btc_price = self.generate_btc_price()

    def generate_dates(self, days):
        """生成日期序列"""
        start_date = datetime.now() - timedelta(days=days - 1)
        return [start_date + timedelta(days=i) for i in range(days)]

    def generate_usdt_data(self):
        """生成USDT资金池模拟数据"""
        base_value = 10000
        data = [base_value]

        for i in range(1, 30):
            # 模拟USDT资金池的变化（有增有减）
            change = np.random.normal(0, 200)  # 正态分布变化
            new_value = max(data[-1] + change, 1000)  # 确保不为负
            data.append(new_value)

        return data

    def generate_btc_data(self):
        """生成BTC资金池模拟数据（以BTC数量计）"""
        base_btc = 0.1
        data = [base_btc]

        for i in range(1, 30):
            # 模拟BTC数量的变化
            change = np.random.normal(0, 0.005)
            new_btc = max(data[-1] + change, 0.001)
            data.append(new_btc)

        return data

    def generate_btc_price(self):
        """生成BTC价格模拟数据"""
        base_price = 100000
        data = [base_price]

        for i in range(1, 30):
            # 模拟价格波动（随机游走）
            change_percent = np.random.normal(0, 0.03)  # 3%的日波动
            new_price = data[-1] * (1 + change_percent)
            data.append(new_price)

        return data

    def calculate_btc_value(self):
        """计算BTC资金池的美元价值"""
        return [btc * price for btc, price in zip(self.btc_pool, self.btc_price)]

    def calculate_total_assets(self):
        """计算总资产价值"""
        btc_value = self.calculate_btc_value()
        return [usdt + btc for usdt, btc in zip(self.usdt_pool, btc_value)]

    def create_pool_visualization(self):
        """创建资金池可视化图表"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial']
        plt.rcParams['axes.unicode_minus'] = False

        # 1. USDT资金池变化
        ax1.plot(self.dates, self.usdt_pool, 'g-', linewidth=2, label='USDT资金池')
        ax1.fill_between(self.dates, self.usdt_pool, alpha=0.3, color='green')
        ax1.set_title('USDT资金池变化趋势', fontsize=14, fontweight='bold')
        ax1.set_ylabel('USDT数量', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # 格式化x轴日期显示
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))

        # 2. BTC资金池变化（数量）
        ax2.plot(self.dates, self.btc_pool, 'orange', linewidth=2, label='BTC数量')
        ax2.fill_between(self.dates, self.btc_pool, alpha=0.3, color='orange')
        ax2.set_title('BTC持有数量变化', fontsize=14, fontweight='bold')
        ax2.set_ylabel('BTC数量', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax2.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))

        # 3. BTC价格变化
        ax3.plot(self.dates, self.btc_price, 'r-', linewidth=2, label='BTC价格')
        ax3.fill_between(self.dates, self.btc_price, alpha=0.3, color='red')
        ax3.set_title('BTC价格变化', fontsize=14, fontweight='bold')
        ax3.set_ylabel('价格 (USDT)', fontsize=12)
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax3.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))

        # 4. 总资产价值变化
        total_assets = self.calculate_total_assets()
        btc_value = self.calculate_btc_value()

        ax4.plot(self.dates, total_assets, 'b-', linewidth=2, label='总资产')
        ax4.plot(self.dates, self.usdt_pool, 'g--', linewidth=1, label='USDT部分')
        ax4.plot(self.dates, btc_value, 'r--', linewidth=1, label='BTC部分')
        ax4.fill_between(self.dates, total_assets, alpha=0.3, color='blue')
        ax4.set_title('总资产价值变化', fontsize=14, fontweight='bold')
        ax4.set_ylabel('总价值 (USDT)', fontsize=12)
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        ax4.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax4.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))

        plt.tight_layout()
        plt.suptitle('双币投资策略 - 资金池可视化分析', fontsize=16, fontweight='bold', y=1.02)
        plt.show()

        return fig

    def create_combined_chart(self):
        """创建合并图表，显示USDT和BTC资金池在同一图中的对比"""
        fig, ax = plt.subplots(figsize=(12, 6))

        # 计算BTC的美元价值
        btc_value = self.calculate_btc_value()
        total_assets = self.calculate_total_assets()

        # 创建堆叠区域图
        ax.stackplot(self.dates, self.usdt_pool, btc_value,
                     labels=['USDT资金池', 'BTC价值'],
                     colors=['#2ecc71', '#e74c3c'], alpha=0.7)

        # 添加总资产线
        ax.plot(self.dates, total_assets, 'b-', linewidth=2, label='总资产', color='#2980b9')

        ax.set_title('双币投资策略 - 资金池分布与总资产变化', fontsize=14, fontweight='bold')
        ax.set_ylabel('价值 (USDT)', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper left')

        # 格式化x轴
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        return fig


# 使用示例
if __name__ == "__main__":
    # 创建可视化实例
    visualizer = InvestmentPoolVisualizer()

    # 显示详细的可视化图表
    print("生成资金池可视化图表...")
    visualizer.create_pool_visualization()

    # 显示合并图表
    print("生成合并图表...")
    visualizer.create_combined_chart()

    # 打印当前状态摘要
    current_usdt = visualizer.usdt_pool[-1]
    current_btc = visualizer.btc_pool[-1]
    current_btc_price = visualizer.btc_price[-1]
    current_btc_value = current_btc * current_btc_price
    total_assets = current_usdt + current_btc_value

    print(f"\n当前状态摘要:")
    print(f"USDT资金池: {current_usdt:,.2f} USDT")
    print(f"BTC持有量: {current_btc:.6f} BTC")
    print(f"BTC当前价格: {current_btc_price:,.2f} USDT")
    print(f"BTC价值: {current_btc_value:,.2f} USDT")
    print(f"总资产价值: {total_assets:,.2f} USDT")
    print(f"资产分配: USDT {current_usdt / total_assets * 100:.1f}%, BTC {current_btc_value / total_assets * 100:.1f}%")

