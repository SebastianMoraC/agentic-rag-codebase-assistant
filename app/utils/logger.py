
class TerminalColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    GRAY = '\033[90m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class PrettyLogger:
    def __init__(self, logger):
        self.logger = logger

    def info(self, message):
        if "Node:" in message:
            self.node_log(message)
        elif "Edge:" in message:
            self.edge_log(message)
        elif "HTTP Request:" in message:
            self.http_log(message)
        elif "Starting retrieval" in message:
            self.retrieval_log(message)
        elif "Context:" in message:
            self.context_log(message)
        elif "Scored result:" in message:
            self.score_log(message)
        elif "Creating agent" in message:
            self.agent_log(message, "🤖")
        elif "Invoking agent" in message:
            self.agent_log(message, "🚀")
        elif "Agent execution completed" in message:
            self.agent_log(message, "✅")
        elif "Generated" in message:
            self.generation_log(message)
        else:
            self.logger.info(message)

    def error(self, message):
        print(f"{TerminalColors.RED}⛔ ERROR: {message}{TerminalColors.ENDC}")
        self.logger.error(message)

    def node_log(self, message):
        message = message.replace("Node:", f"{TerminalColors.PURPLE}Node:{TerminalColors.ENDC}")
        print(f"{TerminalColors.CYAN}🔷 {message}{TerminalColors.ENDC}")

    def edge_log(self, message):
        message = message.replace("Edge:", f"{TerminalColors.YELLOW}Edge:{TerminalColors.ENDC}")
        print(f"{TerminalColors.BLUE}➡️  {message}{TerminalColors.ENDC}")

    def http_log(self, message):
        if "200 OK" in message:
            status_color = TerminalColors.GREEN
        else:
            status_color = TerminalColors.YELLOW
        message = message.replace("HTTP/1.1", f"{status_color}HTTP/1.1{TerminalColors.ENDC}")
        print(f"{TerminalColors.GRAY}🌐 {message}{TerminalColors.ENDC}")

    def retrieval_log(self, message):
        print(f"{TerminalColors.CYAN}🔍 {message}{TerminalColors.ENDC}")

    def context_log(self, message):
        print(f"{TerminalColors.GREEN}📄 {message}{TerminalColors.ENDC}")

    def score_log(self, message):
        print(f"{TerminalColors.YELLOW}⭐ {message}{TerminalColors.ENDC}")

    def agent_log(self, message, emoji):
        print(f"{TerminalColors.PURPLE}{emoji} {message}{TerminalColors.ENDC}")

    def generation_log(self, message):
        print(f"{TerminalColors.GREEN}💡 {message}{TerminalColors.ENDC}")
