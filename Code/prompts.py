from enum import Enum

class SystemPrompt(Enum):
    template = "Evaluate the following scenario from a <framework> perspective. Based on your evaluation, answer if this is acceptable or not:"
    DEONTOLOGY = template.replace("<framework>", "deontological")
    CONSEQUENTIALISM = template.replace("<framework>", "consequentialist")
    VIRTUE_ETHICS = template.replace("<framework>", "virtue ethics")