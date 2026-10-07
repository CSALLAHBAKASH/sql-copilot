from typing import Literal, Optional
from pydantic import BaseModel, Field
from ai.generate_sql import llm

ChartType = Literal["bar", "line", "none"]


class ChartSpec(BaseModel):
    should_chart: bool
    chart_type: ChartType
    x_column: Optional[str] = None
    y_column: Optional[str] = None


chart_advisor = llm.with_structured_output(ChartSpec)

CHART_PROMPT = """A user asked: "{question}"

The query returned these columns: {columns}
Sample rows: {sample_rows}

Decide whether this result is worth charting. A single summary number or a
result with only one row is NOT worth charting (should_chart: false). A result
with a category/time column and a numeric column across multiple rows usually is.
Use "line" only when the x-axis column is clearly a date/time; otherwise "bar".
If charting, x_column and y_column must be exact column names from the list above.
"""


def suggest_chart(columns: list[str], rows: list[dict], question: str) -> ChartSpec:
    sample_rows = rows[:5]
    prompt = CHART_PROMPT.format(question=question, columns=columns, sample_rows=sample_rows)
    return chart_advisor.invoke(prompt)

if __name__ == "__main__":
    from ai.pipeline import ask_question
    import json

    print(json.dumps(ask_question("What is our total revenue?")["chart"], indent=2))
    print(json.dumps(ask_question("What's the average order value by product category?")["chart"], indent=2))
