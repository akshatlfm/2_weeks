from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-first-server")

@mcp.tool()
def calculate(expression: str) -> str:
    """Evaluates a math expression like '2 + 2' or '10 * 5' and returns their result as string"""
    try:
        result=eval(expression)
    except Exception as e:
        return f"Error is:{e}"
    else:
        return str(result)

@mcp.tool()
def read_file(file_path: str) -> str:
    """Reads a file and returns its contents as a string"""
    try:
        with open(file_path,"r") as f:
            return f.read()
    except Exception as e:
        return f"Error:{e}"

if __name__ == "__main__":
    mcp.run(transport="stdio")