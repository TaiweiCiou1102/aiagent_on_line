from mcp.server.fastmcp import FastMCP
import tools
import tools.geoencoding 

mcp = FastMCP()
mcp.add_tool(tools.geoencoding.get_coordinates)

def main():
    mcp.run("stdio")

if __name__ == "__main__":
    main()