"""Agent that uses tools."""

from tools.calculator_tool import calculate

class ToolAgent:
    def use_calculator(self, expr: str) -> float:
        return calculate(expr)
