import os


class AgentManager:
    def __init__(self, base_dir="runtime/agents"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def initialize_agents(self, agents="founding"):
        print(f"🔧 Loading agents: {agents}")
        # TODO: load configs or spawn AI workers
        with open(os.path.join(self.base_dir, f"{agents}.txt"), "w") as f:
            f.write("Initialized")
        print("✅ Agents initialized.")
