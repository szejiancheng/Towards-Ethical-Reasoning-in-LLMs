from enum import Enum

class SystemPrompt(Enum):
    template = "Evaluate this scenario from a <framework> perspective, is this acceptable?"
    DEONTOLOGY = template.replace("<framework>", "deontological")
    CONSEQUENTIALISM = template.replace("<framework>", "consequentialist")
    VIRTUE_ETHICS = template.replace("<framework>", "virtue ethics")