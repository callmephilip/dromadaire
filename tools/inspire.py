import asyncio, subprocess, os, sys
from gitingest import ingest_async
from json import loads

def ask_gemini(prompt):
    """Execute gemini-cli with the given prompt and return the result."""
    cmd = ["npx", "--yes", "https://github.com/google-gemini/gemini-cli", "-p", prompt]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"

async def ingest():
    """Load inspiration data from all configured sources."""
    # read the inspiration file
    with open("tools/inspiration.json", "r") as f:
        inspiration = loads(f.read())
    
    tasks = [
        ingest_async(
            insp["gh"],
            include_patterns=",".join(insp.get("include_patterns", [])),
            exclude_patterns=",".join(insp.get("exclude_patterns", [])),
        )
        for insp in inspiration
    ]
    results = await asyncio.gather(*tasks)
    return results

def main():
    if len(sys.argv) != 2:
        print("Usage: python tools/inspire.py \"your question here\"")
        sys.exit(1)
    
    if "GEMINI_API_KEY" not in os.environ: raise ValueError("GEMINI_API_KEY environment variable is not set.")
    
    question = sys.argv[1]
    
    # Load inspiration data
    results = asyncio.run(ingest())
    results_str = ""
    for summary, tree, content in results:
        results_str += f"Summary: {summary}\n\nTree:\n{tree}\n\nContent:\n{content}\n\n"
    
    # Create prompt with context and question
    prompt = f"""
    You are expert at identifying relevant parts a large codebase and providing concise summaries and code snippets.
    Give codebase below and the question, provide a concise answer to the question based on the codebase including relevant code snippets.

    # Codebase:
    
    {results_str}
    
    # Question:
    
    {question}
    """
    
    # Get answer from Gemini
    answer = ask_gemini(prompt)
    print(answer)

if __name__ == "__main__":
    main()