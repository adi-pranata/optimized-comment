import json
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class Comment:
    id: int  
    score: int  
    text: str  
    children: List['Comment']  

def build_comment_tree(data: Dict) -> Comment:
    """Recursively builds a comment tree from a JSON dictionary."""
    return Comment(
        id=data["id"], 
        score=data["score"], 
        text=data["text"],
        children=[build_comment_tree(child) for child in data.get("children", [])]
    )

def select_optimal_comments(thread: Dict, depth_limit: int) -> List[int]:
    """
    Selects the optimal subset of comments, maximizing total score,
    while ensuring depth constraints and parent-child dependencies.
    """
    memo = {}  # Caching results for optimization

    def dfs(comment: Comment, depth: int) -> Tuple[int, List[int]]:
        """Performs DFS to determine the optimal comment selection."""
        if depth > depth_limit:
            return 0, []

        if comment.id in memo:
            return memo[comment.id]

        # Option 1: Select this comment
        selected_ids = [comment.id]
        total_score_with = comment.score
        child_score_sum = 0
        child_selection = []

        for child in comment.children:
            child_score, child_ids = dfs(child, depth + 1)
            if child_ids:
                child_score_sum += child_score
                child_selection.extend(child_ids)

        total_score_with += child_score_sum  # Total score if we take this comment and children

        # Option 2: Skip this comment (only valid if no children are selected)
        total_score_without = 0
        selected_without = []

        if not child_selection:
            total_score_without, selected_without = 0, []

        # Choose the better option
        if total_score_with > total_score_without:
            memo[comment.id] = (total_score_with, selected_ids + child_selection)
            return memo[comment.id]
        else:
            memo[comment.id] = (total_score_without, selected_without)
            return memo[comment.id]

    # Build comment tree from input
    comment_tree = build_comment_tree(thread)

    # Run DFS from the root
    _, optimal_selection = dfs(comment_tree, 1)

    return optimal_selection

# Load comments from JSON file
with open("comments.json", "r", encoding="utf-8") as file:
    comments_data = json.load(file)

# Define depth limit
depth_limit = 2

# Run function and get optimal comments
optimal_comments = select_optimal_comments(comments_data, depth_limit)

# Output result
print(f" Comments: {optimal_comments}")
