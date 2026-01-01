import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = anthropic.Anthropic()

# File creation tool
tools = [
    {
        "name": "create_file",
        "description": "Create a new file with content",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "File path (e.g., 'main.py' or 'src/utils.py')"
                },
                "content": {
                    "type": "string",
                    "description": "Complete file content"
                }
            },
            "required": ["path", "content"]
        }
    }
]

created_files = []

def execute_tool(tool_name, tool_input):
    """Execute the requested tool"""
    if tool_name == "create_file":
        path = tool_input['path']
        content = tool_input['content']
        
        try:
            # Create directory if needed
            directory = os.path.dirname(path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            
            # Write file
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            created_files.append(path)
            file_size = len(content)
            return f"Successfully created {path} ({file_size} characters)"
        
        except Exception as e:
            return f"Error creating {path}: {str(e)}"
    
    return f"Unknown tool: {tool_name}"

# Load prompt
with open('calorie_tracker_prompt.txt', 'r', encoding='utf-8') as f:
    prompt = f.read()

messages = [{
    "role": "user",
    "content": f"""{prompt}

You have access to a create_file tool. Use it to create ALL necessary files for the Calorie Tracker application.

Important:
1. Create each file using the create_file tool
2. Include complete, working code in each file
3. After creating all files, send a final message confirming completion
4. Do not output code in markdown - only use the create_file tool"""
}]

print("🤖 Claude is building the Calorie Tracker...\n")
print("="*60 + "\n")

max_iterations = 50  # Prevent infinite loops
iteration = 0

while iteration < max_iterations:
    iteration += 1
    
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            thinking={
                "type": "enabled",
                "budget_tokens": 2000
            },
            tools=tools,
            messages=messages
        )
    except Exception as e:
        print(f"❌ API Error: {e}")
        break
    
    # Print thinking if present
    for block in response.content:
        if block.type == "thinking":
            print(f"[Claude is thinking: {block.thinking[:100]}...]")
    
    # Check stop reason
    if response.stop_reason == "end_turn":
        # Claude is done - print any final text
        for block in response.content:
            if block.type == "text":
                print(f"\n💬 {block.text}\n")
        break
    
    elif response.stop_reason == "tool_use":
        # Add assistant's response to conversation
        messages.append({"role": "assistant", "content": response.content})
        
        # Extract and execute tool calls
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"🔧 Creating: {block.input.get('path', 'unknown')}")
                
                # Execute the tool
                result = execute_tool(block.name, block.input)
                print(f"   {result}")
                
                # Store result to send back to Claude
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })
        
        # Send tool results back to Claude
        messages.append({"role": "user", "content": tool_results})
    
    elif response.stop_reason == "max_tokens":
        print("⚠️  Warning: Response hit max_tokens limit. Continuing...")
        # Add response and continue - might need to increase max_tokens
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": "Please continue creating the remaining files."})
    
    else:
        print(f"⚠️  Unexpected stop_reason: {response.stop_reason}")
        break

if iteration >= max_iterations:
    print(f"\n⚠️  Reached maximum iterations ({max_iterations})")

print("\n" + "="*60)
print(f"✅ Complete! Created {len(created_files)} files")
print("="*60 + "\n")

if created_files:
    print("Created files:")
    for f in created_files:
        print(f"  • {f}")
    
    print("\n📁 Next steps:")
    print("  1. pip install -r requirements.txt")
    print("  2. python main.py")
else:
    print("⚠️  No files were created. Check the output above for errors.")