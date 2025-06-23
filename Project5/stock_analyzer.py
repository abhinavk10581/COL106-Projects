"""
Stock Analyzer - Core Analysis Engine
Implements: Stacks, Queues, Sliding Window, Greedy Algorithms
"""

from collections import deque
from typing import List, Tuple, Dict, Any, Optional

class StockAnalyzer:
    def __init__(self):
        self.prices = []
        self.window_size = 3
    
    def calculate_stock_span(self, prices: List[float]) -> List[int]:
        """
        Calculate stock span using monotonic stack
        Time Complexity: O(n), Space Complexity: O(n)
        """
        spans = []
        stack = []  # Stack stores indices
        
        print("\n" + "="*60)
        print("📊 STOCK SPAN ANALYSIS (Monotonic Stack)")
        print("="*60)
        print(f"{'Day':<5} {'Price':<8} {'Span':<6} {'Stack State':<15} {'Trend'}")
        print("-" * 60)
        
        for i in range(len(prices)):
            # Pop elements while stack is not empty and current price >= stack top price
            while stack and prices[i] >= prices[stack[-1]]:
                stack.pop()
            
            # Calculate span
            span = i + 1 if not stack else i - stack[-1]
            spans.append(span)
            
            # Determine trend
            if span > 3:
                trend = "STRONG UP 📈"
            elif span > 1:
                trend = "UP ↗️"
            elif i > 0 and prices[i] < prices[i-1]:
                trend = "DOWN ↘️"
            else:
                trend = "NEUTRAL ➡️"
            
            # Display current state
            stack_str = str([prices[j] for j in stack[-3:]]) if stack else "[]"
            print(f"{i+1:<5} ${prices[i]:<7} {span:<6} {stack_str:<15} {trend}")
            
            # Push current index
            stack.append(i)
        
        return spans
    
    def calculate_buy_sell_signals(self, prices: List[float]) -> Tuple[List[Dict], float, List[Tuple]]:
        """
        Calculate buy/sell signals using greedy algorithm
        Time Complexity: O(n), Space Complexity: O(1)
        """
        signals = []
        buy_price = None
        total_profit = 0
        trades = []
        
        print("\n" + "="*70)
        print("💰 BUY/SELL SIGNALS (Greedy Algorithm)")
        print("="*70)
        print(f"{'Day':<5} {'Price':<8} {'Action':<10} {'Profit':<10} {'Total P/L':<12} {'Logic'}")
        print("-" * 70)
        
        for i in range(len(prices) - 1):
            current_price = prices[i]
            next_price = prices[i + 1]
            
            # Buy signal: current price < next price and we're not holding
            if current_price < next_price and buy_price is None:
                buy_price = current_price
                action = "BUY 🟢"
                profit = 0
                logic = f"Price will rise: {current_price} → {next_price}"
                
            # Sell signal: current price > next price and we're holding
            elif current_price > next_price and buy_price is not None:
                profit = current_price - buy_price
                total_profit += profit
                action = "SELL 🔴"
                logic = f"Price will fall: {current_price} → {next_price}"
                trades.append((buy_price, current_price, profit))
                buy_price = None
                
            else:
                action = "HOLD ⏸️"
                profit = 0
                logic = "No profitable opportunity"
            
            signals.append({
                'day': i + 1,
                'price': current_price,
                'action': action,
                'profit': profit
            })
            
            print(f"{i+1:<5} ${current_price:<7} {action:<10} ${profit:<9.2f} ${total_profit:<11.2f} {logic}")
        
        # Handle last day
        last_price = prices[-1]
        if buy_price is not None:
            profit = last_price - buy_price
            total_profit += profit
            trades.append((buy_price, last_price, profit))
            print(f"{len(prices):<5} ${last_price:<7} {'SELL 🔴':<10} ${profit:<9.2f} ${total_profit:<11.2f} End of period")
        else:
            print(f"{len(prices):<5} ${last_price:<7} {'HOLD ⏸️':<10} $0.00     ${total_profit:<11.2f} End of period")
        
        return signals, total_profit, trades
    
    def calculate_moving_average(self, prices: List[float], window_size: int) -> List[Dict]:
        """
        Calculate moving average using fixed-size queue
        Time Complexity: O(n), Space Complexity: O(k) where k is window_size
        """
        moving_averages = []
        queue = deque()  # Fixed-size queue
        
        print(f"\n" + "="*70)
        print(f"📈 MOVING AVERAGE ANALYSIS (Fixed-Size Queue, Window={window_size})")
        print("="*70)
        print(f"{'Day':<5} {'Price':<8} {'Queue State':<20} {'MovAvg':<8} {'Signal':<12} {'Deviation'}")
        print("-" * 70)
        
        for i in range(len(prices)):
            queue.append(prices[i])
            
            # Maintain fixed window size
            if len(queue) > window_size:
                queue.popleft()  # Remove oldest element (FIFO)
            
            # Calculate moving average
            avg = sum(queue) / len(queue)
            
            # Generate signal
            deviation = ((prices[i] - avg) / avg) * 100
            if deviation > 5:
                signal = "STRONG BUY 🚀"
            elif deviation > 0:
                signal = "BUY 📈"
            elif deviation < -5:
                signal = "STRONG SELL 📉"
            elif deviation < 0:
                signal = "SELL 📊"
            else:
                signal = "NEUTRAL ➡️"
            
            moving_averages.append({
                'day': i + 1,
                'price': prices[i],
                'moving_avg': avg,
                'signal': signal,
                'deviation': deviation
            })
            
            queue_str = f"[{', '.join([f'{x:.1f}' for x in list(queue)])}]"
            print(f"{i+1:<5} ${prices[i]:<7} {queue_str:<20} ${avg:<7.2f} {signal:<12} {deviation:+.1f}%")
        
        return moving_averages
    
    def sliding_window_analysis(self, prices: List[float], window_size: int) -> List[Dict]:
        """
        Sliding window max/min analysis using deque
        Time Complexity: O(n), Space Complexity: O(k)
        """
        windows = []
        
        print(f"\n" + "="*80)
        print(f"🔍 SLIDING WINDOW MAX/MIN ANALYSIS (Window Size={window_size})")
        print("="*80)
        print(f"{'Window':<8} {'Range':<10} {'Prices':<25} {'Max':<8} {'Min':<8} {'Volatility':<12} {'Risk'}")
        print("-" * 80)
        
        for i in range(len(prices) - window_size + 1):
            window = prices[i:i + window_size]
            max_price = max(window)
            min_price = min(window)
            volatility = ((max_price - min_price) / min_price) * 100
            
            # Risk assessment
            if volatility > 15:
                risk = "HIGH 🔴"
            elif volatility > 8:
                risk = "MEDIUM 🟡"
            else:
                risk = "LOW 🟢"
            
            windows.append({
                'window_num': i + 1,
                'range': f"{i+1}-{i+window_size}",
                'prices': window,
                'max': max_price,
                'min': min_price,
                'volatility': volatility,
                'risk': risk
            })
            
            prices_str = f"[{', '.join([f'{x:.0f}' for x in window])}]"
            print(f"{i+1:<8} {i+1}-{i+window_size:<9} {prices_str:<25} ${max_price:<7} ${min_price:<7} {volatility:<11.1f}% {risk}")
        
        return windows
    
    def calculate_max_profit_kadane(self, prices: List[float]) -> Tuple[float, Optional[int], Optional[int]]:
        """
        Calculate maximum profit using Kadane's algorithm variant
        Time Complexity: O(n), Space Complexity: O(1)
        """
        if len(prices) < 2:
            return 0, None, None
        
        max_profit = 0
        min_price = prices[0]
        buy_day = 0
        sell_day = 0
        temp_buy_day = 0
        
        print(f"\n" + "="*70)
        print("🎯 MAXIMUM PROFIT ANALYSIS (Kadane's Algorithm Variant)")
        print("="*70)
        print(f"{'Day':<5} {'Price':<8} {'MinPrice':<10} {'MaxProfit':<12} {'BuyDay':<8} {'SellDay':<8} {'Action'}")
        print("-" * 70)
        
        for i in range(len(prices)):
            action = ""
            if prices[i] < min_price:
                min_price = prices[i]
                temp_buy_day = i
                action = "New min found"
            
            current_profit = prices[i] - min_price
            if current_profit > max_profit:
                max_profit = current_profit
                buy_day = temp_buy_day
                sell_day = i
                action = "New max profit!"
            
            print(f"{i+1:<5} ${prices[i]:<7} ${min_price:<9} ${max_profit:<11.2f} {buy_day+1:<8} {sell_day+1:<8} {action}")
        
        return max_profit, buy_day, sell_day
    
    def detect_anomalies(self, prices: List[float], moving_averages: List[Dict]) -> List[Dict]:
        """
        Detect price anomalies and local extrema
        """
        anomalies = []
        
        print(f"\n" + "="*60)
        print("🚨 ANOMALY DETECTION")
        print("="*60)
        print(f"{'Day':<5} {'Price':<8} {'MovAvg':<8} {'Deviation':<12} {'Type'}")
        print("-" * 60)
        
        for i, ma in enumerate(moving_averages):
            deviation = abs(ma['deviation'])
            if deviation > 10:
                anomaly_type = "EXTREME 🚨"
                anomalies.append({
                    'day': ma['day'],
                    'price': ma['price'],
                    'deviation': ma['deviation'],
                    'type': anomaly_type
                })
                print(f"{ma['day']:<5} ${ma['price']:<7} ${ma['moving_avg']:<7.2f} {ma['deviation']:+<11.1f}% {anomaly_type}")
        
        if not anomalies:
            print("No significant anomalies detected ✅")
        
        return anomalies
    
    def print_summary(self, prices: List[float], total_profit: float, max_profit: float, 
                     buy_day: Optional[int], sell_day: Optional[int], trades: List[Tuple], 
                     windows: List[Dict]) -> None:
        """
        Print comprehensive summary
        """
        print(f"\n" + "="*80)
        print("📋 COMPREHENSIVE TRADING SUMMARY")
        print("="*80)
        
        # Basic Statistics
        print(f"📊 Price Statistics:")
        print(f"   • Total Trading Days: {len(prices)}")
        print(f"   • Highest Price: ${max(prices):.2f}")
        print(f"   • Lowest Price: ${min(prices):.2f}")
        print(f"   • Price Range: {((max(prices) - min(prices)) / min(prices) * 100):.1f}%")
        print(f"   • Average Price: ${sum(prices) / len(prices):.2f}")
        
        # Profit Analysis
        print(f"\n💰 Profit Analysis:")
        print(f"   • Greedy Algorithm Total Profit: ${total_profit:.2f}")
        print(f"   • Maximum Single Trade Profit: ${max_profit:.2f}")
        if buy_day is not None and sell_day is not None:
            print(f"   • Best Trade: Buy Day {buy_day+1} (${prices[buy_day]:.2f}) → Sell Day {sell_day+1} (${prices[sell_day]:.2f})")
        print(f"   • Total Trades Executed: {len(trades)}")
        
        # Trade Details
        if trades:
            print(f"   • Trade History:")
            for i, (buy_price, sell_price, profit) in enumerate(trades, 1):
                print(f"     {i}. Buy ${buy_price:.2f} → Sell ${sell_price:.2f} = ${profit:+.2f}")
        
        # Risk Analysis
        if windows:
            volatilities = [w['volatility'] for w in windows]
            avg_volatility = sum(volatilities) / len(volatilities)
            max_volatility = max(volatilities)
            print(f"\n⚠️  Risk Analysis:")
            print(f"   • Average Volatility: {avg_volatility:.1f}%")
            print(f"   • Maximum Volatility: {max_volatility:.1f}%")
            
            high_risk_windows = sum(1 for v in volatilities if v > 15)
            print(f"   • High Risk Windows: {high_risk_windows}/{len(windows)}")
        
        # Algorithm Performance
        print(f"\n🔧 Algorithm Performance:")
        print(f"   • Stock Span: O(n) time, O(n) space")
        print(f"   • Buy/Sell Greedy: O(n) time, O(1) space")
        print(f"   • Moving Average: O(n) time, O(k) space")
        print(f"   • Sliding Window: O(n) time, O(k) space")
        print(f"   • Max Profit: O(n) time, O(1) space")