import platform

# Network Functions
# =================
def hostname():
    """
        Computer's name. Not guaranteed unique, but useful for zoo prototype
    """
    return platform.node()