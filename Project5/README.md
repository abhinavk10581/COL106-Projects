# 🏛️ Stock Span & Trade Analyzer

A comprehensive stock analysis tool that implements advanced data structures and algorithms for technical analysis and trading signal generation.

## 🔍 Features

### Algorithms Implemented
- **Monotonic Stack**: Stock span calculation (O(n) time complexity)
- **Greedy Algorithm**: Buy/sell signal generation for maximum profit
- **Fixed-Size Queue**: Moving average calculation with sliding window
- **Sliding Window**: Volatility and risk analysis
- **Kadane's Algorithm Variant**: Maximum single trade profit calculation
- **Anomaly Detection**: Price deviation analysis

### Analysis Types
- 📊 **Stock Span Analysis**: Identifies price trends and momentum
- 💰 **Buy/Sell Signals**: Optimal trading decisions using greedy approach
- 📈 **Moving Average**: Technical indicator with configurable window
- 🔍 **Sliding Window Analysis**: Risk assessment and volatility measurement
- 🎯 **Maximum Profit Calculation**: Best single trade opportunity
- 🚨 **Anomaly Detection**: Unusual price movements identification

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- No external dependencies required (uses standard library only)

### Installation
```bash
git clone <repository-url>
cd stock-analyzer
```

### Running the Application
```bash
python main.py
```

### Usage Example
```
🏛️  STOCK SPAN & TRADE ANALYZER
🔍 Advanced Technical Analysis using Data Structures & Algorithms
📈 Implementing: Stacks, Queues, Sliding Window, Greedy Algorithms

INPUT CONFIGURATION
Use sample data? (y/n): y
Using sample prices: [100, 80, 60, 70, 60, 75, 85, 90, 65, 95, 105, 95]
Enter window size for moving average (default 3): 3
```

## 📁 Project Structure

```
stock-analyzer/
│
├── main.py              # Entry point and user interface
├── stock_analyzer.py    # Core analysis engine with all algorithms
├── requirements.txt     # Dependencies (optional enhancements)
└── README.md           # This documentation
```

## 🔧 Technical Details

### Time & Space Complexity
| Algorithm | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Stock Span | O(n) | O(n) |
| Buy/Sell Signals | O(n) | O(1) |
| Moving Average | O(n) | O(k) |
| Sliding Window | O(n) | O(k) |
| Max Profit | O(n) | O(1) |

### Data Structures Used
- **Stack**: For monotonic stack in span calculation
- **Deque**: For fixed-size queue in moving average
- **Lists**: For sliding window operations
- **Dictionary**: For structured data storage

## 📊 Sample Output

### Stock Span Analysis
```
📊 STOCK SPAN ANALYSIS (Monotonic Stack)
Day   Price    Span   Stack State     Trend
------------------------------------------------------------
1     $100     1      []              NEUTRAL ➡️
2     $80      1      [100.0]         DOWN ↘️
3     $60      1      [100.0, 80.0]   DOWN ↘️
4     $70      2      [100.0, 80.0]   UP ↗️
```

### Buy/Sell Signals
```
💰 BUY/SELL SIGNALS (Greedy Algorithm)
Day   Price    Action     Profit     Total P/L    Logic
----------------------------------------------------------------------
1     $100     HOLD ⏸️    $0.00      $0.00        No profitable opportunity
2     $80      HOLD ⏸️    $0.00      $0.00        No profitable opportunity
3     $60      BUY 🟢     $0.00      $0.00        Price will rise: 60.0 → 70.0
4     $70      HOLD ⏸️    $0.00      $0.00        No profitable opportunity
```

## 🎯 Use Cases

### For Traders
- **Technical Analysis**: Identify trends and momentum
- **Signal Generation**: Automated buy/sell recommendations
- **Risk Assessment**: Volatility and risk level analysis
- **Profit Optimization**: Maximum profit opportunity identification

### For Developers
- **Algorithm Study**: Practical implementation of data structures
- **Performance Analysis**: Time/space complexity examples
- **Code Learning**: Clean, well-documented Python code
- **Extension Base**: Foundation for more complex trading systems

### For Students
- **Data Structures**: Real-world application of stacks, queues, sliding windows
- **Algorithm Design**: Greedy algorithms and dynamic programming variants
- **Complexity Analysis**: Understanding Big O notation in practice
- **Problem Solving**: Financial domain problem-solving techniques

## 🔄 Customization

### Adding New Indicators
1. Add method to `StockAnalyzer` class
2. Follow existing pattern for console output
3. Include complexity analysis comments
4. Update summary method

### Modifying Window Sizes
- Moving average window size is configurable via user input
- Sliding window size can be modified in the analysis methods
- Risk thresholds can be adjusted in the risk assessment logic

### Extending Analysis
- Add new trading strategies
- Implement additional technical indicators
- Include backtesting capabilities
- Add data visualization features

## 📈 Performance Characteristics

### Optimizations
- **Monotonic Stack**: Amortized O(1) operations
- **Sliding Window**: Constant space with configurable window
- **Greedy Algorithm**: Single-pass optimization
- **Memory Efficient**: Minimal space usage for large datasets

### Scalability
- Handles large price datasets efficiently
- Linear time complexity for most operations
- Configurable parameters for different market conditions
- Extensible architecture for additional features

## 🤝 Contributing

Feel free to contribute by:
- Adding new technical indicators
- Improving algorithm efficiency
- Enhancing user interface
- Adding data visualization
- Writing tests and documentation

## 📝 License

This project is for educational and research purposes. Use responsibly and at your own risk for actual trading decisions.

---

**Note**: This analyzer is for educational purposes. Always consult with financial professionals before making investment decisions.