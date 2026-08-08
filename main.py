from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(
    title="Calculator API",
    description=(
        "A simple FastAPI calculator supporting addition, subtraction, "
        "multiplication, and division."
    ),
    version="1.0.0",
)


class CalculationRequest(BaseModel):
    a: float = Field(..., description="First number", examples=[10])
    b: float = Field(..., description="Second number", examples=[5])
    operator: str = Field(
        ...,
        description="Operator: +, -, *, or /",
        examples=["+"],
    )


@app.get("/")
def home() -> dict:
    return {
        "message": "Calculator API is running.",
        "docs": "/docs",
        "endpoint": "/calculate",
    }


@app.post("/calculate")
def calculate(data: CalculationRequest) -> dict:
    if data.operator == "+":
        result = data.a + data.b

    elif data.operator == "-":
        result = data.a - data.b

    elif data.operator == "*":
        result = data.a * data.b

    elif data.operator == "/":
        if data.b == 0:
            raise HTTPException(
                status_code=400,
                detail="Division by zero is not allowed.",
            )
        result = data.a / data.b

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid operator. Use +, -, *, or /.",
        )

    return {
        "a": data.a,
        "b": data.b,
        "operator": data.operator,
        "result": result,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
