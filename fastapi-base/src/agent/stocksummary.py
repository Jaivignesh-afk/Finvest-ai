import os
import yfinance as yf
from langchain.tools import tool
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from nsepython import nse_eq


# =========================
# 1️⃣ Python functions
# =========================
def yfinance_func(symbol: str) -> str:
    """Return current stock price for an NSE symbol."""
    if not symbol.endswith(".NS"):
        symbol += ".NS"
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d")
    if not data.empty:
        price = round(data["Close"].iloc[-1], 2)
        return f"The current stock price of {symbol} is ₹{price}"
    return f"Couldn't fetch live price for {symbol}"


def financial_summary_func(symbol: str, fields: list[str] = None) -> str:
    """Fetch Market Cap, EPS, and P/E Ratio from NSE or yfinance."""
    nse_pe = None
    try:
        print(f"🟡 Fetching NSE data for {symbol}...")
        info = nse_eq(symbol)
        data = info.get("metadata", {})
        print("✅ NSE metadata keys:", list(data.keys()))
        nse_pe = data.get("pdSymbolPe") or data.get("pdSectorPe")
    except Exception as e:
        print(f"⚠️ NSE fetch failed for {symbol}: {e}")

    # Always use yfinance for EPS and Market Cap to ensure coverage
    print("🔵 Fetching Yahoo Finance data...")
    if not symbol.endswith(".NS"):
        symbol += ".NS"
    stock = yf.Ticker(symbol)
    info = stock.info
    print("✅ yfinance info keys:", list(info.keys())[:15])

    eps = info.get("trailingEps", "N/A")
    pe_ratio = nse_pe or info.get("trailingPE", "N/A")
    market_cap = info.get("marketCap", "N/A")
    dividend_yield = info.get("dividendYield", "N/A")

    if isinstance(market_cap, (int, float)):
        market_cap = f"₹{market_cap:,.0f}"

    return f"Market Cap: {market_cap}\nEPS: {eps}\nP/E Ratio: {pe_ratio}\nDividend Yield: {dividend_yield}"



def calculator_func(expression: str) -> str:
    """Perform simple math calculations."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"


# =========================
# 2️⃣ LangChain Tools
# =========================
yfinance_tool = tool(yfinance_func)
financial_summary_tool = tool(financial_summary_func)
calculator_tool = tool(calculator_func)

tools = [yfinance_tool, financial_summary_tool, calculator_tool]

# =========================
# 3️⃣ LLM setup
# =========================
llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
    temperature=0.2,
    max_new_tokens=400,
)

chat = ChatHuggingFace(llm=llm)
chat_with_tools = chat.bind_tools(tools)

# =========================
# 4️⃣ Query handler
# =========================
def handle_query(query: str) -> str:
    response = chat_with_tools.invoke(query)
    tool_calls = response.additional_kwargs.get("tool_calls", [])
    if not tool_calls:
        return response.content
    final_output = ""
    for call in tool_calls:
        tool_obj = next((t for t in tools if t.name == call["function"]["name"]), None)
        if tool_obj:
            args = eval(call["function"]["arguments"])
            final_output += tool_obj.func(**args) + "\n"
        else:
            final_output += f"Unknown tool: {call['function']['name']}\n"
    return final_output.strip()

# =========================
# 5️⃣ Example
# =========================
queries = ["Give me the Dividend Yield of RELIANCE"]

for q in queries:
    print(f"\n💬 User: {q}")
    print("🤖 Bot:", handle_query(q))
