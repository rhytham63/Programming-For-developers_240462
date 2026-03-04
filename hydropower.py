class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def max_power_generation(root):
    max_power = float('-inf')

    def dfs(node):
        nonlocal max_power

        if node is None:
            return 0

        left_gain = max(0, dfs(node.left))
        right_gain = max(0, dfs(node.right))

        current_power = node.value + left_gain + right_gain
        max_power = max(max_power, current_power)

        return node.value + max(left_gain, right_gain)

    dfs(root)
    return max_power
