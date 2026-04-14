from agents.supervisor_graph import run_supervisor

print("Testing Guardian Graph...")
try:
    result = run_supervisor("test message")
    print(result)
except Exception as e:
    import traceback
    traceback.print_exc()
